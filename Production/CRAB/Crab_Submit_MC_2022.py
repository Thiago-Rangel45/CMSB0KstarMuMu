#!/usr/bin/env python3
import os
from multiprocessing import Process
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from CRABClient.UserUtilities import config

try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

def submit(config):
    try:
        print(f"==> Submetendo: {config.General.requestName}")
        crabCommand('submit', config=config)
    except HTTPException as hte:
        print(f"Erro HTTP na submissão: {hte.headers}")
    except ClientException as cle:
        print(f"Erro no Cliente CRAB: {cle}")

if __name__ == '__main__':

    conf = config()

    # ================= CONFIGURAÇÃO GERAL =================
    conf.General.workArea     = 'crab_projects_CMSSW_15_1_0_MC'
    conf.General.transferLogs = True
    
    conf.JobType.pluginName   = 'Analysis'
    conf.JobType.psetName     = '/afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0/src/BPH_MC_cfg.py' 
    conf.JobType.numCores     = 4
    conf.JobType.maxMemoryMB  = 4000
    conf.JobType.sendExternalFolder = True
    
    conf.Data.inputDBS        = 'global'    
    conf.Data.splitting       =  'Automatic' #'LumiBased' 
    conf.Data.unitsPerJob     = 500          #40
    conf.Data.publication     = False
    conf.Data.ignoreLocality  = False
    conf.Data.outLFNDirBase   = '/store/user/tdeandra/BPH_NanoAOD_MC/'
    
    conf.Site.storageSite     = 'T2_BR_UERJ'

    datasets = {

        # --- Bd -> Jpsi K* (Com MuFilter) ---
        'BdtoJpsiKstar_MuFilter_2022': '/BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoJpsiKstar_MuFilter_2022EE': '/BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',
        
        # --- Bd -> Jpsi K* (Sem Filtro) ---
        'BdtoJpsiKstar_NoFilter_2022': '/BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoJpsiKstar_NoFilter_2022EE': '/BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',

        # --- Bd -> K* MuMu (Com MuFilter) ---
        'BdtoKstarMuMu_MuFilter_2022': '/BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoKstarMuMu_MuFilter_2022EE': '/BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',

        # --- Bd -> K* MuMu (Sem Filtro ) ---
        'BdtoKstarMuMu_NoFilter_2022': '/BdtoKstar2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoKstarMuMu_NoFilter_2022EE': '/BdtoKstar2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',

        # --- Bd -> K* Psi(2S) (Com MuFilter) ---
        'BdtoKstarPsi2s_MuFilter_2022': '/BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoKstarPsi2s_MuFilter_2022EE': '/BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',

        # --- Bd -> K* Psi(2S) (Sem Filtro) ---
        'BdtoKstarPsi2s_NoFilter_2022': '/BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv3-124X_mcRun3_2022_realistic_v12-v2/MINIAODSIM',
        'BdtoKstarPsi2s_NoFilter_2022EE':'/BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22EEMiniAODv3-124X_mcRun3_2022_realistic_postEE_v1-v2/MINIAODSIM',
    }

    print(f"\nIniciando submissão de {len(datasets)} jobs...\n")

    for nick, dset in datasets.items():
        conf.General.requestName   = f"BPH_Nano_MC_{nick}_retry2"
        conf.Data.inputDataset     = dset
        conf.Data.outputDatasetTag = f"BPH_Nano_MC_{nick}_retry2"
        
        p = Process(target=submit, args=(conf,))
        p.start()
        p.join()

    print("\n" + "="*60)
    print("PROCESSO DE SUBMISSÃO CONCLUÍDO")
    print("="*60)