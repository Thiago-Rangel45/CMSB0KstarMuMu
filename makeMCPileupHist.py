#!/usr/bin/env python3

"""
Use this script to convert MC pileup distribution from a Python file to a TH1 in a ROOT file.

e.g.

./makeMCPileupHist.py SimGeneral.MixingModule.mix_2017_25ns_WinterMC_PUScenarioV1_PoissonOOTPU_cfi
"""

import argparse
import importlib
import sys
import os
import ROOT

# --- Configuração do ROOT ---
# Impede que o ROOT interprete os argumentos da linha de comando
ROOT.PyConfig.IgnoreCommandLineOptions = True
# Executa em modo "batch" para não abrir janelas gráficas
ROOT.gROOT.SetBatch(True)
# Habilita o cálculo automático de erros estatísticos
ROOT.TH1.SetDefaultSumw2(True)


def get_module_name_from_path(filepath):
    """
    Converte um caminho de arquivo (padrão CMSSW) em um nome de módulo Python.
    Ex: /path/to/src/SimGeneral/MixingModule/python/mix.py -> SimGeneral.MixingModule.mix
    """
    # Normaliza o caminho para o padrão do sistema operacional
    filepath = os.path.normpath(filepath)
    parts = filepath.split(os.sep)

    try:
        # Encontra o diretório 'src', que é a raiz dos pacotes CMSSW
        src_index = parts.index('src')
        # O caminho do módulo começa após 'src'
        module_parts = parts[src_index + 1:]
        
        # O subdiretório 'python' não faz parte do nome do módulo
        if 'python' in module_parts:
            module_parts.remove('python')

        # Junta as partes para formar o nome do módulo
        module_name = ".".join(module_parts)
        
        # Remove a extensão do arquivo (.py)
        return os.path.splitext(module_name)[0]

    except ValueError:
        print(f"Aviso: Diretório 'src' não encontrado no caminho '{filepath}'.", file=sys.stderr)
        # Se 'src' não for encontrado, assume que o nome já é um módulo
        return os.path.splitext(os.path.basename(filepath))[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pileup", help="Nome do arquivo de pileup do MC (módulo Python ou caminho para o arquivo)")
    parser.add_argument("--nbins", type=int, default=100, help="Número de bins do histograma")
    parser.add_argument("--min", type=float, default=0.0, help="Limite inferior do histograma")
    parser.add_argument("--max", type=float, default=100.0, help="Limite superior do histograma")
    parser.add_argument("-o", "--outputFilename", default="PileupMC.root", help="Nome do arquivo ROOT de saída")
    args = parser.parse_args()

    module_name = ""
    if os.path.isfile(args.pileup):
        # Se for um arquivo, converte o caminho para nome de módulo
        module_name = get_module_name_from_path(args.pileup)
    else:
        # Caso contrário, assume que já é o nome do módulo
        module_name = args.pileup

    print(f"Tentando importar o módulo: {module_name}")
    try:
        # Importa o módulo dinamicamente
        py_file = importlib.import_module(module_name)
    except ImportError as e:
        print(f"Erro: Não foi possível importar o módulo '{module_name}'. Verifique o nome e seu PYTHONPATH.", file=sys.stderr)
        print(f"Detalhes: {e}", file=sys.stderr)
        sys.exit(1)

    # Extrai os dados de pileup do módulo (específico para arquivos de configuração CMSSW)
    try:
        bins = py_file.mix.input.nbPileupEvents.probFunctionVariable
        values = py_file.mix.input.nbPileupEvents.probValue
    except AttributeError as e:
        print(f"Erro: Não foi possível encontrar os dados de pileup no módulo '{module_name}'.", file=sys.stderr)
        print("Verifique se o arquivo contém 'mix.input.nbPileupEvents.probFunctionVariable' e 'probValue'.", file=sys.stderr)
        sys.exit(1)

    # --- Verificações de Sanidade ---
    if not bins or not values:
        raise RuntimeError("As listas de dados de pileup estão vazias.")
    if min(bins) < args.min:
        raise RuntimeError(f"O valor de --min ({args.min}) é maior que o menor bin no arquivo de PU ({min(bins)}).")
    if max(bins) > args.max:
        raise RuntimeError(f"O valor de --max ({args.max}) é menor que o maior bin no arquivo de PU ({max(bins)}).")
    if len(bins) != len(values):
        raise RuntimeError(f"O número de bins ({len(bins)}) não corresponde ao número de valores ({len(values)}).")

    # --- Criação e Preenchimento do Histograma ---
    hist = ROOT.TH1D("pileup", "MC Pileup Distribution;True Number of Interactions;Probability", args.nbins, args.min, args.max)

    # Preenche o histograma de forma robusta
    for i, bin_val in enumerate(bins):
        # 'bin_val' é o número de interações (eixo x)
        # 'values[i]' é a probabilidade (peso)
        hist.Fill(bin_val, values[i])

    # Normaliza o histograma para que a integral seja 1
    integral = hist.Integral()
    if integral > 0:
        hist.Scale(1.0 / integral)
    else:
        print("Aviso: A integral do histograma é zero. Não foi possível normalizar.", file=sys.stderr)

    # --- Escrita no Arquivo de Saída ---
    print(f"Salvando histograma em {args.outputFilename}...")
    try:
        f = ROOT.TFile(args.outputFilename, "RECREATE")
        if not f or f.IsZombie():
            raise IOError(f"Não foi possível criar o arquivo de saída: {args.outputFilename}")
        
        hist.Write("pileup")
        f.Close()
        print("Concluído.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo ROOT: {e}", file=sys.stderr)
        sys.exit(1)
