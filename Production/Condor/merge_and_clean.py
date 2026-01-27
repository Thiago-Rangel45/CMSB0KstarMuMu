import os
import subprocess
import glob
import sys

# ================= CONFIGURAÇÃO =================
# Caminho onde estão os arquivos parciais (no EOS)
INPUT_DIR = "/eos/user/t/tdeandra/skim_outputs/data/"

# Padrão dos nomes dos arquivos parciais (para não apagar coisas erradas)
# O * serve como "qualquer coisa" (ex: MC_Skim_123_0.root)
FILE_PATTERN = "Data_Skim_*.root"

# Nome do arquivo final UNIFICADO
OUTPUT_FILENAME = "Data_background_merged.root"

# O arquivo final será salvo na MESMA pasta, mas com nome diferente
FINAL_PATH = os.path.join(INPUT_DIR, OUTPUT_FILENAME)

# ================= EXECUÇÃO =================
def main():
    # 1. Encontrar todos os arquivos parciais
    search_path = os.path.join(INPUT_DIR, FILE_PATTERN)
    files_to_merge = glob.glob(search_path)
    
    # Ordenar para garantir consistência
    files_to_merge.sort()

    if len(files_to_merge) == 0:
        print(f"[ERRO] Nenhum arquivo encontrado em: {search_path}")
        sys.exit(1)

    print(f"Encontrados {len(files_to_merge)} arquivos parciais.")
    print(f"Destino final: {FINAL_PATH}")
    
    # 2. Montar o comando hadd
    # -f força a sobreescrita se o arquivo já existir
    # -k pula arquivos corrompidos (opcional, mas seguro)
    cmd = ["hadd", "-f", "-k", FINAL_PATH] + files_to_merge

    print("-" * 40)
    print("Iniciando o 'hadd' (isso pode demorar alguns minutos)...")
    
    try:
        # Executa o comando no terminal
        subprocess.run(cmd, check=True)
        print("-" * 40)
        print("✔ MERGE REALIZADO COM SUCESSO!")
        
    except subprocess.CalledProcessError:
        print("❌ [ERRO] O comando hadd falhou.")
        print("Nenhum arquivo será apagado. Verifique os logs.")
        sys.exit(1)

    # 3. Limpeza (Só acontece se o passo anterior não der erro)
    print("Iniciando limpeza dos arquivos parciais...")
    
    deleted_count = 0
    for file_path in files_to_merge:
        try:
            os.remove(file_path)
            deleted_count += 1
        except OSError as e:
            print(f"Erro ao apagar {file_path}: {e}")

    print("-" * 40)
    print(f"LIMPEZA CONCLUÍDA: {deleted_count} arquivos apagados.")
    print(f"Arquivo final disponível em: {FINAL_PATH}")

if __name__ == "__main__":
    main()