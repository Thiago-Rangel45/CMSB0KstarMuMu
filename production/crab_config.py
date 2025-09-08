from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'BPH_NanoAOD_Data_Run2022C_1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../BPH_Data.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 4000
config.JobType.sendExternalFolder = True

config.Data.inputDataset = '/ParkingDoubleMuonLowMass0/Run2022C-PromptReco-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.outLFNDirBase = '/store/user/tdeandra/'
config.Data.publication = False
config.Data.outputDatasetTag = 'BPH_NanoAOD_Run2022C'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraC_355862_357482_Golden.json'

config.Site.storageSite = 'T3_CH_CERNBOX'