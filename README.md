
## Step-by-Step for B-Physics NanoAOD Analysis

### 1. Create the CMSSW area

```bash
cmsrel CMSSW_15_1_0_pre2
cd CMSSW_15_1_0_pre2/src/
cmsenv
```

---

### 2. Add the required packages

```bash
git cms-addpkg Configuration/PyReleaseValidation/
git cms-addpkg DataFormats/PatCandidates/
git cms-addpkg TrackingTools/TransientTrack
```

---

### 3. Clone the repository with the analysis scripts

```bash
git clone -b cmsDriver_command git@github.com:gmelachr/BPHNano.git ./PhysicsTools
git cms-addpkg PhysicsTools/NanoAOD
```

---

### 4. Copy modified files from a public repository

> **Note:** Replace the user path with your own on lxplus.

```bash
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/classes* /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/TrackingTools/TransientTrack/src/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/classes_def_objects.xml /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/DataFormats/PatCandidates/src/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/relval_nano.py /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/Configuration/PyReleaseValidation/python/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/CandMCMatchTableProducer.cc /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/PhysicsTools/NanoAOD/plugins/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/SimpleFlatTableProducerPlugins.cc /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/PhysicsTools/NanoAOD/plugins/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/autoNANO.py /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/PhysicsTools/NanoAOD/python/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/custom_bph_cff.py /afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0_pre2/src/PhysicsTools/NanoAOD/python/
```

---

### 5. Compile and move to the test directory

```bash
scram b -j8
cd PhysicsTools/BPHNano/test/
cmsenv
```

---

### 6. Initialize proxy to access the GRID

```bash
voms-proxy-init --rfc --voms cms
```

> After entering your GRID password, you should see confirmation like:
>
> ```
> Created proxy in /tmp/x509up_uXXXXXX.
> Your proxy is valid until [date/time].
> ```

---

### 7. Run the job for MC

```bash
cmsRun run_bphNano_cfg.py
```

This command starts the customized NanoAOD processing. Make sure the input files listed in `run_bphNano_cfg.py` are correct.

---

### 8. Run the job for data

```bash
cmsRun run_bphNano_cfg.py isMC=False
```

This command also starts the customized NanoAOD processing, but for real data. Again, ensure the input files are correctly specified in `run_bphNano_cfg.py`.

---
