CMN="--compilation_steps_only"


echo
echo "******** 1. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-sanity.conf  \
           --msg "1.  "

echo
echo "******** 2. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-envelopRetry.conf \
           --msg "2.  "

echo
echo "******** 3. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-newEnvelope.conf \
           --msg "3.  "

echo
echo "******** 4. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-simpleRules.conf \
           --msg "4.  "

echo
echo "******** 5. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-invariants.conf \
           --msg "5.  "

echo
echo "******** 6. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-encode-decode-correct.conf \
           --rule encode_decode_well_formed_TX \
           --msg "6.  "

echo
echo "******** 7. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-shuffle.conf \
           --msg "7.  "

