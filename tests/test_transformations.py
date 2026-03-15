# tests/test_transformations.py
import logging
from datetime import datetime

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType)

from processing.transformations import Transformation

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def spark_session():
    logger.info("Criando SparkSession para testes.")

    spark = (
        SparkSession.builder
        .appName("PySpark Unit Tests")
        .master("local[*]")
        .getOrCreate()
    )

    yield spark

    spark.stop()
    logger.info("SparkSession de testes finalizada.")


def test_build_report_filters_and_returns_expected_columns(spark_session):
    logger.info("Iniciando teste unitário da classe Transformation.")

    orders_schema = StructType([
        StructField("id_pedido", StringType(), True),
        StructField("produto", StringType(), True),
        StructField("valor_unitario", DoubleType(), True),
        StructField("quantidade", LongType(), True),
        StructField("data_criacao", TimestampType(), True),
        StructField("uf", StringType(), True),
        StructField("id_cliente", LongType(), True),
    ])

    payments_schema = StructType([
        StructField("id_pedido", StringType(), True),
        StructField("forma_pagamento", StringType(), True),
        StructField("valor_pagamento", DoubleType(), True),
        StructField("status", BooleanType(), True),
        StructField("data_processamento", TimestampType(), True),
        StructField(
            "avaliacao_fraude",
            StructType([
                StructField("fraude", BooleanType(), True),
                StructField("score", DoubleType(), True),
            ]),
            True)
    ])

    orders_data = [
        ("1", "NOTEBOOK", 1500.0, 2, datetime(2025, 1, 10, 10, 0, 0), "SP", 100),
        ("2", "CELULAR", 1000.0, 1, datetime(2024, 5, 10, 10, 0, 0), "RJ", 101),
    ]

    payments_data = [
        ("1", "PIX", 3000.0, False, datetime(2025, 1, 10, 10, 5, 0), {"fraude": False, "score": 0.10}),
        ("2", "CARTAO", 1000.0, False, datetime(2024, 5, 10, 10, 5, 0), {"fraude": False, "score": 0.30}),
    ]

    orders_df = spark_session.createDataFrame(orders_data, schema=orders_schema)
    payments_df = spark_session.createDataFrame(payments_data, schema=payments_schema)

    transformation = Transformation(report_year=2025)
    result_df = transformation.build_report(orders_df, payments_df)

    result = result_df.collect()

    assert len(result) == 1
    assert result[0]["id_pedido"] == "1"
    assert result[0]["uf"] == "SP"
    assert result[0]["forma_pagamento"] == "PIX"
    assert result[0]["valor_total_pedido"] == 3000.0

    logger.info("Teste unitário executado com sucesso.")