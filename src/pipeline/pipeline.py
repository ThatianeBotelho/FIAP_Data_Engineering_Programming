# src/pipeline/pipeline.py
import logging

from pyspark.sql import DataFrame

from io_utils.data_handler import DataHandler
from processing.transformations import Transformation

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Classe responsável pela orquestração do pipeline de dados.
    """

    def __init__(self, data_handler: DataHandler, transformation: Transformation) -> None:
        self.data_handler = data_handler
        self.transformation = transformation
        logger.info("PipelineOrchestrator inicializado com sucesso.")

    def run(self, orders_path: str, payments_path: str, output_path: str, orders_csv_options: dict, payments_json_options: dict) -> DataFrame:
        """Executa o pipeline completo: leitura, transformação e escrita."""
        logger.info("Iniciando execução do pipeline completo.")

        logger.info("Lendo dados de pedidos.")
        orders_df = self.data_handler.load_orders(
            path=orders_path,
            compression=orders_csv_options["compression"],
            header=orders_csv_options["header"],
            sep=orders_csv_options["sep"])

        logger.info("Lendo dados de pagamentos.")
        payments_df = self.data_handler.load_payments(
            path=payments_path,
            compression=payments_json_options["compression"])

        logger.info("Aplicando regras de negócio para construção do relatório.")
        report_df = self.transformation.build_report(orders_df, payments_df)

        logger.info("Gravando relatório final em parquet.")
        self.data_handler.write_parquet(df=report_df, path=output_path)

        logger.info("Execução do pipeline concluída com sucesso.")
        return report_df