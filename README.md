
## Step-by-Step for B-Physics NanoAOD Analysis

### 1. Create the CMSSW area

```bash
cmsrel CMSSW_15_1_X_2025-07-16-2300
cd CMSSW_15_1_X_2025-07-16-2300/src/
cmsenv
```

---

### 2. Clone the repository with the analysis scripts

```bash
git cms-init
git cms-addpkg PhysicsTools/BPHNano
git cms-addpkg PhysicsTools/NanoAOD
```

---

### 3. Compile and create the python script

```bash
scram b -j8

cmsDriver.py --conditions 140X_dataRun3_Prompt_v4 --datatier NANOAOD --era Run3,run3_nanoAOD_pre142X --eventcontent NANOAOD --filein root://cms-xrd-global.cern.ch//store/data/Run2024C/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/379/415/00000/b40397b5-61c6-4887-8f4e-025e8ca925ee.root --fileout file:BPH_test_data.root --nThreads 4 -n -1 --no_exec --python_filename BPH_test.py --scenario pp --step NANO:@BPH
```
---

### 4. Initialize proxy to access the GRID

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

### 5. Run the job for MC

```bash
cmsRun BPH_test.py
```

This command starts the customized NanoAOD processing. Make sure the input files listed in `run_bphNano_cfg.py` are correct.

---
