# SalesTrust Pipeline

Projeto final da disciplina **Data Engineering Programming**.
Pipeline de dados desenvolvido em **PySpark**, estruturado com **orientação a objetos**, responsável por gerar um relatório analítico de pedidos de venda com pagamentos recusados e classificados como legítimos na avaliação de fraude.


## Objetivo

Desenvolver um pipeline responsável por gerar um relatório de pedidos de venda com pagamentos recusados (`status=false`) e classificados como legítimos na avaliação de fraude (`fraude=false`), considerando apenas pedidos do ano de 2025. O resultado do processamento é persistido em formato Parquet.

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

## Requisitos

- Python 3.9 ou superior
- Java (necessário para execução do Apache Spark)
- Git instalado

## Preparação do ambiente

### Clonar o repositório

```bash
git clone https://github.com/ThatianeBotelho/FIAP_Data_Engineering_Programming.git salestrust_pipeline
cd salestrust_pipeline
```

Após clonar o repositório, execute:

```bash
bash scripts/salestrust_pipeline_setup.sh
```

O script realiza automaticamente:
- criação do ambiente virtual
- instalação das dependências
- clonagem dos datasets necessários


## Execução dos testes

```bash
cd /home/ubuntu/environment
source salestrust_pipeline/.venv/bin/activate
PYTHONPATH=salestrust_pipeline/src pytest salestrust_pipeline/tests
```

## Execução do pipeline

```bash
cd /home/ubuntu/environment
source salestrust_pipeline/.venv/bin/activate
PYTHONPATH=salestrust_pipeline/src python salestrust_pipeline/src/main.py
```

## Saída gerada

O relatório parquet será salvo em:

```text
salestrust_pipeline/data/output/sales_orders_report_2025/
```

Para visualizar uma amostra dos dados gerados (20 primeiras linhas), execute:
```bash
python -c "
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet('data/output/sales_orders_report_2025/')
df.show(20, truncate=False)
spark.stop()
"
```

## Observações

- Todos os schemas foram definidos explicitamente.
- O projeto foi estruturado com orientação a objetos.
- O `main.py` atua como aggregation root.
- As dependências são injetadas no fluxo principal.
- Há logging e tratamento de erros.
- Há teste unitário com `pytest`.

