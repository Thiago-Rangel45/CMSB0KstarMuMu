# nanoAOD producer customized for BPH analysis 

The focus is on B -> mumu X analyses.
Based on the code of RK 2018 (BParkingNano)

## Getting started

```shell
cmsrel CMSSW_15_1_X
cd CMSSW_15_1_X/src
cmsenv
git cms-init
```
Architecture should be el8 or el9

## Add the BPHNano package and build everything

```shell
git clone -b cmsDriver_command git@github.com:gmelachr/BPHNano.git ./PhysicsTools
git cms-addpkg PhysicsTools/NanoAOD 
scram b -j 8 
```
or https equivalent

## To run on a test file

```shell
cd PhysicsTools/BPHNano/test/
cmsenv 
cmsRun run_bphNano_cfg.py
```

## cmsDriver command
```shell

Data: cmsDriver.py --conditions 140X_dataRun3_Prompt_v4 --datatier NANOAOD --data --era Run3,run3_nanoAOD_pre142X --eventcontent NANOAOD --filein root://cms-xrd-global.cern.ch//store/data/Run2024C/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/379/416/00000/0134a8bc-c8d4-400e-9508-2a4b222c5431.root --fileout file:/tmp/gmelachr/BPH_test_data.root --nThreads 4 -n 4500 --no_exec --python_filename BPH_test.py --scenario pp --step NANO:@BPH

MC: cmsDriver.py --conditions 130X_mcRun3_2023_realistic_v14 --datatier NANOAOD --era Run3_2023,run3_nanoAOD_pre142X --eventcontent NANOAODSIM --filein root://cms-xrd-global.cern.ch//store/mc/Run3Summer23MiniAODv4/ButoJpsiK_Jpsito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2820000/14c41e05-3e09-4255-86aa-201b687345a7.root --fileout file:/tmp/gmelachr/BPH_mc.root --nThreads 4 -n -1 --no_exec --python_filename BPH_MC.py --scenario pp --step NANO:@BPH --mc

#era modifier run3_nanoAOD_pre142X required in order to run in CMSSW_15_X miniAODs produced with CMSSW_14 or previous releases 
```




