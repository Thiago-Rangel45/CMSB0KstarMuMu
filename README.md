# B-Physics NanoAOD Analysis Workflow

This guide provides a step-by-step setup for producing customized B-Physics NanoAODs using CMSSW.

---

## Step-by-Step for B-Physics NanoAOD Analysis

### 1. Create the CMSSW area

```bash
cmsrel CMSSW_15_1_0_pre5
cd CMSSW_15_1_0_pre5/src/
cmsenv
```
---

### 2. Clone the repository with the analysis scripts

```bash
git cms-init
git cms-addpkg PhysicsTools/BPHNano
git cms-addpkg PhysicsTools/NanoAOD
```

These packages are required for B-physics NanoAOD customization.

---

### 3. Compile the environment

```bash
scram b -j8
```

The `-j8` flag allows parallel compilation with 8 threads. You can adjust it based on your machine.

---

### 4. Generate the python configuration for NanoAOD production (example with Run2024C data)

```bash
cmsDriver.py --conditions 140X_dataRun3_Prompt_v4 --datatier NANOAOD --era Run3,run3_nanoAOD_pre142X --eventcontent NANOAOD --filein root://cms-xrd-global.cern.ch//store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/355/872/00000/fc32f8ac-8ba1-498d-96b2-1925a4c825fa.root --fileout file:BPH_test_data.root --nThreads 4 -n -1 --no_exec --python_filename BPH_test.py --scenario pp --step NANO:@BPH
```

This creates the configuration file `BPH_test.py`, which defines the NanoAOD workflow.

---

### 5. Initialize proxy to access the GRID

```bash
voms-proxy-init --voms cms
```

> After entering your GRID password, you should see confirmation like:
>
> ```
> Created proxy in /tmp/x509up_uXXXXXX.
> Your proxy is valid until [date/time].
> ```

---

### 6. Modify customization in the python config

Before running, update the file:

```
PhysicsTools/NanoAOD/python/custom_bph_cff.py
```

- **Remove** (or comment out) the following tau ID that is not supported in this release:

```python
tauID('byVVVLooseDeepTau2018v2p5VSjet'),
```

- **Replace** the default customization:

```python
from PhysicsTools.NanoAOD.custom_bph_cff import nanoAOD_customizeBPH 
#process = nanoAOD_customizeBPH(process)
```

with a **more focused customization** (only muons, dimuons, tracks, and B→hh decays):

```python
from PhysicsTools.NanoAOD.custom_bph_cff import *
process = nanoAOD_customizeMuonBPH(process)
process = nanoAOD_customizeDiMuonBPH(process)
process = nanoAOD_customizeTrackBPH(process)
process = nanoAOD_customizeBToTrkTrkLL(process)
```

This reduces the output content to only what's necessary for typical B→hhμμ analyse.

---

### 7. Run the job

```bash
cmsRun BPH_test.py
```

✅ This command starts the customized NanoAOD production. Ensure the `filein` path is valid.

---

## Notes

- For **MC workflows**, use the following `cmsDriver.py` command instead (note the `--mc` flag and different condition tag):

```bash
cmsDriver.py MC \
  --conditions 130X_mcRun3_2023_realistic_v14 \
  --datatier NANOAOD \
  --mc \
  --era Run3,run3_nanoAOD_pre142X \
  --eventcontent NANOAODSIM \
  --filein root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/8beab378-4479-498e-a3d6-0bd8a3dcf50e.root \
  --fileout file:BPH_NANO.root \
  --nThreads 4 \
  -n -1 \
  --no_exec \
  --python_filename BPH_MC.py \
  --scenario pp \
  --step NANO:@BPH
```

- Then run it with:

```bash
cmsRun BPH_MC.py
```

---

📬 Feel free to open issues or pull requests for improvements or bug reports.
