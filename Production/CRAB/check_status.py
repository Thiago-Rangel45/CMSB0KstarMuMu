import os
import subprocess

# Pasta base onde os projetos foram criados
base_dir = "crab_projects_CMSSW_15_1_0"

def get_crab_status(project_path):
    # Executa o crab status capturando a saída
    cmd = ["crab", "status", "-d", project_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Procura pelas linhas de status mais relevantes no output
    status_summary = []
    for line in result.stdout.split('\n'):
        if "Status on the scheduler:" in line:
            status_summary.append(line.strip())
        elif "Jobs status:" in line:
            status_summary.append(line.strip())
        elif "%" in line and any(x in line for x in ["finished", "running", "failed", "transferring", "idle"]):
            status_summary.append(f"  -> {line.strip()}")
            
    return status_summary

if __name__ == "__main__":
    if not os.path.exists(base_dir):
        print(f"Erro: Pasta base '{base_dir}' não encontrada.")
        exit(1)

    projects = sorted([f for f in os.listdir(base_dir) if f.startswith("crab_")])
    
    print("="*60)
    print(f"Verificando status de {len(projects)} projetos...")
    print("="*60)

    for project in projects:
        project_path = os.path.join(base_dir, project)
        print(f"\n[{project}]")
        
        status_lines = get_crab_status(project_path)
        
        if not status_lines:
             print("  Não foi possível recuperar o status (verifique manualmente).")
        else:
             for line in status_lines:
                 print(f"  {line}")

    print("\n" + "="*60)
    print("Verificação concluída.")
    print("="*60)