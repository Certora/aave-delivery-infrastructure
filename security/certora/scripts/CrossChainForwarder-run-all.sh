
certoraRun --send_only \
           --fe_version latest \
           security/certora/confs/verifyCrossChainForwarder-sanity.conf 

certoraRun --send_only \
           --fe_version latest \
           security/certora/confs/verifyCrossChainForwarder-envelopRetry.conf

certoraRun --send_only \
           --fe_version latest \
           security/certora/confs/verifyCrossChainForwarder-newEnvelope.conf

certoraRun --send_only \
           --fe_version latest \
           security/certora/confs/verifyCrossChainForwarder-simpleRules.conf

certoraRun --send_only \
           --fe_version latest \
           security/certora/confs/verifyCrossChainForwarder-invariants.conf
