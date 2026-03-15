# SalesTrust Pipeline

Projeto final da disciplina **Data Engineering Programming**.
Pipeline de dados desenvolvido em **PySpark**, estruturado com **orientação a objetos**, responsável por gerar um relatório analítico de pedidos de venda com pagamentos recusados e classificados como legítimos na avaliação de fraude.

---

## Objetivo

Desenvolver um pipeline responsável por gerar um relatório de pedidos de venda com pagamentos recusados (`status=false`) e classificados como legítimos na avaliação de fraude (`fraude=false`), considerando apenas pedidos do ano de 2025. O resultado do processamento é persistido em formato Parquet.

---

## Regras de negócio

O dataset final contém:
1. Identificador do pedido
2. Estado (UF)
3. Forma de pagamento
4. Valor total do pedido
5. Data do pedido

Durante o processamento são aplicados os seguintes critérios:
- considerar apenas pedidos realizados no ano de **2025**
- filtrar pagamentos com `status=false`
- considerar apenas registros com `avaliacao_fraude.fraude=false`
- ordenar o resultado por `uf`, `forma_pagamento` e `data_pedido`
- grava a saída em formato **Parquet**

---

## Estrutura do projeto

```text
salestrust_pipeline/
├── config/
│   └── settings.yaml
├── data/
│   ├── input/
│   │   ├── dataset-json-pagamentos/
│   │   └── datasets-csv-pedidos/
│   └── output/
├── logs/
├── scripts/
│   └── salestrust_pipeline_setup.sh
├── src/
│   ├── main.py
│   ├── configs/
│   │   └── settings.py
│   ├── session/
│   │   └── spark_session.py
│   ├── io_utils/
│   │   └── data_handler.py
│   ├── processing/
│   │   └── transformations.py
│   └── pipeline/
│       └── pipeline.py
├── tests/
│   └── test_transformations.py
├── README.md
├── MANIFEST.in
├── pyproject.toml
├── requirements.txt
```
---

## Requisitos

- Python 3.9 ou superior
- Java (necessário para execução do Apache Spark)
- Git instalado

---

## Preparação do ambiente

### Clonar o repositório

```bash
git clone https://github.com/ThatianeBotelho/FIAP_Data_Engineering_Programming.git salestrust_pipeline
cd salestrust_pipeline
```

### Executar script de setup:

```bash
bash scripts/salestrust_pipeline_setup.sh
```

O script realiza automaticamente:
- criação do ambiente virtual
- instalação das dependências
- clonagem dos datasets necessários

### Diretório de execução e ambiente virtual

Todos os comandos do projeto devem ser executados:
- a partir do diretório raiz do projeto
- com o ambiente virtual ativo

Ative o ambiente virtual com:
```bash
source .venv/bin/activate
```

> *Exemplo ilustrativo de terminal com ambiente virtual ativo e execução no diretório raiz do projeto:*
>
> ```bash
> (.venv) salestrust_pipeline $
> ```
---

## Execução do Projeto

### Execução dos testes

```bash
PYTHONPATH=src pytest tests
```

### Execução do pipeline

```bash
PYTHONPATH=src python src/main.py
```
---

## Resultados Gerados

O relatório parquet será salvo em:

```text
salestrust_pipeline/data/output/sales_orders_report_2025/
```

Para visualizar uma amostra dos dados gerados (20 primeiras linhas), execute:
```bash
ls data/output/
python -c "
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet('data/output/sales_orders_report_2025/')
df.show(20, truncate=False)
spark.stop()
"
```
Para visualizar o registro das etapas do pipeline no arquivo de log, execute:
```bash
tail -n 20 logs/salestrust_pipeline.log
```
---

## Arquitetura

O projeto foi estruturado seguindo princípios de separação de responsabilidades e injeção de dependências, contemplando os requisitos da disciplina:
- Schemas explicitamente definidos para todos os DataFrames (sem inferência)
- Classe dedicada para gerenciamento da sessão Spark
- Classe dedicada para leitura e escrita de dados (I/O)
- Classe dedicada para implementação das regras de negócio
- Classe responsável pela orquestração do pipeline
- `main.py` atuando como Aggregation Root, responsável por instanciar e injetar as dependências
- Configurações centralizadas em arquivo YAML
- Logging estruturado para rastreabilidade das etapas
- Tratamento de exceções na lógica de negócio
- Teste unitário implementado com `pytest`

