from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'BPH_NanoAOD_MC_Run2022C_jpsi'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../BPH_MC.py'
config.Data.unitsPerJob    = 40
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 4000
config.JobType.sendExternalFolder = True

config.Data.inputDataset = '/BdToJpsiKstar_BMuonFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.publication = False
config.Data.outputDatasetTag = 'BPH_NanoAOD_Run2022C_MC'

config.Site.storageSite = 'T2_BR_UERJ'
