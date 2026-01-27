import subprocess
import os

# ================= CONFIGURAÇÃO =================
REDIRECTOR = "xrootd2.hepgrid.uerj.br:1094"
ROOT_PREFIX = f"root://{REDIRECTOR}/"

# 1. Diretórios de DADOS
DATA_DIRS = [
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass0/BPH_NanoAOD_Run2022C/251125_201418/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass1/BPH_NanoAOD_Run2022C/251214_122305/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass2/BPH_NanoAOD_Run2022C/251214_122434/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass3/BPH_NanoAOD_Run2022C/251125_201643/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass4/BPH_NanoAOD_Run2022C/251125_201708/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass5/BPH_NanoAOD_Run2022C/251125_201733/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass6/BPH_NanoAOD_Run2022C/251125_201756/0000/",
    "/cms/store/user/tdeandra/ParkingDoubleMuonLowMass7/BPH_NanoAOD_Run2022C/251125_201902/0000/"
]

# 2. Diretório de MC (Genérico / Anterior)
MC_DIRS = [
    "/cms/store/user/tdeandra/BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_NanoAOD_Run2022C_MC/251121_015314/0000/"
]

# 3. NOVO Diretório de MC (JPsi Kstar)
MC_JPSI_DIRS = [
    "/cms/store/user/tdeandra/BdToJpsiKstar_BMuonFilter_SoftQCDnonD_TuneCP5_13p6TeV_pythia8-evtgen/BPH_NanoAOD_Run2022C_MC/251219_000717/0000/"
]

# Quantos arquivos ROOT processar por Job do Condor?
FILES_PER_JOB = 50

# ================= FUNÇÕES =================

def get_files_from_grid(dir_list):
    """
    Usa xrdfs ls para listar arquivos remotos e retorna lista limpa.
    """
    found_files = []
    print(f"Varrendo {len(dir_list)} diretórios no Grid...")

    for i, raw_dir in enumerate(dir_list):
        # Ajuste: O XRootD geralmente espera /store, removemos /cms se existir
        search_dir = raw_dir.replace("/cms/store", "/store")
        
        print(f"   [{i+1}/{len(dir_list)}] Listando: {search_dir}")
        
        # Comando xrdfs ls
        cmd = ["xrdfs", REDIRECTOR, "ls", search_dir]
        
        try:
            result = subprocess.check_output(cmd, text=True)
            lines = result.splitlines()
            
            count_local = 0
            for line in lines:
                if line.endswith(".root"):
                    # Garante o caminho completo com protocolo e ajusta o path
                    clean_path = line.strip()
                    if not clean_path.startswith("/"):
                        clean_path = "/" + clean_path
                        
                    full_path = f"{ROOT_PREFIX}{clean_path}"
                    found_files.append(full_path)
                    count_local += 1
            
            print(f"      -> Encontrados {count_local} arquivos.")
            
        except subprocess.CalledProcessError as e:
            print(f"      [ERRO] Falha ao acessar {search_dir}. Erro: {e}")
            
    return sorted(found_files)

def create_job_lists(file_list, output_folder):
    """
    Divide a lista total em pequenos arquivos de texto e cria o índice para o Condor.
    """
    if not file_list:
        print(f"[AVISO] Lista vazia para {output_folder}. Nada criado.")
        return

    # Cria pasta se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    master_list_name = os.path.join(output_folder, "list_files.txt")
    
    print(f"Gerando chunks em '{output_folder}'...")
    
    with open(master_list_name, "w") as f_master:
        # Loop com passo de FILES_PER_JOB
        chunk_counter = 0
        for i in range(0, len(file_list), FILES_PER_JOB):
            chunk = file_list[i : i + FILES_PER_JOB]
            
            # Nome do arquivo pequeno: input_0.txt, input_1.txt...
            chunk_filename = os.path.join(output_folder, f"input_{chunk_counter}.txt")
            
            # Escreve os N arquivos ROOT neste arquivo texto
            with open(chunk_filename, "w") as f_chunk:
                for root_file in chunk:
                    f_chunk.write(root_file + "\n")
            
            # Escreve o caminho do arquivo texto na lista mestra
            f_master.write(chunk_filename + "\n")
            
            chunk_counter += 1

    print(f"✔ Sucesso! Criados {chunk_counter} jobs para {len(file_list)} arquivos.")
    print(f"  Lista mestre: {master_list_name}")
    print("-" * 40)

# ================= EXECUÇÃO =================

if __name__ == "__main__":
    print("=== INICIANDO GERAÇÃO DE LISTAS PARA O CONDOR ===")
    
    # 1. Processar DADOS
    print("\n>>> DATASET: DADOS")
    data_files = get_files_from_grid(DATA_DIRS)
    create_job_lists(data_files, "file_lists_data")
    
    # 2. Processar MC (Antigo)
    print("\n>>> DATASET: MONTE CARLO (Genérico)")
    mc_files = get_files_from_grid(MC_DIRS)
    create_job_lists(mc_files, "file_lists_mc")

    # 3. Processar NOVO MC (JPsi)
    print("\n>>> DATASET: MONTE CARLO (JPsi)")
    mc_jpsi_files = get_files_from_grid(MC_JPSI_DIRS)
    create_job_lists(mc_jpsi_files, "file_lists_mc_jpsi")
    
    print("\nProcesso concluído. Agora você pode rodar 'condor_submit condor.sub'.")