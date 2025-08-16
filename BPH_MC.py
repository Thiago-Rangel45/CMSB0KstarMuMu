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
    input = cms.untracked.int32(1000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2520000/790ab392-1e36-4471-b63c-6b4f41b2db24.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/2e9dba99-bd16-45ab-ba97-3ba833da2025.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/3137600b-9553-4322-a8cb-02e935118e10.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/8605db4f-46dd-462e-a54e-2532a1184b88.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/d2298dc2-bc0f-4438-b81f-ccd7e9c35c25.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2530000/dd5a0141-ae5d-4e5d-b230-a3b40d55434e.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/2540000/738cd115-7066-40e2-97b9-df9af278916e.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/1a903a7b-9283-4e95-8318-a873db537417.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/3152adf8-7887-4a9c-889c-6808ad4fab3c.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/35fd1606-9377-4214-8818-d102c4cf968d.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/5a1e5814-2ef2-43b8-995c-0e750b056a6b.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/64fe945b-c1f6-438c-a5be-f5e947619c55.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/82a5537d-272d-42f8-b4f2-072938e58bf1.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/cbdc6258-79bf-4d27-b086-11ac193102e6.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/30000/fbaab031-2b87-472d-ab6b-b56f0da186a5.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/40000/a06f1583-c9bd-4297-904e-0a718c8ac880.root',
                                      'root://cms-xrd-global.cern.ch//store/mc/Run3Summer22MiniAODv4/BdToKstarMuMu_KplusPiminusFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/rndm_130X_mcRun3_2022_realistic_v5-v2/60000/ef4addd4-4089-4719-915c-6a83ce205ade.root'),
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
    fileName = cms.untracked.string('/eos/user/t/tdeandra/BPH_NANO.root'),
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