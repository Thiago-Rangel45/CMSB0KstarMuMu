#!/bin/bash

# Verifica se o usuário passou a Era
if [ -z "$1" ]; then
    echo "Erro: Faltou o nome da era."
    echo "Uso: ./merge_roots.sh dados_Run2022C"
    exit 1
fi

ERA=$1
INPUT_DIR="/eos/user/t/tdeandra/skim_outputs/$ERA"
OUTPUT_DIR="/eos/user/t/tdeandra/skim_outputs/Merged_Eras"
OUTPUT_FILE="$OUTPUT_DIR/Merged_${ERA}.root"
LIST_FILE="list_to_merge_${ERA}.txt"

if [ ! -d "$INPUT_DIR" ]; then
    echo "Erro: A pasta $INPUT_DIR não existe no EOS."
    exit 1
fi

# Cria a pasta de destino final no EOS
mkdir -p "$OUTPUT_DIR"

echo "=============================================="
echo "Iniciando Merge e Limpeza para a era: $ERA"
echo "=============================================="

# 1. Coleta o caminho absoluto de todos os arquivos ROOT
echo "🔍 Mapeando arquivos em $INPUT_DIR..."
find "$INPUT_DIR" -type f -name "*.root" > "$LIST_FILE"
NUM_FILES=$(wc -l < "$LIST_FILE")

if [ "$NUM_FILES" -eq 0 ]; then
    echo "❌ Nenhum arquivo encontrado em $INPUT_DIR."
    rm -f "$LIST_FILE"
    exit 1
fi

echo "✅ $NUM_FILES arquivos encontrados. Unindo em paralelo (-j 8)..."

# 2. Roda o hadd
hadd -j 8 -f "$OUTPUT_FILE" @"$LIST_FILE"

# 3. Trava de segurança: Só apaga se o hadd foi perfeito
if [ $? -eq 0 ]; then
    echo "=============================================="
    echo "🎉 SUCESSO no Merge! Salvo em: $OUTPUT_FILE"
    echo "🗑️  Limpando os $NUM_FILES arquivos originais para liberar cota..."
    
    # xargs lê o arquivo TXT e deleta os ROOTs sem travar o terminal
    xargs rm -f < "$LIST_FILE"
    
    if [ $? -eq 0 ]; then
        echo "✅ Limpeza concluída! A pasta $INPUT_DIR está vazia."
    else
        echo "⚠️ Aviso: O merge funcionou, mas houve um erro ao apagar alguns arquivos."
    fi
    echo "=============================================="
    
    # Limpa a lista temporária
    rm -f "$LIST_FILE"
else
    echo "❌ Erro durante a execução do hadd. Os arquivos originais NÃO foram apagados por segurança."
fi
