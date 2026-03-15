#!/bin/bash
set -e

PROJECT_DIR="$(pwd)"

echo "Iniciando configuração do projeto..."
echo "Diretório do projeto: $PROJECT_DIR"

# Criação da estrutura principal
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/config"
mkdir -p "$PROJECT_DIR/dist"
mkdir -p "$PROJECT_DIR/data/input"
mkdir -p "$PROJECT_DIR/data/output"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/scripts"
mkdir -p "$PROJECT_DIR/src/configs"
mkdir -p "$PROJECT_DIR/src/session"
mkdir -p "$PROJECT_DIR/src/io_utils"
mkdir -p "$PROJECT_DIR/src/processing"
mkdir -p "$PROJECT_DIR/src/pipeline"
mkdir -p "$PROJECT_DIR/tests"

# Criação dos arquivos de configuração
touch "$PROJECT_DIR/config/settings.yaml"

# Criação dos arquivos __init__.py
touch "$PROJECT_DIR/src/__init__.py"
touch "$PROJECT_DIR/src/configs/__init__.py"
touch "$PROJECT_DIR/src/session/__init__.py"
touch "$PROJECT_DIR/src/io_utils/__init__.py"
touch "$PROJECT_DIR/src/processing/__init__.py"
touch "$PROJECT_DIR/src/pipeline/__init__.py"
touch "$PROJECT_DIR/tests/__init__.py"

# Criação dos arquivos-fonte principais
touch "$PROJECT_DIR/src/configs/settings.py"
touch "$PROJECT_DIR/src/session/spark_session.py"
touch "$PROJECT_DIR/src/io_utils/data_handler.py"
touch "$PROJECT_DIR/src/processing/transformations.py"
touch "$PROJECT_DIR/src/pipeline/pipeline.py"
touch "$PROJECT_DIR/src/main.py"

# Arquivos de teste
touch "$PROJECT_DIR/tests/test_transformations.py"

# Arquivos de empacotamento e documentação
touch "$PROJECT_DIR/pyproject.toml"
touch "$PROJECT_DIR/requirements.txt"
touch "$PROJECT_DIR/MANIFEST.in"
touch "$PROJECT_DIR/README.md"
touch "$PROJECT_DIR/.gitignore"

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
