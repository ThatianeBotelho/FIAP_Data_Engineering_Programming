# src/main.py
import logging

from configs.settings import AppConfig
from io_utils.data_handler import DataHandler
from pipeline.pipeline import PipelineOrchestrator
from processing.transformations import Transformation
from session.spark_session import SparkSessionManager

logger = logging.getLogger(__name__)


def config_logging() -> None:
    """Configura o logging para todo o projeto."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("./salestrust_pipeline/logs/pipeline.log"),
            logging.StreamHandler()
        ])


def main() -> None:
    """Função principal da aplicação."""
    spark = None

    try:
        logger.info("Iniciando aplicação principal.")

        logger.info("Carregando configurações.")
        settings = AppConfig()

        logger.info("Criando sessão Spark.")
        spark = SparkSessionManager.get_spark_session(settings.spark_app_name)
        spark.sparkContext.setLogLevel("WARN")

        logger.info("Instanciando dependências da aplicação.")
        data_handler = DataHandler(spark)
        transformation = Transformation(settings.report_year)

        logger.info("Criando orquestrador do pipeline.")
        orchestrator = PipelineOrchestrator(
            data_handler=data_handler,
            transformation=transformation)

        logger.info("Executando pipeline.")
        report_df = orchestrator.run(
            orders_path=settings.orders_path,
            payments_path=settings.payments_path,
            output_path=settings.output_path,
            orders_csv_options=settings.orders_csv_options,
            payments_json_options=settings.payments_json_options)

        logger.info("Pipeline executado com sucesso.")
        logger.info(f"Quantidade de registros no relatório final: {report_df.count()}")

    except Exception as exc:
        logger.error(f"Falha crítica no pipeline: {exc}")
        raise exc

    finally:
        if spark:
            spark.stop()
            logger.info("Sessão Spark finalizada.")


if __name__ == "__main__":
    config_logging()
    main()