import uproot
import awkward as ak
import argparse
import sys
import os
import traceback

def main():
    # =========================================================
    # 1. CONFIGURAÇÃO DE PARÂMETROS PARA O CONDOR (argparse)
    # =========================================================
    parser = argparse.ArgumentParser(description="Script de filtragem de NanoAOD para o Condor")
    parser.add_argument("--input_list", required=True, help="Arquivo .txt com lista de arquivos ROOT ou caminho direto")
    parser.add_argument("--output", required=True, help="Nome do arquivo ROOT de saída")
    parser.add_argument("--process_mode", required=True, choices=["data", "mc"], help="'data' para dados reais, 'mc' para simulação")
    args = parser.parse_args()

    is_mc = (args.process_mode.lower() == "mc")

    files_to_process = []
    if args.input_list.endswith(".txt"):
        with open(args.input_list) as f:
            for line in f:
                link = line.strip()
                if link and not link.startswith("#"):
                    files_to_process.append(link)
    else:
        files_to_process = [args.input_list]

    if not files_to_process:
        print("ERRO: Lista de arquivos vazia.")
        sys.exit(1)

    try:
        print(f"Modo: {args.process_mode.upper()} | Arquivos a processar: {len(files_to_process)}")
        print(f"Iniciando leitura e filtragem em chunks...")

        prefixes = ("BToTrkTrkMuMu_", "DiTrack_", "BPH", "Track_", "MuMu_", "HLT_", "L1_")
        
        first_file_tree = f"{files_to_process[0]}:Events"
        with uproot.open(first_file_tree) as test_tree:
            available_branches = test_tree.keys()
        
        keep_cols_set = {col for col in available_branches if col.startswith(prefixes) or col in ["run", "event", "luminosityBlock"]}
        if is_mc:
            keep_cols_set.update({col for col in available_branches if col.startswith(("Pileup_", "genWeight", "GenPart_", "BPHGenPart_"))})
        
        keep_cols = list(keep_cols_set)
        compression = uproot.LZMA(4) 
        paths_with_tree = [f"{path}:Events" for path in files_to_process]
        
        # =========================================================
        # 2. PROCESSAMENTO EM CHUNKS (iterate)
        # =========================================================
        with uproot.recreate(args.output, compression=compression) as out_file:
            is_first_chunk = True
            
            for batch in uproot.iterate(paths_with_tree, filter_name=keep_cols, step_size="100 MB"):
                
                ll_idx = batch["BToTrkTrkMuMu_ll_idx"]
                l1_idx = batch["BToTrkTrkMuMu_l1_idx"]
                l2_idx = batch["BToTrkTrkMuMu_l2_idx"]
                trk1_idx = batch["BToTrkTrkMuMu_trk1_idx"]
                trk2_idx = batch["BToTrkTrkMuMu_trk2_idx"]

                mask_mumu = (
                    (batch["MuMu_pt"][ll_idx] > 6.9) &
                    (batch["MuMu_svprob"][ll_idx] > 0.1) &
                    (batch["MuMu_l_xy"][ll_idx] / batch["MuMu_l_xy_unc"][ll_idx] > 3.0) &
                    (batch["MuMu_fit_cos2D"][ll_idx] > 0.9)
                )

                mask_b0 = (
                    (batch["BToTrkTrkMuMu_fit_l1_pt"] > 4.0) &
                    (batch["BToTrkTrkMuMu_fit_l2_pt"] > 4.0) &
                    (batch["BToTrkTrkMuMu_svprob"] > 0.01) &
                    (batch["BToTrkTrkMuMu_fit_trk1_pt"] > 0.8) &
                    (batch["BToTrkTrkMuMu_fit_trk2_pt"] > 0.8)
                )

                final_mask = mask_mumu & mask_b0

                dict_filtrado = {}

                # 1. Global
                for branch in ["run", "event", "luminosityBlock"]:
                    if branch in batch.fields:
                        dict_filtrado[branch] = batch[branch]

                # 2. B0 e DiTrack
                for branch in [b for b in batch.fields if b.startswith(("BToTrkTrkMuMu_", "DiTrack_"))]:
                    dict_filtrado[branch] = batch[branch][final_mask]

                # 3. MuMu
                for branch in [b for b in batch.fields if b.startswith("MuMu_")]:
                    dict_filtrado[branch] = batch[branch][ll_idx][final_mask]

                # 4. Track -> Trk1 e Trk2
                for branch in [b for b in batch.fields if b.startswith("Track_")]:
                    dict_filtrado[branch.replace("Track_", "Trk1_")] = batch[branch][trk1_idx][final_mask]
                    dict_filtrado[branch.replace("Track_", "Trk2_")] = batch[branch][trk2_idx][final_mask]

                # 5. BPHMuon -> Muon1 e Muon2
                for branch in [b for b in batch.fields if b.startswith("BPHMuon_")]:
                    dict_filtrado[branch.replace("BPHMuon_", "BPH_1Muon_")] = batch[branch][l1_idx][final_mask]
                    dict_filtrado[branch.replace("BPHMuon_", "BPH_2Muon_")] = batch[branch][l2_idx][final_mask]

                # 6. Triggers e Pesos MC (Broadcast)
                target_branches = [b for b in batch.fields if b.startswith("HLT_DoubleMu4_")]
                if is_mc:
                    target_branches += [b for b in batch.fields if b.startswith(("Pileup_", "genWeight"))]
                
                for branch in target_branches:
                    expanded = ak.broadcast_arrays(batch[branch], final_mask)[0]    
                    dict_filtrado[branch] = expanded[final_mask]

                # --- CORREÇÃO DE TIPO (UINT32 -> INT32) ---
                # Essencial para compatibilidade com NumPy 1.x na LXPLUS
                for branch in dict_filtrado:
                    if "uint32" in str(ak.type(dict_filtrado[branch])):
                        dict_filtrado[branch] = ak.values_astype(dict_filtrado[branch], "int32")

                # Agrupamento e Máscara de Evento
                B_candidates_clean = ak.zip(dict_filtrado)
                event_mask = ak.num(B_candidates_clean["BToTrkTrkMuMu_fit_pt"]) > 0
                
                if not ak.any(event_mask):
                    continue
                
                B_candidates_validos = B_candidates_clean[event_mask]
                output_dict = {f: B_candidates_validos[f] for f in B_candidates_validos.fields}
                
                if is_mc:
                    gen_branches = [b for b in batch.fields if b.startswith("BPHGenPart_")]
                    for branch in gen_branches:
                        output_dict[branch] = batch[branch][event_mask]

                # =========================================================
                # 3. SALVANDO O CHUNK COM TIPAGEM EXPLÍCITA
                # =========================================================
                if is_first_chunk:
                    # CORREÇÃO: Passando o esquema de tipos explicitamente para o mktree
                    branch_types = {name: ak.type(array) for name, array in output_dict.items()}
                    out_file.mktree("Events", branch_types)
                    out_file["Events"].extend(output_dict)
                    is_first_chunk = False
                else:
                    out_file["Events"].extend(output_dict)

        print(f"Processo concluído com sucesso! Salvo em: {args.output} 🚀")

    except Exception as e:
        print(f"Erro fatal: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()