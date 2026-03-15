#!/bin/bash
set -e

PROJECT_DIR="$(pwd)"

echo "Iniciando configuração do projeto..."
echo "Diretório do projeto: $PROJECT_DIR"

# Garante diretórios operacionais
mkdir -p "$PROJECT_DIR/data/input"
mkdir -p "$PROJECT_DIR/data/output"
mkdir -p "$PROJECT_DIR/logs"

# Criação do ambiente virtual
if [ ! -d "$PROJECT_DIR/.venv" ]; then
  echo "Criando ambiente virtual..."
  python3 -m venv "$PROJECT_DIR/.venv"
else
  echo "Ambiente virtual já existe."
fi

# Ativação do ambiente virtual
source "$PROJECT_DIR/.venv/bin/activate"

# Instalação das dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

# Clonagem dos datasets
if [ ! -d "$PROJECT_DIR/data/input/dataset-json-pagamentos" ]; then
  echo "Clonando dataset de pagamentos..."
  git clone https://github.com/infobarbosa/dataset-json-pagamentos "$PROJECT_DIR/data/input/dataset-json-pagamentos"
else
  echo "Dataset de pagamentos já existe."
fi

if [ ! -d "$PROJECT_DIR/data/input/datasets-csv-pedidos" ]; then
  echo "Clonando dataset de pedidos..."
  git clone https://github.com/infobarbosa/datasets-csv-pedidos "$PROJECT_DIR/data/input/datasets-csv-pedidos"
else
  echo "Dataset de pedidos já existe."
fi

echo "Configuração finalizada com sucesso."
echo "Para ativar o ambiente virtual depois, rode:"
echo "source .venv/bin/activate"
