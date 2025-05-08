# Setup para Análise de B-Physics NanoAOD 

## 🔧 Passo a passo

### 1. Criar área do CMSSW

```bash
cmsrel CMSSW_15_1_0_pre2
cd CMSSW_15_1_0_pre2/src/
cmsenv
```
---

### 2. Adicionar pacotes necessários

```bash
git cms-addpkg Configuration/PyReleaseValidation/
git cms-addpkg DataFormats/PatCandidates/
git cms-addpkg TrackingTools/TransientTrack
```

---

### 3. Clonar o repositório com os scripts da análise

```bash
git clone -b cmsDriver_command git@github.com:gmelachr/BPHNano.git ./PhysicsTools
git cms-addpkg PhysicsTools/NanoAOD
```

---

### 4. Copiar arquivos modificados de um repositório público

```bash
# TrackingTools
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/classes* TrackingTools/TransientTrack/src/

# DataFormats
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/classes_def_objects.xml DataFormats/PatCandidates/src/

# Configuration
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/relval_nano.py Configuration/PyReleaseValidation/python/

# PhysicsTools/NanoAOD plugins
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/CandMCMatchTableProducer.cc PhysicsTools/NanoAOD/plugins/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/SimpleFlatTableProducerPlugins.cc PhysicsTools/NanoAOD/plugins/

# Python files para NanoAOD
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/autoNANO.py PhysicsTools/NanoAOD/python/
cp /afs/cern.ch/user/g/gmelachr/public/forDiego/custom_bph_cff.py PhysicsTools/NanoAOD/python/
```

---

### 5. Navegar até o diretório de teste

```bash
cd PhysicsTools/BPHNano/test/
cmsenv
```

---

### 6. Inicializar proxy para acesso ao GRID 

```bash
voms-proxy-init --rfc --voms cms
```

> Após digitar sua senha do GRID, você verá uma confirmação:
>
> ```
> Created proxy in /tmp/x509up_uXXXXXX.
> Your proxy is valid until [data/hora].
> ```

---

### 7. Executar o job para MC

```bash
cmsRun run_bphNano_cfg.py
```

Esse comando inicia o processamento do NanoAOD customizado. Certifique-se de que os arquivos de entrada no `run_bphNano_cfg.py` estão corretos.

---

### 8. Executar o job para dados

```bash
cmsRun run_bphNano_cfg.py isMC=False
```

Esse comando inicia o processamento do NanoAOD customizado. Certifique-se de que os arquivos de entrada no `run_bphNano_cfg.py` estão corretos.

---
