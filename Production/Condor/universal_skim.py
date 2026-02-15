#!/usr/bin/env python3

import ROOT
import sys
import argparse

# Multithreading (ajuste o número se quiser fixar)
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)


def get_cut_string():
    return """
    MuMu_pt_idx > 6.9 &&
    MuMu_svprob_idx > 0.1 &&
    (MuMu_l_xy_idx / MuMu_l_xy_unc_idx) > 3 &&
    MuMu_fit_cos2D_idx > 0.9 &&

    abs(BToTrkTrkMuMu_fit_ditrack_mass_Kpi - 0.896) <
    abs(BToTrkTrkMuMu_fit_ditrack_mass_piK - 0.896) &&

    BToTrkTrkMuMu_fit_l1_pt > 4 &&
    abs(BToTrkTrkMuMu_fit_l1_eta) < 2.4 &&
    BToTrkTrkMuMu_fit_l2_pt > 4 &&
    abs(BToTrkTrkMuMu_fit_l2_eta) < 2.4 &&
    BToTrkTrkMuMu_fit_trk1_pt > 0.8 &&
    abs(BToTrkTrkMuMu_fit_trk1_eta) < 2.4 &&

    HLT_DoubleMu4_LowMass_Displaced == 1 &&
    Muon_softMvaRun3_l1_idx > 0.74 &&
    Muon_softMvaRun3_l2_idx > 0.74 &&

    (BToTrkTrkMuMu_fit_ditrack_mass_KK > 1.035)
    """


def main():

    parser = argparse.ArgumentParser()
    # Alterado para --input_list para coincidir com seu job.sh
    parser.add_argument("--input_list", required=True,
                        help="Arquivo ROOT ou txt com lista de ROOTs")
    parser.add_argument("--output", required=True)
    # Removido o choices=["data", "mc"] para aceitar "dados", "bu", "jpsi", etc.
    parser.add_argument("--process_mode", required=True)
    args = parser.parse_args()

    print("Inicializando RDataFrame...")

    # ===============================
    # Leitura de múltiplos arquivos
    # ===============================
    if args.input_list.endswith(".txt"):
        with open(args.input_list) as f:
            file_list = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

        if len(file_list) == 0:
            print("ERRO: arquivo txt está vazio.")
            sys.exit(1)

        print(f"{len(file_list)} arquivos encontrados no txt.")
        df = ROOT.RDataFrame("Events", file_list)
    else:
        df = ROOT.RDataFrame("Events", args.input_list)

    # ===============================
    # Pegando todas as colunas
    # ===============================
    all_columns = list(df.GetColumnNames())

    # ===============================
    # Criando colunas indexadas MuMu
    # ===============================
    mumu_columns = [col for col in all_columns if col.startswith("MuMu_")]
    for col in mumu_columns:
        df = df.Define(f"{col}_idx", f"ROOT::VecOps::Take({col}, BToTrkTrkMuMu_ll_idx)")

    df = df.Define("Muon_softMvaRun3_l1_idx", "ROOT::VecOps::Take(Muon_softMvaRun3, BToTrkTrkMuMu_l1_idx)")
    df = df.Define("Muon_softMvaRun3_l2_idx", "ROOT::VecOps::Take(Muon_softMvaRun3, BToTrkTrkMuMu_l2_idx)")
    df = df.Define("pass_cut", get_cut_string())

    # ===============================
    # BToTrkTrkMuMu
    # ===============================
    BToTrk_columns = [col for col in all_columns if col.startswith("BToTrkTrkMuMu_")]
    for item in BToTrk_columns:
        df = df.Define(f"{item}_good", f"{item}[pass_cut]")

    # ===============================
    # DiTrack
    # ===============================
    DiTrack_columns = [col for col in all_columns if col.startswith("DiTrack_")]
    for item in DiTrack_columns:
        df = df.Define(f"{item}_good", f"{item}[pass_cut]")

    # ===============================
    # MuMu filtrado
    # ===============================
    for col in mumu_columns:
        df = df.Define(f"{col}_good", f"{col}_idx[pass_cut]")

    # ===============================
    # Muons
    # ===============================
    Muon_columns = [col for col in all_columns if col.startswith("Muon_")]
    for col in Muon_columns:
        df = df.Define(f"{col}_l1", f"ROOT::VecOps::Take({col}, BToTrkTrkMuMu_l1_idx)")
        df = df.Define(f"{col}_l2", f"ROOT::VecOps::Take({col}, BToTrkTrkMuMu_l2_idx)")
        df = df.Define(f"{col}_l1_good", f"{col}_l1[pass_cut]")
        df = df.Define(f"{col}_l2_good", f"{col}_l2[pass_cut]")

    # ===============================
    # Tracks
    # ===============================
    Track_columns = [col for col in all_columns if col.startswith("Track_")]
    for col in Track_columns:
        df = df.Define(f"{col}_t1", f"ROOT::VecOps::Take({col}, BToTrkTrkMuMu_trk1_idx)")
        df = df.Define(f"{col}_t2", f"ROOT::VecOps::Take({col}, BToTrkTrkMuMu_trk2_idx)")
        df = df.Define(f"{col}_trk1_good", f"{col}_t1[pass_cut]")
        df = df.Define(f"{col}_trk2_good", f"{col}_t2[pass_cut]")

    # ===============================
    # Trigger
    # ===============================
    Trigger_columns = [col for col in all_columns if col.startswith("HLT_DoubleMu4_")]

    # ===============================
    # MC-only branches
    # ===============================
    # AJUSTE AQUI: Se for diferente de "dados", carrega as colunas de MC
    if args.process_mode != "dados":
        Pileup_columns = [col for col in all_columns if col.startswith("Pileup_")]
        GenPart_columns = [col for col in all_columns if "GenPart" in col]
    else:
        Pileup_columns = []
        GenPart_columns = []

    # ===============================
    # Mantém apenas eventos com candidato
    # ===============================
    df = df.Filter("BToTrkTrkMuMu_fit_ditrack_mass_Kpi_good.size() > 0")

    final_columns = list(df.GetColumnNames())
    features_to_save = [col for col in final_columns if col.endswith("_good")]
    features_to_save += Trigger_columns

    for g in ["run", "luminosityBlock", "event"]:
        if g in final_columns:
            features_to_save.append(g)

    features_to_save += Pileup_columns
    features_to_save += GenPart_columns

    # Remove duplicatas
    features_to_save = list(set(features_to_save))

    # ===============================
    # Snapshot
    # ===============================
    opts = ROOT.RDF.RSnapshotOptions()
    opts.fCompressionAlgorithm = 4
    opts.fCompressionLevel = 4

    print(f"Salvando output em: {args.output}")
    df.Snapshot("tree_ML", args.output, features_to_save, opts)

    print("Concluído.")


if __name__ == "__main__":
    main()