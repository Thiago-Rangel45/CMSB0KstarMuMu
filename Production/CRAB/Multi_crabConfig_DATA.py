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
    config.General.workArea     = 'crab_projects_CMSSW_15_1_0'
    config.General.transferLogs = True
    config.JobType.pluginName   = 'Analysis'
    config.JobType.psetName     = '../BPH_Data_cfg.py' 
    config.JobType.numCores     = 4
    config.JobType.maxMemoryMB  = 4000
    config.JobType.sendExternalFolder = True
    config.Data.inputDBS        = 'global'    
    config.Data.splitting       = 'LumiBased'
    config.Data.publication     = False
    config.Site.storageSite     = 'T3_CH_CERNBOX'
    config.Data.lumiMask        = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraC_355862_357482_Golden.json'
    config.Data.allowNonValidInputDataset = True

    # --- Whitelist necessária quando ignoreLocality = True ---
    config.Data.ignoreLocality  = True
    config.Site.whitelist       = ['T2_*'] 
    
    def submit(config):
        try:
            res = crabCommand('submit', config = config)
        except HTTPException as hte:
            print("HTTPException:", hte.headers)
        except ClientException as cle:
            print("ClientException:", cle) 

    # ============ JOB 1 ============
    config.General.requestName = 'BPH_NanoAOD_Run2022C_LowMass1'
    config.Data.unitsPerJob    = 40
    config.Data.inputDataset   = '/ParkingDoubleMuonLowMass1/Run2022C-PromptReco-v1/MINIAOD'
    config.Data.outLFNDirBase  = '/store/user/tdeandra/BPH_NanoAOD_Data/'
    config.Data.outputDatasetTag = 'BPH_NanoAOD_Run2022C_Data_LowMass1'
    p1 = Process(target=submit, args=(config,)) # Mudei para p1 para clareza
    p1.start()
    p1.join()

    # ============ JOB 2 ============
    config.General.requestName = 'BPH_NanoAOD_Run2022C_LowMass2'
    config.Data.unitsPerJob    = 40
    config.Data.inputDataset   = '/ParkingDoubleMuonLowMass2/Run2022C-PromptReco-v1/MINIAOD'
    config.Data.outLFNDirBase  = '/store/user/tdeandra/BPH_NanoAOD_Data/'
    config.Data.outputDatasetTag = 'BPH_NanoAOD_Run2022C_Data_LowMass2'
    p2 = Process(target=submit, args=(config,)) # Mudei para p2
    p2.start()
    p2.join()

    print("\n" + "="*60)
    print("SCRIPT FINALIZADO")
    print("="*60)