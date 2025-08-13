#CMN="--compilation_steps_only"


echo
echo "******** 1. Running: verifyCrossChainForwarder-sanity.conf   ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-sanity.conf  \
           --msg "1. verifyCrossChainForwarder-sanity.conf "

echo
echo "******** 2. Running: verifyCrossChainForwarder-envelopRetry.conf   ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-envelopRetry.conf \
           --msg "2. verifyCrossChainForwarder-envelopRetry.conf "

echo
echo "******** 3. Running:    ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainForwarder-newEnvelope.conf \
           --msg "3. verifyCrossChainForwarder-newEnvelope.conf "

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
           --msg "7. verifyCrossChainForwarder-shuffle.conf "


echo
echo "******** 8. Running: verifyCrossChainReceiver.conf   ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainReceiver.conf \
           --msg "8. verifyCrossChainReceiver.conf "


echo
echo "******** 9. Running: verifyCrossChainControllerWithEmergency.conf   ****************"
certoraRun $CMN  security/certora/confs/verifyCrossChainControllerWithEmergency.conf \
           --msg "9. verifyCrossChainControllerWithEmergency.conf"


