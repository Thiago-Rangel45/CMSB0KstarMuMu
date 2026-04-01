import subprocess
import os

FILES_PER_JOB = 1 
REDIRECTOR = "root://xrootd2.hepgrid.uerj.br:1094/"

eras = ["Run2022C", "Run2022D", "Run2022E", "Run2022F", "Run2022G"]
MC_DIRS_BASE = "/store/user/tdeandra/BPH_NanoAOD_MC/"
DATA_DIRS_BASE = "/store/user/tdeandra/BPH_NanoAOD_Data/"

def get_files_uerj(dir_path):
    """Lista arquivos usando o protocolo XRootD da UERJ"""
    found_files = []
    cmd = f"xrdfs xrootd2.hepgrid.uerj.br:1094 ls -R {dir_path} | grep '.root' | grep -v '/log/'"
    
    try:
        print(f"Buscando em: {dir_path}")
        result = subprocess.check_output(cmd, shell=True, text=True)
        for line in result.splitlines():
            if line.strip():
                path = line.strip()
                if not path.startswith("/store/"):
                    path = "/store/" + path.split("/store/")[-1]
                found_files.append(f"{REDIRECTOR}{path}")
    except Exception as e:
        print(f"⚠️ Erro ao listar {dir_path}: {e}")
    return found_files

def create_job_lists(file_list, output_folder):
    if not file_list: return
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    
    master_list_name = os.path.join(output_folder, "list_files.txt")
    with open(master_list_name, "w") as f:
        for root_file in file_list:
            f.write(root_file + "\n")
    print(f"✔ {output_folder}: {len(file_list)} jobs criados.")

if __name__ == "__main__":
    mc_samples = {
        "mc_signal_2022": "BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoKstarMuMu_2022/",
        "mc_signal_2022EE": "BdtoKstar2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoKstarMuMu_2022EE/",
        "mc_jpsi_2022": "BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoJpsiKstar_2022/",
        "mc_jpsi_2022EE": "BdtoJpsiKstar_Jpsito2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoJpsiKstar_2022EE/",
        "mc_psi2s_2022": "BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoKstarPsi2s_2022/",
        "mc_psi2s_2022EE": "BdtoKstarPsi2s_Psi2sto2Mu_KstartoKPi_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/BPH_Nano_MC_BdtoKstarPsi2s_2022EE/",
    }

    for key, subpath in mc_samples.items():
        files = get_files_uerj(MC_DIRS_BASE + subpath)
        create_job_lists(files, f"file_lists_{key}")

    for era in eras:
        all_data_files = []
        for i in range(8):
            path = f"{DATA_DIRS_BASE}{era}/ParkingDoubleMuonLowMass{i}/NanoAOD_LowMass{i}/"
            all_data_files.extend(get_files_uerj(path))
        create_job_lists(all_data_files, f"file_lists_dados_{era}")