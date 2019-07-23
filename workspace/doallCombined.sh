#!/bin/bash
ZREGION=ch1_DNNAtanNoMass___ZRegion
ZCONTROL=ch1_pTbalanceAll___ZRegion
ZREGIONBDT=ch1_BDTAtanNoMass___ZRegion

SIGNAL=ch2_DNNAtan___SignalRegion
SIDE=ch2_DNNAtanNoMass___SideBand
SIGNALBDT=ch2_BDTAtan___SignalRegion
SIDEBDT=ch2_BDTAtanNoMass___SideBand

YEARS="run2016 run2017 run2018"
#YEARS="run2018"
for i in 2016 2017 2018 ; do
  combineCards.py datacard${i}Z.txt datacard${i}H.txt > datacard${i}.txt
done 
combineCards.py run2016=datacard2016.txt run2017=datacard2017.txt run2018=datacard2018.txt > combined.txt
#combineCards.py run2018=datacard2018.txt > combined.txt

TOMASK="$ZCONTROL $SIGNAL $ZREGION  $SIDE $SIGNALBDT"
TOFIT="$SIDEBDT $ZREGIONBDT"
#TOMASK="$ZCONTROL $SIGNAL"
#TOFIT="$SIDE $ZREGION"
PREFITMASK=`for y in $YEARS ; do for i in $TOMASK; do echo -ne mask_${y}_${i}=1, ; done ; done`
PREFITNOMASK=`for y in $YEARS ; do for i in $TOFIT; do echo -ne mask_${y}_${i}=0, ; done ; done`
PREFIT="--setParameters $PREFITMASK$PREFITNOMASK"

TOMASK="$ZCONTROL $SIGNAL $ZREGION  $SIDE"
TOFIT="$SIDEBDT $ZREGIONBDT $SIGNALBDT"
#TOMASK=$ZCONTROL 
#TOFIT="$SIDE $ZREGION $SIGNAL"
FITMASK=`for y in $YEARS ; do for i in $TOMASK; do echo -ne mask_${y}_${i}=1, ; done ; done`
FITNOMASK=`for y in $YEARS ; do for i in $TOFIT; do echo -ne mask_${y}_${i}=0, ; done ; done`
FIT="--setParameters $FITMASK$FITNOMASK"

echo "Prefit: " $PREFIT
echo "Fit: " $FIT

DCTXT=combined.txt
NAME=cmb

./decorrelate.sh >> combined.txt
text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel    --channel-masks ${DCTXT}   --PO  'map=.*Hmm.*:r[1.,-10,10]'  >>${NAME}.log

combine  -M MultiDimFit -n$NAME --saveWorkspace $PREFIT combined.root --verbose 9   >>${NAME}.log

combine -M Significance --snapshotName MultiDimFit -t -1  higgsCombine${NAME}.MultiDimFit.mH120.root ${FIT}r=1   >>${NAME}.log
combine -M Significance --snapshotName MultiDimFit -t -1  higgsCombine${NAME}.MultiDimFit.mH120.root ${FIT}r=1  --toysFrequentist  >>${NAME}.log
