# src/processing/transformations.py
import logging

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

logger = logging.getLogger(__name__)


class Transformation:
    """
    Classe que contém as transformações e regras de negócio da aplicação.
    """

    def __init__(self, report_year: int) -> None:
        self.report_year = report_year
        logger.info(f"Transformation inicializada para o ano de relatório: {report_year}")

    def add_order_total(self, orders_df: DataFrame) -> DataFrame:
        """Adiciona a coluna valor_total_pedido."""
        logger.info("Adicionando coluna valor_total_pedido.")
        return orders_df.withColumn(
            "valor_total_pedido",
            F.col("valor_unitario") * F.col("quantidade"))

    def filter_orders_from_report_year(self, orders_df: DataFrame) -> DataFrame:
        """Filtra apenas pedidos do ano configurado."""
        logger.info(f"Filtrando pedidos do ano de {self.report_year}")
        return orders_df.filter(
            F.year(F.col("data_criacao")) == self.report_year
        )

    def filter_refused_and_legitimate_payments(self, payments_df: DataFrame) -> DataFrame:
        """Filtra pagamentos recusados e classificados como legítimos."""
        logger.info("Filtrando pagamentos com status=false e fraude=false.")
        return payments_df.filter(
            (F.col("status") == F.lit(False)) &
            (F.col("avaliacao_fraude.fraude") == F.lit(False)))

    def join_orders_and_payments(self, orders_df: DataFrame, payments_df: DataFrame) -> DataFrame:
        """Faz a junção entre os DataFrames de pedidos e pagamentos."""
        logger.info("Realizando join entre pedidos e pagamentos.")
        return orders_df.join(payments_df, on="id_pedido", how="inner")

    def select_final_report_columns(self, report_df: DataFrame) -> DataFrame:
        """Seleciona as colunas finais exigidas no relatório."""
        logger.info("Selecionando colunas finais do relatório.")
        return report_df.select(
            F.col("id_pedido"),
            F.col("uf"),
            F.col("forma_pagamento"),
            F.col("valor_total_pedido"),
            F.col("data_criacao").alias("data_pedido"))

    def order_final_report(self, report_df: DataFrame) -> DataFrame:
        """Ordena o relatório final por UF, forma de pagamento e data do pedido."""
        logger.info("Ordenando relatório final.")
        return report_df.orderBy(
            F.col("uf").asc(),
            F.col("forma_pagamento").asc(),
            F.col("data_pedido").asc())

    def build_report(self, orders_df: DataFrame, payments_df: DataFrame) -> DataFrame:
        """Executa todas as etapas de transformação para construir o relatório final."""
        try:
            logger.info("Iniciando pipeline de transformação do relatório.")

            logger.info("Etapa 1: cálculo do valor total do pedido.")
            orders_with_total_df = self.add_order_total(orders_df)

            logger.info("Etapa 2: filtro de pedidos do ano de relatório.")
            filtered_orders_df = self.filter_orders_from_report_year(orders_with_total_df)

            logger.info("Etapa 3: filtro de pagamentos recusados e legítimos.")
            filtered_payments_df = self.filter_refused_and_legitimate_payments(payments_df)

            logger.info("Etapa 4: junção entre pedidos e pagamentos.")
            joined_df = self.join_orders_and_payments(filtered_orders_df, filtered_payments_df)

            logger.info("Etapa 5: seleção das colunas finais.")
            selected_df = self.select_final_report_columns(joined_df)

            logger.info("Etapa 6: ordenação final do relatório.")
            ordered_df = self.order_final_report(selected_df)

            logger.info("Pipeline de transformação concluído com sucesso.")
            return ordered_df

        except Exception as exc:
            logger.error(f"Erro durante a transformação do relatório: {exc}")
            raise exc