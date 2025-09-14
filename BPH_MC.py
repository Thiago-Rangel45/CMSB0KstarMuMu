# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: --conditions 130X_mcRun3_2023_realistic_v14 --datatier NANOAOD --mc --era Run3,run3_nanoAOD_pre142X --eventcontent NANOAODSIM --filein root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/dd5a0141-ae5d-4e5d-b230-a3b40d55434e.root --fileout file:BPH_NANO.root --nThreads 4 -n -1 --no_exec --python_filename BPH_MC.py --scenario pp --step NANO:@BPH
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.Eras.Modifier_run3_nanoAOD_pre142X_cff import run3_nanoAOD_pre142X

process = cms.Process('NANO',Run3,run3_nanoAOD_pre142X)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/18b9cc80-a289-4243-8285-b7574064c253.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/25abc25e-04a5-4511-96ae-9e06b7fd7654.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/27fd440b-5776-4fc6-8908-36a62402c048.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/5301fff0-4e96-486b-87a9-196fb564a810.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/5b815577-42a0-49d6-ba5b-596fb9d5c426.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/6dc0e913-956b-4216-af66-a60d84c18d84.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/70baa8b4-a90d-4d58-a19a-d2fba4137ae3.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/7963ef8c-5044-4b18-884c-a14cebe8f502.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/8beab378-4479-498e-a3d6-0bd8a3dcf50e.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/9aac028c-665a-4c61-a862-2d407f46d187.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/a173007d-b9ba-41cf-9cb4-96726b98f40e.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/d97ddbc3-afdd-402d-aa94-4b08bb94a53b.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/ea4beaa1-f728-443e-aece-4a1f929bb25a.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/ecdeac72-a6fc-4eef-82d2-ba1c48a51671.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/f65f7c00-c071-4e1d-adcb-19987563487b.root',
        'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv3/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_124X_mcRun3_2022_realistic_v12-v2/2810000/f69ed475-eeb0-430e-b2a3-9e8035f2708d.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--conditions nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('/eos/user/t/tdeandra/BPH_NANO_124.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2023_realistic_v14', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon

#call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.custom_bph_cff
from PhysicsTools.NanoAOD.custom_bph_cff import nanoAOD_customizeBPH

#call to customisation function nanoAOD_customizeBPH imported from PhysicsTools.NanoAOD.custom_bph_cff
process = nanoAOD_customizeBPH(process)

# End of customisation functions


# Customisation from command line

process.source.delayReadingEventProducts = cms.untracked.bool(False)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion