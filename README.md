# B-Physics NanoAOD Analysis Workflow

Este repositório fornece um guia passo a passo para a produção de NanoAODs customizados para análises de Física-B, utilizando o ambiente de software do CMS (CMSSW). O objetivo é criar arquivos de saída enxutos, contendo apenas as informações necessárias para análises específicas, como reconstruções de decaimentos do tipo B→hhμμ.

---

## Pré-requisitos

Antes de começar, certifique-se de que você possui:
* Acesso a um ambiente com o `cvmfs` e o sistema operacional `CentOS 7` ou `AlmaLinux 9` (como o `lxplus` do CERN).
* Uma conta de usuário válida no Grid do CERN para acesso aos dados.

---

## Guia de Instalação e Execução

Siga os passos abaixo para configurar o ambiente, gerar os arquivos de configuração e produzir os NanoAODs.

### 1. Criar a Área de Trabalho CMSSW

Primeiro, crie e configure o ambiente de trabalho do CMSSW.

```bash
cmsrel CMSSW_15_1_0_pre5
cd CMSSW_15_1_0_pre5/src/
cmsenv
```

### 2. Adicionar os Pacotes Necessários

Inicialize o repositório git local para o CMSSW e adicione os pacotes específicos para a customização dos NanoAODs de Física-B.

```bash
git cms-init
git cms-addpkg PhysicsTools/BPHNano
git cms-addpkg PhysicsTools/NanoAOD
```

### 3. Compilar o Ambiente

Compile os pacotes. O argumento `-j` especifica o número de threads para a compilação paralela. Ajuste este valor de acordo com os recursos da sua máquina.

```bash
scram b -j8
```

### 4. Inicializar o Proxy do Grid

Para acessar os arquivos de dados hospedados no Grid, você precisa de um proxy válido.

```bash
voms-proxy-init --voms cms
```
Você será solicitado a inserir sua senha do Grid. Uma mensagem de sucesso confirmará a criação do proxy.

---

## Produção de NanoAOD para Dados Reais (Data)

### Passo 4.A: Gerar o Arquivo de Configuração Python

Execute o comando `cmsDriver.py` abaixo para gerar o arquivo de configuração. Este exemplo utiliza dados de `Run2022C` e aplica customizações para otimizar a saída.

```bash
cmsDriver.py --python_filename BPH_Data_cfg.py \
--conditions 140X_dataRun3_Prompt_v4 \
--datatier NANOAOD \
--era Run3,run3_nanoAOD_pre142X \
--eventcontent NANOAOD \
--filein root://cms-xrd-global.cern.ch//store/data/Run2022C/ParkingDoubleMuonLowMass0/MINIAOD/PromptReco-v1/000/355/872/00000/fc32f8ac-8ba1-498d-96b2-1925a4c825fa.root \
--fileout file:BPH_data_NANO.root \
--nThreads 4 \
-n -1 \
--no_exec \
--scenario pp \
--step NANO \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeMuonBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeDiMuonBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeTrackBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeBToTrkTrkLL
```
Este comando criará o arquivo `BPH_Data_cfg.py`.

### Passo 4.B: Editar o Arquivo de Configuração

Antes de executar, é necessário fazer uma pequena edição manual no arquivo `BPH_Data_cfg.py`.

* **Remova** ou comente (com `#`) a seguinte linha referente à identificação de taus, pois ela não é suportada nesta versão do CMSSW:

    ```python
    # Em BPH_Data_cfg.py, encontre e remova esta linha:
    tauID('byVVVLooseDeepTau2018v2p5VSjet'),
    ```

### Passo 4.C: Executar o Job

Finalmente, inicie a produção do NanoAOD customizado com o comando `cmsRun`.

```bash
cmsRun BPH_Data_cfg.py
```

---

## Produção de NanoAOD para Monte Carlo (MC)

O fluxo para dados simulados é similar, mas usa configurações diferentes.

### Passo 5.A: Gerar o Arquivo de Configuração para MC

Use o `cmsDriver.py` com a flag `--mc` e as condições apropriadas para Monte Carlo.

```bash
cmsDriver.py --python_filename BPH_MC_cfg.py \
--conditions 130X_mcRun3_2023_realistic_v14 \
--datatier NANOAODSIM \
--mc \
--era Run3,run3_nanoAOD_pre142X \
--eventcontent NANOAODSIM \
--filein root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/dd5a0141-ae5d-4e5d-b230-a3b40d55434e.root \
--fileout file:BPH_MC_NANO.root \
--nThreads 4 \
-n -1 \
--no_exec \
--scenario pp \
--step NANO \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeMuonBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeDiMuonBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeTrackBPH \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeBToTrkTrkLL \
--customise=PhysicsTools/NanoAOD/custom_bph_cff.nanoAOD_customizeMC
```

### Passo 5.B: Customizar a Saída (Opcional)

Para reduzir ainda mais o tamanho do arquivo final, você pode remover coleções de dados indesejadas. Adicione as seguintes linhas ao final do arquivo `BPH_MC_cfg.py` gerado:

```python
# Adicione estas linhas ao BPH_MC_cfg.py
process.NANOAODSIMoutput.outputCommands.append('drop *_*_*_L1')
process.NANOAODSIMoutput.outputCommands.append('drop *_*_*_HLT')
```

### Passo 5.C: Executar o Job de MC

```bash
cmsRun BPH_MC_cfg.py
```

---

## Contato e Contribuições

📬 Sinta-se à vontade para abrir *issues* para reportar bugs e sugerir melhorias, ou enviar *pull requests* para contribuir com o projeto.
