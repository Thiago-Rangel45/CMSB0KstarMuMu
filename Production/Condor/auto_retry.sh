#!/bin/bash

# 1. Verifica se o usuário passou o nome da era
if [ -z "$1" ]; then
    echo "Erro: Faltou o nome da era."
    echo "Uso: ./auto_retry.sh <nome_da_era>"
    echo "Exemplo: ./auto_retry.sh dados_Run2022C"
    exit 1
fi

ERA=$1
LOG_DIR="logs/$ERA"
RETRY_LIST="retry_list_${ERA}.txt"
RETRY_SUB="condor_retry_${ERA}.sub"

# 2. Verifica se a pasta existe
if [ ! -d "$LOG_DIR" ]; then
    echo "Erro: A pasta $LOG_DIR não existe."
    exit 1
fi

echo "=============================================="
echo "Iniciando resubmissão automática para: $ERA"
echo "=============================================="

# 3. Procura os arquivos de erro que não estão vazios
ERR_FILES=$(find "$LOG_DIR" -name "*.err" ! -size 0)

if [ -z "$ERR_FILES" ]; then
    echo "✅ Excelente! Nenhum erro encontrado na pasta $LOG_DIR."
    exit 0
fi

# 4. Limpa a lista de repescagem antiga, se existir
> "$RETRY_LIST"
COUNT=0

# 5. Extrai as URLs e cria a lista
echo "Extraindo URLs dos jobs que falharam..."
for ERR_FILE in $ERR_FILES; do
    # Troca a extensão de .err para .out para achar o log correspondente
    OUT_FILE="${ERR_FILE%.err}.out"
    
    if [ -f "$OUT_FILE" ]; then
        # Pega a última palavra (o link) da linha que contém "Input URL"
        URL=$(grep "Input URL" "$OUT_FILE" | awk '{print $NF}')
        
        if [ -n "$URL" ]; then
            echo "$URL" >> "$RETRY_LIST"
            ((COUNT++))
            # Renomeia o arquivo .err para não ser lido novamente no futuro
            mv "$ERR_FILE" "${ERR_FILE}.lido"
        fi
    fi
done

echo "⚠️ Foram encontrados $COUNT arquivos com falha."
echo "📋 Lista salva em: $RETRY_LIST"

# 6. Cria o arquivo de submissão HTCondor sob medida
cat << EOF_SUB > "$RETRY_SUB"
universe              = vanilla
executable            = job.sh
getenv                = True
transfer_input_files  = universal_skim.py, my_proxy
should_transfer_files = YES
transfer_output_files = ""
x509userproxy         = my_proxy
+JobFlavour           = "longlunch"

# Usamos o Auto-Retry aqui também para garantir a repescagem
max_retries           = 3

output                = $LOG_DIR/retry_job_\$(ProcId).out
error                 = $LOG_DIR/retry_job_\$(ProcId).err
log                   = $LOG_DIR/retry_cluster.log
arguments             = \$(filename) Skim_Retry_\$(ProcId).root $ERA

queue filename from $RETRY_LIST
EOF_SUB

# 7. Submete a repescagem
echo "🚀 Submetendo ao HTCondor..."
condor_submit "$RETRY_SUB"
echo "=============================================="
