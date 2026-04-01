#!/bin/bash
# job.sh

INPUT_URL="$1"   
OUTPUT_NAME="$2"       
MODE_FULL="$3"         

echo "========== JOB START LOCAL T2_UERJ =========="
echo "Input URL: $INPUT_URL"

# Atraso aleatorio de 1 a 60 segundos para evitar sobrecarga no servidor
sleep $((RANDOM % 60))

cd $_CONDOR_SCRATCH_DIR
export X509_USER_PROXY=$_CONDOR_SCRATCH_DIR/my_proxy
export X509_CERT_DIR=/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates

[[ $MODE_FULL == *mc* ]] && INTERNAL_MODE="mc" || INTERNAL_MODE="data"

python3 universal_skim.py --input_list "$INPUT_URL" \
                          --output "$OUTPUT_NAME" \
                          --process_mode "$INTERNAL_MODE"

if [ $? -ne 0 ]; then 
    echo "Erro no universal_skim.py"
    exit 1
fi

EOS_DEST="root://eosuser.cern.ch//eos/user/t/tdeandra/skim_outputs/$MODE_FULL"
echo "Enviando para o EOS CERN: $EOS_DEST"
xrdcp -f --nopbar --streams 4 "$OUTPUT_NAME" "$EOS_DEST/$OUTPUT_NAME"

if [ $? -eq 0 ]; then 
    rm -f "$OUTPUT_NAME"
    echo "Sucesso e limpeza concluida."
else 
    echo "Erro no xrdcp para o EOS"
    exit 2
fi
