import "base.spec";
import "invariants.spec";

use invariant inv_TXid_maps_have_same_IDs;
use invariant inv_every_forwarded_TX_contains_registered_EV;
use invariant inv_TXnonce_less_than_curr_nonce;
use invariant nonce_correct;
use invariant max_nonceTX_is_valid;


/* ========================================================             /
   Rule 1: Only the approved senders can forward a message.            /
   Status: PASS                                                    \  /
                                                                    \/
   ========================================================*/
rule _01_only_approved_senders_can_call_forwardMessage() {
    env e;
    uint256 destinationChainId;
    address destination;
    uint256 gasLimit;
    bytes message;

    forwardMessage(e, destinationChainId, destination, gasLimit, message);

    assert (isSenderApproved(e.msg.sender));
}


/* ========================================================             /
   Rule 2: Internal transaction nonces are sequential.                 /
   Status: PASS                                                    \  /
                                                                    \/
   Remark: The implementation of this rule is the following:
   If retryTransaction() was called (hence no new transaction), then 
   we check that the max-TX-nonce was not changed.
   If retryEnvelope() or forwardMessage() were called then the nonce is
   the previous maximal nonce + 1.
   We can argue by induction that this implies that the transaction nonces (of transactions
   generated by retryEnvelope() or forwardMessage()) are indeed sequential.
   ========================================================*/
rule _02_transaction_nonce_are_sequential (method f)
    filtered {f -> f.selector!=sig:reset_harness_storage().selector}
{
    env e;
    calldataarg args;
    reset_harness_storage();

    requireInvariant max_nonceTX_is_valid();
    requireInvariant nonce_correct();
    requireInvariant inv_TXid_maps_have_same_IDs();
    requireInvariant inv_TXnonce_less_than_curr_nonce();
    
    uint256 before_max_TXnonce = get_max_TXnonce();
    bool first_call_to_bridgeTransaction = getCurrentTransactionNonce()==0;
    f(e,args);
    uint256 after_TXnonce = get_last_nonceTX_sent();
    uint256 after_max_TXnonce = get_max_TXnonce();

    if (f.selector == sig:retryTransaction(bytes,uint256,address[]).selector) {
        assert (bridgeTransaction_was_called());
        assert (after_TXnonce <= before_max_TXnonce);
        assert (before_max_TXnonce == after_max_TXnonce);
    }
    else {
        assert( (bridgeTransaction_was_called() && !first_call_to_bridgeTransaction)
                =>
                (to_mathint(after_TXnonce)==before_max_TXnonce+1)
              );
    }
}


/* ========================================================
   Rule 18: Only the Owner can enable/disable authorized senders.
   Status: PASS
   ========================================================*/
rule _18_only_owner_can_change_senders_list(method f) {
    env e;
    address alice;
    bool alice_is_sender_prev = isSenderApproved(alice);
    
    calldataarg args;
    f(e,args);
    
    bool alice_is_sender_after = isSenderApproved(alice);

    assert (e.msg.sender == owner() || alice_is_sender_prev==alice_is_sender_after);
}

/* ========================================================
   Rule 19: Only the Owner can enable/disable bridge adapters.
   Status: PASS
   ========================================================*/
rule _19_only_owner_can_change_bridge_adapters(method f) {
    env e;
    uint256 chainId;
    uint ind;
    address before_dest = getForwarderBridgeAdaptersByChainAtPos_dest(chainId,ind);
    address before_curr = getForwarderBridgeAdaptersByChainAtPos_curr(chainId,ind);
        
    calldataarg args;
    f(e,args);

    address after_dest = getForwarderBridgeAdaptersByChainAtPos_dest(chainId,ind);
    address after_curr = getForwarderBridgeAdaptersByChainAtPos_curr(chainId,ind);

    assert (e.msg.sender == owner() || (before_dest==after_dest && before_curr==after_curr) );
}

/* ========================================================
   Rule 20: An adapter can not be the address 0.
   Status: PASS
   ========================================================*/
invariant _20_adapter_cant_be_0()
    (forall uint id. forall uint pos.
     pos<mirror_bridgeAdaptersByChain_IDlen[id] =>
     (mirrorArray_dest[id][pos] != 0 && mirrorArray_curr[id][pos] != 0) 
    );



/* ========================================================
   Rule 21: A sender can not be the address 0.
   Status: PASS
   ========================================================*/
invariant _21_sender_cant_be_0()
    isSenderApproved(0)==false;





/* ===========================================================================
   Rule 10: Forwarding a message should revert if no bridge adapters are 
         registered for the destination chain.

   Status: PASS
   ========================================================================= */
rule _10_revert_if_no_bridge() {
    env e;
    uint256 destinationChainId;
    address destination;
    uint256 gasLimit;
    bytes message;

    uint num_of_adapters = getForwarderBridgeAdaptersByChain_len(destinationChainId);
    forwardMessage@withrevert(e, destinationChainId, destination, gasLimit, message);

    assert (num_of_adapters==0 => lastReverted);
}

/* ===========================================================================
   Rule 11: An Envelope can only be retried if it has been previously registered.

   Status: PASS
   ========================================================================= */
rule _11_retry_envelope_only_if_registered() {
    env e;
    CrossChainForwarderHarness.Envelope envelope;
    uint256 gasLimit;
    bytes32 last_transactionId = retryEnvelope@withrevert(e,envelope,gasLimit);
    bool reverted = lastReverted;
    
    bool previously_registered = isEnvelopeRegistered(envelope);


    assert (!previously_registered => reverted);
}

/* ===========================================================================
   Rule 14: A Transaction can only be retried if it has been previously forwarded

   Status: PASS (with loop-iter==1)
   ========================================================================= */
rule _14_retry_transaction_only_if_forwarded() {
    env e;

    bytes encodedTransaction;
    uint256 gasLimit;
    address[] bridgeAdaptersToRetry;

    bytes32 transactionId = get_transaction_ID_from_encodedTX(encodedTransaction); 
    
    retryTransaction@withrevert(e,encodedTransaction,gasLimit,bridgeAdaptersToRetry);
    bool reverted = lastReverted;
    
    bool previously_registered = isTransactionForwarded(transactionId);

    assert (!previously_registered => reverted);
}


