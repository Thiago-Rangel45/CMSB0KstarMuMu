
## Step-by-Step for B-Physics NanoAOD Analysis

### 1. Create the CMSSW area

```bash
cmsrel CMSSW_15_1_0_pre2
cd CMSSW_15_1_0_pre2/src/
cmsenv
```

---

### 2. Clone the repository with the analysis scripts

```bash
git clone -b git@github.com:Thiago-Rangel45/CMSB0KstarMuMu.git
```

---

### 3. Compile and move to the test directory

```bash
scram b -j8
cd PhysicsTools/BPHNano/test/
cmsenv
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
cmsRun run_bphNano_cfg.py
```

This command starts the customized NanoAOD processing. Make sure the input files listed in `run_bphNano_cfg.py` are correct.

---

### 6. Run the job for data

```bash
cmsRun run_bphNano_cfg.py isMC=False
```

This command also starts the customized NanoAOD processing, but for real data. Again, ensure the input files are correctly specified in `run_bphNano_cfg.py`.

---
