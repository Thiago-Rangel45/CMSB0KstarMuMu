////////////////////////////// BToTrkTrkLLBuilder //////////////////////////////
/// original authors: G Karathanasis (CERN),  G Melachroinos (NKUA)
// takes the ditrack collection and a dilepton collection and produces B moth
// - ers using a four-track vertex

#include <algorithm>
#include <limits>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include "CommonTools/Statistics/interface/ChiSquaredProbability.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "KinVtxFitter.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "helper.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

class BToTrkTrkLLBuilder : public edm::global::EDProducer<> {
  // perhaps we need better structure here (begin run etc)
public:
  typedef std::vector<reco::TransientTrack> TransientTrackCollection;

  explicit BToTrkTrkLLBuilder(const edm::ParameterSet &cfg)
      : bFieldToken_{esConsumes<MagneticField, IdealMagneticFieldRecord>()},
        // selections
        pre_vtx_selection_{cfg.getParameter<std::string>("preVtxSelection")},
        post_vtx_selection_{cfg.getParameter<std::string>("postVtxSelection")},
        // inputs
        dileptons_{consumes<pat::CompositeCandidateCollection>(cfg.getParameter<edm::InputTag>("dileptons"))},
        ditracks_{consumes<pat::CompositeCandidateCollection>(cfg.getParameter<edm::InputTag>("ditracks"))},
        leptons_ttracks_{consumes<TransientTrackCollection>(cfg.getParameter<edm::InputTag>("leptonTransientTracks"))},
        ditracks_ttracks_{consumes<TransientTrackCollection>(cfg.getParameter<edm::InputTag>("transientTracks"))},
        pu_tracks_(consumes<pat::CompositeCandidateCollection>(cfg.getParameter<edm::InputTag>("PUtracks"))),
        beamspot_{consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamSpot"))},
        dilepton_constraint_{cfg.getParameter<bool>("dileptonMassContraint")} {
    // output
    produces<pat::CompositeCandidateCollection>("SelectedBToTrkTrkMuMu");
    produces<pat::CompositeCandidateCollection>("SelectedTrkTrk");
  }

  ~BToTrkTrkLLBuilder() override {}

  void produce(edm::StreamID, edm::Event &, const edm::EventSetup &) const override;

private:
  const edm::ESGetToken<MagneticField, IdealMagneticFieldRecord> bFieldToken_;

  // selections
  const StringCutObjectSelector<pat::CompositeCandidate> pre_vtx_selection_;
  const StringCutObjectSelector<pat::CompositeCandidate> post_vtx_selection_;

  // inputs
  const edm::EDGetTokenT<pat::CompositeCandidateCollection> dileptons_;
  const edm::EDGetTokenT<pat::CompositeCandidateCollection> ditracks_;
  const edm::EDGetTokenT<TransientTrackCollection> leptons_ttracks_;
  const edm::EDGetTokenT<TransientTrackCollection> ditracks_ttracks_;
  const edm::EDGetTokenT<pat::CompositeCandidateCollection> pu_tracks_;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_;
  const bool dilepton_constraint_;
};

void BToTrkTrkLLBuilder::produce(edm::StreamID, edm::Event &evt, edm::EventSetup const &iSetup) const {
  // input
  edm::Handle<pat::CompositeCandidateCollection> dileptons;
  evt.getByToken(dileptons_, dileptons);
  edm::Handle<TransientTrackCollection> leptons_ttracks;
  evt.getByToken(leptons_ttracks_, leptons_ttracks);

  edm::Handle<pat::CompositeCandidateCollection> ditracks;
  evt.getByToken(ditracks_, ditracks);
  edm::Handle<TransientTrackCollection> ditracks_ttracks;
  evt.getByToken(ditracks_ttracks_, ditracks_ttracks);

  edm::Handle<pat::CompositeCandidateCollection> pu_tracks;
  evt.getByToken(pu_tracks_, pu_tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  evt.getByToken(beamspot_, beamspot);

  edm::ESHandle<MagneticField> fieldHandle;
  const auto &bField = iSetup.getData(bFieldToken_);
  AnalyticalImpactPointExtrapolator extrapolator(&bField);

  // output
  std::unique_ptr<pat::CompositeCandidateCollection> ret_val(new pat::CompositeCandidateCollection());
  std::unique_ptr<pat::CompositeCandidateCollection> ditrack_out(new pat::CompositeCandidateCollection());

  for (size_t ditracks_idx = 0; ditracks_idx < ditracks->size(); ++ditracks_idx) {
    // both k*,phi and lep pair already passed cuts; no need for more
    // preselection
    edm::Ptr<pat::CompositeCandidate> ditracks_ptr(ditracks, ditracks_idx);
    edm::Ptr<reco::Candidate> trk1_ptr = ditracks_ptr->userCand("trk1");
    edm::Ptr<reco::Candidate> trk2_ptr = ditracks_ptr->userCand("trk2");
    int trk1_idx = ditracks_ptr->userInt("trk1_idx");
    int trk2_idx = ditracks_ptr->userInt("trk2_idx");

    for (size_t ll_idx = 0; ll_idx < dileptons->size(); ++ll_idx) {
      edm::Ptr<pat::CompositeCandidate> ll_ptr(dileptons, ll_idx);
      edm::Ptr<reco::Candidate> l1_ptr = ll_ptr->userCand("l1");
      edm::Ptr<reco::Candidate> l2_ptr = ll_ptr->userCand("l2");
      int l1_idx = ll_ptr->userInt("l1_idx");
      int l2_idx = ll_ptr->userInt("l2_idx");

      if (l1_ptr->charge() * l2_ptr->charge() >= 0)
        continue;

      if (l1_ptr->charge() <= 0) {
        std::swap(l1_ptr, l2_ptr);
        std::swap(l1_idx, l2_idx);
      }

      if (trk1_ptr->charge() * trk2_ptr->charge() >= 0)
        continue;

      if (trk1_ptr->charge() <= 0) {
        std::swap(trk1_ptr, trk2_ptr);
        std::swap(trk1_idx, trk2_idx);
      }

      pat::CompositeCandidate cand;
      cand.setP4(ll_ptr->p4() + ditracks_ptr->p4());
      cand.setCharge(l1_ptr->charge() + l2_ptr->charge() + trk1_ptr->charge() + trk2_ptr->charge());

      cand.addUserCand("l1", l1_ptr);
      cand.addUserCand("l2", l2_ptr);
      cand.addUserCand("trk1", trk1_ptr);
      cand.addUserCand("trk2", trk2_ptr);
      cand.addUserCand("ditrack", ditracks_ptr);
      cand.addUserCand("dilepton", ll_ptr);

      cand.addUserInt("l1_idx", l1_idx);
      cand.addUserInt("l2_idx", l2_idx);
      cand.addUserInt("trk1_idx", trk1_idx);
      cand.addUserInt("trk2_idx", trk2_idx);
      //cand.addUserInt("ditrack_idx", ditracks_idx); this index corresponds to the ditrack collection.
      cand.addUserInt("ll_idx", ll_idx);

      int charge_l1 = l1_ptr->charge();
      int charge_l2 = l2_ptr->charge();
      int charge_trk1 = trk1_ptr->charge();
      int charge_trk2 = trk2_ptr->charge();

      cand.addUserInt("charge_l1", charge_l1);
      cand.addUserInt("charge_l2", charge_l2);
      cand.addUserInt("charge_trk1", charge_trk1);
      cand.addUserInt("charge_trk2", charge_trk2);

      auto lep1_p4 = l1_ptr->polarP4();
      auto lep2_p4 = l2_ptr->polarP4();
      lep1_p4.SetM(l1_ptr->mass());
      lep2_p4.SetM(l2_ptr->mass());

      auto trk1_p4 = trk1_ptr->polarP4();
      auto trk2_p4 = trk2_ptr->polarP4();

      trk1_p4.SetM(bph::K_MASS);
      trk2_p4.SetM(bph::K_MASS);
      cand.addUserFloat("unfitted_B_mass_KK", (trk1_p4 + trk2_p4 + lep1_p4 + lep2_p4).M());
      trk1_p4.SetM(bph::K_MASS);
      trk2_p4.SetM(bph::PI_MASS);
      cand.addUserFloat("unfitted_B_mass_Kpi", (trk1_p4 + trk2_p4 + lep1_p4 + lep2_p4).M());
      trk2_p4.SetM(bph::K_MASS);
      trk1_p4.SetM(bph::PI_MASS);
      cand.addUserFloat("unfitted_B_mass_piK", (trk1_p4 + trk2_p4 + lep1_p4 + lep2_p4).M());

      auto dr_info = bph::min_max_dr({l1_ptr, l2_ptr, trk1_ptr, trk2_ptr});
      cand.addUserFloat("min_dr", dr_info.first);
      cand.addUserFloat("max_dr", dr_info.second);

      if (!pre_vtx_selection_(cand))
        continue;

      KinVtxFitter fitter;
      try {
        fitter = KinVtxFitter({leptons_ttracks->at(l1_idx),
                               leptons_ttracks->at(l2_idx),
                               ditracks_ttracks->at(trk1_idx),
                               ditracks_ttracks->at(trk2_idx)},
                              {l1_ptr->mass(), l2_ptr->mass(), bph::K_MASS, bph::K_MASS},
                              {bph::LEP_SIGMA, bph::LEP_SIGMA, bph::K_SIGMA, bph::K_SIGMA});
      } catch (const VertexException &e) {
        edm::LogWarning("KinematicFit") << "BToTrkTrkLL - KK mass hypothesis: Skipping candidate due to fit failure: "
                                        << e.what();
        continue;
      }
      if (!fitter.success())
        continue;
      KinVtxFitter fitter_Kpi;
      try {
        fitter_Kpi = KinVtxFitter({leptons_ttracks->at(l1_idx),
                                   leptons_ttracks->at(l2_idx),
                                   ditracks_ttracks->at(trk1_idx),
                                   ditracks_ttracks->at(trk2_idx)},
                                  {l1_ptr->mass(), l2_ptr->mass(), bph::K_MASS, bph::PI_MASS},
                                  {bph::LEP_SIGMA, bph::LEP_SIGMA, bph::K_SIGMA, bph::K_SIGMA});
      } catch (const VertexException &e) {
        edm::LogWarning("KinematicFit") << "BToTrkTrkLL - Kpi mass hypothesis: Skipping candidate due to fit failure: "
                                        << e.what();
        continue;
      }
      if (!fitter_Kpi.success())
        continue;
      KinVtxFitter fitter_piK;
      try {
        fitter_piK = KinVtxFitter({leptons_ttracks->at(l1_idx),
                                   leptons_ttracks->at(l2_idx),
                                   ditracks_ttracks->at(trk1_idx),
                                   ditracks_ttracks->at(trk2_idx)},
                                  {l1_ptr->mass(), l2_ptr->mass(), bph::PI_MASS, bph::K_MASS},
                                  {bph::LEP_SIGMA, bph::LEP_SIGMA, bph::K_SIGMA, bph::K_SIGMA});
      } catch (const VertexException &e) {
        edm::LogWarning("KinematicFit") << "BToTrkTrkLL - piK mass hypothesis: Skipping candidate due to fit failure: "
                                        << e.what();
        continue;
      }
      if (!fitter_piK.success())
        continue;

      cand.setVertex(reco::Candidate::Point(fitter.fitted_vtx().x(), fitter.fitted_vtx().y(), fitter.fitted_vtx().z()));

      cand.addUserFloat("sv_chi2", fitter.chi2());
      cand.addUserFloat("sv_ndof", fitter.dof());
      cand.addUserFloat("sv_prob", fitter.prob());

      // refitted kinematic vars
      cand.addUserFloat("fitted_ditrack_mass_KK", (fitter.daughter_p4(2) + fitter.daughter_p4(3)).mass());
      cand.addUserFloat("fitted_ditrack_mass_Kpi", (fitter_Kpi.daughter_p4(2) + fitter_Kpi.daughter_p4(3)).mass());
      cand.addUserFloat("fitted_ditrack_mass_piK", (fitter_piK.daughter_p4(2) + fitter_piK.daughter_p4(3)).mass());
      cand.addUserFloat("fitted_massErr_KK", sqrt(fitter.fitted_candidate().kinematicParametersError().matrix()(6, 6)));
      cand.addUserFloat("fitted_massErr_Kpi", sqrt(fitter_Kpi.fitted_candidate().kinematicParametersError().matrix()(6, 6)));
      cand.addUserFloat("fitted_massErr_piK", sqrt(fitter_piK.fitted_candidate().kinematicParametersError().matrix()(6, 6)));
      cand.addUserFloat("fitted_mll", (fitter.daughter_p4(0) + fitter.daughter_p4(1)).mass());

      auto fit_p4 = fitter.fitted_p4();
      cand.addUserFloat("fitted_pt", fit_p4.pt());
      cand.addUserFloat("fitted_eta", fit_p4.eta());
      cand.addUserFloat("fitted_phi", fit_p4.phi());

      cand.addUserFloat("fitted_mass_KK", fit_p4.mass());
      cand.addUserFloat("fitted_mass_Kpi", fitter_Kpi.fitted_p4().mass());
      cand.addUserFloat("fitted_mass_piK", fitter_piK.fitted_p4().mass());

      float kstar_mass = -99.0;
      float kstarbar_mass = -99.0;

      double mass_kpi = cand.userFloat("fitted_ditrack_mass_Kpi");
      double mass_piK = cand.userFloat("fitted_ditrack_mass_piK");

      double diff_kpi = std::abs(mass_kpi - bph::KSTAR_PDG_MASS);
      double diff_piK = std::abs(mass_piK - bph::KSTAR_PDG_MASS);

      if (diff_kpi < diff_piK) {
        kstar_mass = mass_kpi;
        kstarbar_mass = mass_piK;
      } else {
        kstar_mass = mass_piK;
        kstarbar_mass = mass_kpi;
      }
      cand.addUserFloat("Kstar_mass", kstar_mass);
      cand.addUserFloat("Kstarbar_mass", kstarbar_mass);

      cand.addUserFloat("cos_theta_2D", bph::cos_theta_2D(fitter, *beamspot, cand.p4()));
      cand.addUserFloat("fitted_cos_theta_2D", bph::cos_theta_2D(fitter, *beamspot, fit_p4));

      auto lxy = bph::l_xy(fitter, *beamspot);
      cand.addUserFloat("l_xy", lxy.value());
      cand.addUserFloat("l_xy_unc", lxy.error());
      cand.addUserFloat("l_xy_sig", lxy.value()/lxy.error());
      
      TrajectoryStateOnSurface tsos1 =
          extrapolator.extrapolate(ditracks_ttracks->at(trk1_idx).impactPointState(), fitter.fitted_vtx());
      std::pair<bool, Measurement1D> cur2DIP1_trk1 = 
          bph::signedTransverseImpactParameter(tsos1, fitter.fitted_refvtx(), *beamspot);
      cand.addUserFloat("trk1_svip2d", cur2DIP1_trk1.second.value()); 
      cand.addUserFloat("trk1_svip2d_err", cur2DIP1_trk1.second.error());
      cand.addUserFloat("trk1_svip2d_sig", std::abs(cur2DIP1_trk1.second.value()/cur2DIP1_trk1.second.error()));

      TrajectoryStateOnSurface tsos2 =
          extrapolator.extrapolate(ditracks_ttracks->at(trk2_idx).impactPointState(), fitter.fitted_vtx());
      std::pair<bool, Measurement1D> cur2DIP2_trk2 = 
          bph::signedTransverseImpactParameter(tsos2, fitter.fitted_refvtx(), *beamspot);
      cand.addUserFloat("trk2_svip2d", cur2DIP2_trk2.second.value()); 
      cand.addUserFloat("trk2_svip2d_err", cur2DIP2_trk2.second.error()); 
      cand.addUserFloat("trk2_svip2d_sig", std::abs(cur2DIP2_trk2.second.value()/cur2DIP2_trk2.second.error()));

      if (!post_vtx_selection_(cand))
        continue;

      const reco::BeamSpot &beamSpot = *beamspot;
      TrajectoryStateClosestToPoint theDCAXBS = fitter.fitted_candidate_ttrk().trajectoryStateClosestToPoint(
          GlobalPoint(beamSpot.position().x(), beamSpot.position().y(), beamSpot.position().z()));
      double DCAB0BS = -99.;
      double DCAB0BSErr = -99.;

      if (theDCAXBS.isValid() == true) {
        DCAB0BS = theDCAXBS.perigeeParameters().transverseImpactParameter();
        DCAB0BSErr = theDCAXBS.perigeeError().transverseImpactParameterError();
      }
      cand.addUserFloat("dca", DCAB0BS);
      cand.addUserFloat("dcaErr", DCAB0BSErr);
      cand.addUserFloat("dcaSig", DCAB0BS/DCAB0BSErr);

      cand.addUserFloat("vtx_x", cand.vx());
      cand.addUserFloat("vtx_y", cand.vy());
      cand.addUserFloat("vtx_z", cand.vz());

      const auto &covMatrix = fitter.fitted_vtx_uncertainty();
      cand.addUserFloat("vtx_cxx", covMatrix.cxx());
      cand.addUserFloat("vtx_cyy", covMatrix.cyy());
      cand.addUserFloat("vtx_czz", covMatrix.czz());
      cand.addUserFloat("vtx_cyx", covMatrix.cyx());
      cand.addUserFloat("vtx_czx", covMatrix.czx());
      cand.addUserFloat("vtx_czy", covMatrix.czy());

      std::vector<std::string> dnames{"l1", "l2", "trk1", "trk2"};

      for (size_t idaughter = 0; idaughter < dnames.size(); idaughter++) {
        cand.addUserFloat("fitted_" + dnames[idaughter] + "_pt", fitter.daughter_p4(idaughter).pt());
        cand.addUserFloat("fitted_" + dnames[idaughter] + "_eta", fitter.daughter_p4(idaughter).eta());
        cand.addUserFloat("fitted_" + dnames[idaughter] + "_phi", fitter.daughter_p4(idaughter).phi());
      }
      
      // compute isolation
      std::vector<float> isos = bph::TrackerIsolation(pu_tracks, cand, dnames);
      for (size_t idaughter = 0; idaughter < dnames.size(); idaughter++) {
        cand.addUserFloat(dnames[idaughter] + "_iso04", isos[idaughter]);
      }

      ret_val->emplace_back(cand);
      ditrack_out->emplace_back(*ditracks_ptr);

    }  
  } 

  evt.put(std::move(ret_val), "SelectedBToTrkTrkMuMu");
  evt.put(std::move(ditrack_out), "SelectedTrkTrk");
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(BToTrkTrkLLBuilder);
