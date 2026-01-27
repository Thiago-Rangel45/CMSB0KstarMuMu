#!/bin/bash

# Argumentos vindos do condor.sub:
# $1 = input_X.txt (Arquivo de lista)
# $2 = output_name.root
# $3 = mode (data ou mc)

INPUT_LIST_FILE=$(basename "$1")
OUTPUT_FILE=$2
MODE=$3

echo "========== JOB START =========="
echo "Host: $(hostname)"
echo "Processing: $INPUT_LIST_FILE"
echo "Mode: $MODE"

# Setup do ambiente (Descomente se necessário no seu cluster/lxplus)
# source /cvmfs/sft.cern.ch/lcg/views/LCG_104/x86_64-el9-gcc11-opt/setup.sh

# Executa o Python
python3 universal_skim.py --input_list "$INPUT_LIST_FILE" \
                          --output "$OUTPUT_FILE" \
                          --process_mode "$MODE"

PY_STATUS=$?
if [ $PY_STATUS -ne 0 ]; then
  echo "ERROR: universal_skim.py falhou."
  exit 1
fi

echo "Copiando output para EOS..."

# Configuração dos caminhos no EOS
# IMPORTANTE: Certifique-se que estas pastas existem! (eos mkdir -p ...)
EOS_BASE="root://eosuser.cern.ch//eos/user/t/tdeandra/skim_outputs"
EOS_DEST="$EOS_BASE/$MODE/"

# Copia usando xrdcp
xrdcp -f "$OUTPUT_FILE" "$EOS_DEST$OUTPUT_FILE"
COPY_STATUS=$?

if [ $COPY_STATUS -ne 0 ]; then
  echo "ERROR: Falha no xrdcp para o EOS."
  # Opcional: tentar copiar para /tmp local se falhar, mas em grid isso não ajuda muito
  exit 2
fi

# Limpeza do arquivo local no worker node
rm "$OUTPUT_FILE"
echo "========== JOB END =========="