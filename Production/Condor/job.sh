#!/bin/bash

INPUT_LIST_FILE=$(basename "$1")
OUTPUT_FILE=$2
MODE=$3

echo "========== JOB START =========="
echo "Host: $(hostname)"
echo "Processing: $INPUT_LIST_FILE"
echo "Mode: $MODE"

python3 universal_skim.py --input_list "$INPUT_LIST_FILE" \
                          --output "$OUTPUT_FILE" \
                          --process_mode "$MODE"

PY_STATUS=$?
if [ $PY_STATUS -ne 0 ]; then
  echo "ERROR: universal_skim.py falhou."
  exit 1
fi

echo "Copiando output para EOS na pasta específica: $MODE"

EOS_BASE="root://eosuser.cern.ch//eos/user/t/tdeandra/skim_outputs"
EOS_DEST="$EOS_BASE/$MODE/"

xrdcp -f "$OUTPUT_FILE" "$EOS_DEST$OUTPUT_FILE"
COPY_STATUS=$?

if [ $COPY_STATUS -ne 0 ]; then
  echo "ERROR: Falha no xrdcp para o EOS."
  exit 2
fi

rm "$OUTPUT_FILE"
echo "========== JOB END =========="