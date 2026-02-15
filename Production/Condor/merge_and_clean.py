import os
import subprocess
import glob
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, help="dados, jpsi, bu, ou nonressonat")
    parser.add_argument("--output", required=True, help="Nome do arquivo final (ex: Bu_merged.root)")
    args = parser.parse_args()

    # Caminho base baseado no modo
    INPUT_DIR = f"/eos/user/t/tdeandra/skim_outputs/{args.mode}/"
    
    # Define o padrão de busca baseado no nome dado no condor.sub
    if args.mode == "dados":
        FILE_PATTERN = "Data_Skim_*.root"
    elif args.mode == "jpsi":
        FILE_PATTERN = "MC_JPsi_Skim_*.root"
    elif args.mode == "bu":
        FILE_PATTERN = "MC_Bu_Skim_*.root"
    else:
        FILE_PATTERN = "MC_Skim_*.root"

    FINAL_PATH = os.path.join(INPUT_DIR, args.output)

    # 1. Encontrar todos os arquivos parciais
    search_path = os.path.join(INPUT_DIR, FILE_PATTERN)
    files_to_merge = glob.glob(search_path)
    files_to_merge.sort()

    if len(files_to_merge) == 0:
        print(f"[ERRO] Nenhum arquivo encontrado em: {search_path}")
        sys.exit(1)

    print(f"Encontrados {len(files_to_merge)} arquivos em '{args.mode}'.")
    
    # 2. Comando hadd
    cmd = ["hadd", "-f", "-k", FINAL_PATH] + files_to_merge

    try:
        subprocess.run(cmd, check=True)
        print("✔ MERGE REALIZADO COM SUCESSO!")
        
        # 3. Limpeza
        for file_path in files_to_merge:
            os.remove(file_path)
        print(f"LIMPEZA CONCLUÍDA: {len(files_to_merge)} arquivos apagados.")

    except subprocess.CalledProcessError:
        print("❌ [ERRO] O comando hadd falhou.")
        sys.exit(1)

if __name__ == "__main__":
    main()