import ROOT
import sys
import argparse
import os

# Otimização: Multithreading e Batch Mode
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)

def get_cut_string():
    """
    Retorna APENAS cortes de qualidade (Trigger, Qualidade dos Múons, Cinemática Básica).
    NENHUM corte de janela de massa (MuMu ou B) é aplicado aqui.
    """
    quality_cuts = """
    MuMu_pt_idx > 6.9 &&
    MuMu_svprob_idx > 0.1 &&
    (MuMu_l_xy_idx / MuMu_l_xy_unc_idx) > 3 &&
    MuMu_fit_cos2D_idx > 0.9 &&
    
    abs(BToTrkTrkMuMu_fit_ditrack_mass_Kpi - 0.896) < abs(BToTrkTrkMuMu_fit_ditrack_mass_piK - 0.896) &&
    
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
    return quality_cuts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_list", required=True, help="Arquivo .txt com lista de inputs")
    parser.add_argument("--output", required=True, help="Nome do arquivo de saída .root")
    parser.add_argument("--process_mode", required=False, default="check", help="Apenas para log (data/mc)")
    args = parser.parse_args()

    # Ler lista de arquivos
    if not os.path.exists(args.input_list):
        sys.exit(f"Erro: Arquivo de lista {args.input_list} não encontrado.")

    with open(args.input_list, 'r') as f:
        file_list = [line.strip() for line in f if line.strip()]

    if not file_list:
        sys.exit("Erro: Lista de arquivos vazia.")

    print(f"Processando {len(file_list)} arquivos. Modo: {args.process_mode}")

    # Inicializa RDataFrame
    df = ROOT.RDataFrame("Events", file_list)

    # --- Definição de Variáveis (Features) ---
    mumu_features = ["MuMu_mass", "MuMu_pt", "MuMu_eta", "MuMu_phi", "MuMu_svprob", "MuMu_l_xy", "MuMu_l_xy_unc", "MuMu_fit_cos2D"]
    
    for item in mumu_features:
        df = df.Define(f"{item}_idx", f"ROOT::VecOps::Take({item}, BToTrkTrkMuMu_ll_idx)")

    df = df.Define("Muon_softMvaRun3_l1_idx", "ROOT::VecOps::Take(Muon_softMvaRun3, BToTrkTrkMuMu_l1_idx)") \
           .Define("Muon_softMvaRun3_l2_idx", "ROOT::VecOps::Take(Muon_softMvaRun3, BToTrkTrkMuMu_l2_idx)")

    df = df.Define("BToTrkTrkMuMu_l_xy_sig", "BToTrkTrkMuMu_l_xy / BToTrkTrkMuMu_l_xy_unc") \
           .Define("BToTrkTrkMuMu_dca_sig", "BToTrkTrkMuMu_dca / BToTrkTrkMuMu_dcaErr") \
           .Define("BToTrkTrkMuMu_trk1_dca_sig", "BToTrkTrkMuMu_trk1_dca / BToTrkTrkMuMu_trk1_dcaErr") \
           .Define("BToTrkTrkMuMu_trk2_dca_sig", "BToTrkTrkMuMu_trk2_dca / BToTrkTrkMuMu_trk2_dcaErr")

    b_features = [
        "BToTrkTrkMuMu_fit_ditrack_mass_Kpi", "BToTrkTrkMuMu_fit_ditrack_mass_piK",
        "BToTrkTrkMuMu_svprob", "BToTrkTrkMuMu_l_xy", "BToTrkTrkMuMu_l_xy_unc",
        "BToTrkTrkMuMu_fit_cos2D", "BToTrkTrkMuMu_dca", "BToTrkTrkMuMu_dcaErr",
        "BToTrkTrkMuMu_trk1_dca", "BToTrkTrkMuMu_trk1_dcaErr",
        "BToTrkTrkMuMu_trk2_dca", "BToTrkTrkMuMu_trk2_dcaErr",
        "BToTrkTrkMuMu_sum_iso04", "BToTrkTrkMuMu_fit_mass_Kpi",
        "BToTrkTrkMuMu_fit_pt", "BToTrkTrkMuMu_fit_eta", "BToTrkTrkMuMu_fit_phi",
        "BToTrkTrkMuMu_l_xy_sig", "BToTrkTrkMuMu_dca_sig",
        "BToTrkTrkMuMu_trk1_dca_sig", "BToTrkTrkMuMu_trk2_dca_sig",
        "BToTrkTrkMuMu_cos_theta_l", "BToTrkTrkMuMu_cos_theta_k",
        "BToTrkTrkMuMu_phi_angle"
    ]

    features = [f"{item}_idx" for item in mumu_features] + \
               ["Muon_softMvaRun3_l1_idx", "Muon_softMvaRun3_l2_idx"] + b_features

    # --- Aplicação dos Cortes ---
    cut_expression = get_cut_string()
    df = df.Define("pass_cut", cut_expression)

    # Cria colunas filtradas
    for item in features:
        df = df.Define(f"{item}_good", f"{item}[pass_cut]")
    
    # Filtro: Salva evento se houver pelo menos 1 candidato válido
    df = df.Filter("BToTrkTrkMuMu_fit_ditrack_mass_Kpi_good.size() > 0")

    features_to_save = [f"{item}_good" for item in features]

    # --- Snapshot ---
    # CORREÇÃO: Usando o valor inteiro 4 para kLZ4 para evitar AttributeError
    opts = ROOT.RDF.RSnapshotOptions()
    opts.fCompressionAlgorithm = 4 # kLZ4
    opts.fCompressionLevel = 4
    
    print(f"Salvando output em: {args.output}")
    df.Snapshot("tree_ML", args.output, features_to_save, opts)
    print("Concluído.")

if __name__ == "__main__":
    main()