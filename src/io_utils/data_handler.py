# src/io_utils/data_handler.py
import logging

from py4j.protocol import Py4JJavaError
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType)
from pyspark.sql.utils import AnalysisException

logger = logging.getLogger(__name__)


class DataHandler:
    """
    Classe responsável pela leitura (input) e escrita (output) de dados.
    """

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark
        logger.info("DataHandler inicializado com sucesso.")

    def _get_schema_orders(self) -> StructType:
        """Define o schema explícito para o dataframe de pedidos."""
        logger.info("Definindo schema explícito para pedidos.")

        return StructType([
            StructField("id_pedido", StringType(), True),
            StructField("produto", StringType(), True),
            StructField("valor_unitario", DoubleType(), True),
            StructField("quantidade", LongType(), True),
            StructField("data_criacao", TimestampType(), True),
            StructField("uf", StringType(), True),
            StructField("id_cliente", LongType(), True)
        ])

    def _get_schema_payments(self) -> StructType:
        """Define o schema explícito para o dataframe de pagamentos."""
        logger.info("Definindo schema explícito para pagamentos.")

        return StructType([
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

    def load_orders(self, path: str, compression: str, header: bool, sep: str) -> DataFrame:
        """Carrega o dataframe de pedidos a partir de arquivos CSV."""
        try:
            logger.info(f"Iniciando leitura do dataset de pedidos em: '{path}'")

            schema = self._get_schema_orders()

            df = (
                self.spark.read
                .option("compression", compression)
                .option("mode", "FAILFAST")
                .csv(path, header=header, schema=schema, sep=sep))

            # Verificação de Dataframe Vazio
            if df.isEmpty():
                logger.warning(f"ATENÇÃO: O arquivo em '{path}' foi lido mas não contém registros.")

            logger.info("Leitura do dataset de pedidos concluída com sucesso.")
            return df

        except AnalysisException as exc:
            logger.error(f"Erro ao ler dataset de pedidos: {exc}")
            raise exc
        except Py4JJavaError as exc:
            logger.error(f"Erro crítico JVM ao ler dataset de pedidos: {exc}")
            raise exc

    def load_payments(self, path: str, compression: str) -> DataFrame:
        """Carrega o dataframe de pagamentos a partir de arquivos JSON."""
        try:
            logger.info(f"Iniciando leitura do dataset de pagamentos em: '{path}'")

            schema = self._get_schema_payments()

            df = (
                self.spark.read
                .option("compression", compression)
                .json(path, schema=schema))

            if df.isEmpty():
                logger.warning(f"ATENÇÃO: O arquivo em '{path}' foi lido mas não contém registros.")

            logger.info("Leitura do dataset de pagamentos concluída com sucesso.")
            return df

        except AnalysisException as exc:
            logger.error(f"Erro ao ler dataset de pagamentos: {exc}")
            raise
        except Py4JJavaError as exc:
            logger.error(f"Erro crítico JVM ao ler dataset de pagamentos: {exc}")
            raise

    def write_parquet(self, df: DataFrame, path: str) -> None:
        """Salva o DataFrame em formato Parquet."""
        try:
            logger.info(f"Iniciando escrita do relatório em parquet em: '{path}'")
            df.write.mode("overwrite").parquet(path)
            logger.info(f"Relatório salvo com sucesso em: '{path}'")
        except Exception as exc:
            logger.error(f"Erro ao gravar arquivo parquet: {exc}")
            raise exc

