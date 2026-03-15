# SalesTrust Pipeline

Projeto final da disciplina **Data Engineering Programming**.

## Objetivo

Desenvolver um pipeline em PySpark para gerar um relatório de pedidos de venda com pagamentos recusados (`status=false`) e classificados como legítimos na avaliação de fraude (`fraude=false`), considerando apenas pedidos do ano de 2025.

## Regras de negócio atendidas

O relatório final contém:

1. Identificador do pedido
2. Estado (UF)
3. Forma de pagamento
4. Valor total do pedido
5. Data do pedido

Além disso:

- considera apenas pedidos de 2025
- filtra pagamentos com `status=false`
- filtra pagamentos com `avaliacao_fraude.fraude=false`
- ordena por `uf`, `forma_pagamento` e `data_pedido`
- grava a saída em formato parquet

## Estrutura do projeto

```text
salestrust_pipeline/
├── config/
├── data/
├── logs/
├── scripts/
├── src/
└── tests/
```

## Criação do ambiente virtual

A partir de `/home/ubuntu/environment`:

```bash
python3 -m venv salestrust_pipeline/.venv
source salestrust_pipeline/.venv/bin/activate
```

## Instalação das dependências

```bash
pip install --upgrade pip
pip install -r salestrust_pipeline/requirements.txt
```

## Clonagem dos datasets

### Pagamentos

```bash
git clone https://github.com/infobarbosa/dataset-json-pagamentos salestrust_pipeline/data/input/dataset-json-pagamentos
```

### Pedidos

```bash
git clone https://github.com/infobarbosa/datasets-csv-pedidos salestrust_pipeline/data/input/datasets-csv-pedidos
```

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

## Observações

- Todos os schemas foram definidos explicitamente.
- O projeto foi estruturado com orientação a objetos.
- O `main.py` atua como aggregation root.
- As dependências são injetadas no fluxo principal.
- Há logging e tratamento de erros.
- Há teste unitário com `pytest`.

## Repositório público

Adicionar aqui o link do repositório GitHub público antes da entrega.