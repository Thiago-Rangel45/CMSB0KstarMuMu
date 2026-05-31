from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'BPH_NanoAOD_Data_Run20223'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/afs/cern.ch/user/t/tdeandra/CMSSW_15_1_0/src/BPH_Data_cfg.py'
config.Data.unitsPerJob    = 40
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 4000
config.JobType.sendExternalFolder = True

config.Data.inputDataset = '/ParkingDoubleMuonLowMass0/Run2023C-PromptReco-v4/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.publication = False
config.Data.outputDatasetTag = 'BPH_NanoAOD_Run2023C'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/PromptReco/Cert_Collisions2023_eraC_367095_368823_Golden.json'

config.Site.storageSite = 'T2_BR_UERJ'