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
    #config.JobType.psetName     = '../BPH_Data_cfg.py' 
    config.JobType.psetName = '/afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0/src/BPH_Data_cfg.py'
    config.JobType.numCores     = 4
    config.JobType.maxMemoryMB  = 4000
    config.JobType.sendExternalFolder = True
    config.Data.inputDBS        = 'global'    
    config.Data.splitting       = 'LumiBased'
    config.Data.publication     = False
    config.Data.allowNonValidInputDataset = True
    config.Site.storageSite     = 'T2_BR_UERJ' 

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

    base_url = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/'
    lumi_masks = {
        'C': base_url + 'Cert_Collisions2022_eraC_355862_357482_Golden.json',
        'D': base_url + 'Cert_Collisions2022_eraD_357538_357900_Golden.json',
        'E': base_url + 'Cert_Collisions2022_eraE_359022_360331_Golden.json',
        'F': base_url + 'Cert_Collisions2022_eraF_360390_362167_Golden.json',
        'G': base_url + 'Cert_Collisions2022_eraG_362433_362760_Golden.json'
    }

    reco_versions = {
        'C': 'v1',
        'D': 'v2',
        'E': 'v1',
        'F': 'v1',
        'G': 'v1'
    }
    eras = ['C', 'D', 'E', 'F', 'G']
    
    for era in eras:
        for ds in range(8):
            
            version = reco_versions[era]            
            input_ds = f'/ParkingDoubleMuonLowMass{ds}/Run2022{era}-PromptReco-{version}/MINIAOD'
            
            config.General.requestName = f'BPH_Run22{era}_LowMass{ds}'
            config.Data.inputDataset   = input_ds
            config.Data.unitsPerJob    = 40            
            config.Data.lumiMask       = lumi_masks[era]            
            config.Data.outLFNDirBase  = f'/store/user/tdeandra/BPH_NanoAOD_Data/Run2022{era}/'
            config.Data.outputDatasetTag = f'NanoAOD_LowMass{ds}'
            
            print(f"Submetendo Era {era} | Dataset {ds} | Versão: {version} | JSON: {lumi_masks[era].split('/')[-1]}")
            
            p = Process(target=submit, args=(config,))
            p.start()
            p.join() 

    print("\n" + "="*60)
    print("SCRIPT FINALIZADO")
    print("="*60)