if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    
    try:
        from http.client import HTTPException
    except ImportError:
        from httplib import HTTPException

    from CRABClient.UserUtilities import config
    config = config()
    
    from multiprocessing import Process

    # ================= CONFIGURAÇÃO GERAL =================
    config.General.workArea     = 'crab_projects_CMSSW_15_1_0_MC'
    config.General.transferLogs = True
    config.JobType.pluginName   = 'Analysis'
    config.JobType.psetName     = '../BPH_MC.py' 
    config.JobType.numCores     = 4
    config.JobType.maxMemoryMB  = 4000
    config.JobType.sendExternalFolder = True
    config.Data.inputDBS        = 'global'    
    config.Data.splitting       = 'LumiBased'
    config.Data.publication     = False
    config.Site.storageSite     = 'T2_BR_UERJ'
    
    # --- Para MC não usamos lumiMask nem ignoreLocality ---
    config.Data.ignoreLocality  = False
    
    def submit(config):
        try:
            res = crabCommand('submit', config = config)
        except HTTPException as hte:
            print("HTTPException:", hte.headers)
        except ClientException as cle:
            print("ClientException:", cle) 

    # ============ JOB 1 ============
    config.General.requestName = 'BPH_NanoAOD_MC_BdToJpsiKstar'
    config.Data.unitsPerJob    = 40
    config.Data.inputDataset   = '/BdToJpsiKstar_BMuonFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
    config.Data.outLFNDirBase  = '/store/user/tdeandra/BPH_NanoAOD_MC/'
    config.Data.outputDatasetTag = 'BPH_NanoAOD_MC_BdToJpsiKstar'
    p1 = Process(target=submit, args=(config,))
    p1.start()
    p1.join()

    # ============ JOB 2 ============
    config.General.requestName = 'BPH_NanoAOD_MC_BdToKstar2Mu'
    config.Data.unitsPerJob    = 40
    config.Data.inputDataset   = '/BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
    config.Data.outLFNDirBase  = '/store/user/tdeandra/BPH_NanoAOD_MC/'
    config.Data.outputDatasetTag = 'BPH_NanoAOD_MC_BdToKstar2Mu'
    p2 = Process(target=submit, args=(config,))
    p2.start()
    p2.join()

    print("\n" + "="*60)
    print("SCRIPT MC FINALIZADO")
    print("="*60)