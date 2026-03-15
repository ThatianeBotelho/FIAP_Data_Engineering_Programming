# src/config/settings.py
import logging
import yaml

logger = logging.getLogger(__name__)


class AppConfig:
    """
    Classe responsável por carregar e disponibilizar as configurações
    centralizadas da aplicação a partir do arquivo settings.yaml.
    """

    def __init__(self, path: str = "./salestrust_pipeline/config/settings.yaml") -> None:
        logger.info("Carregando configurações da aplicação do arquivo YAML.")

        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        self.spark_app_name = config["spark"]["app_name"]

        self.orders_path = config["paths"]["orders"]
        self.payments_path = config["paths"]["payments"]
        self.output_path = config["paths"]["output"]

        self.orders_csv_options = config["file_options"]["orders_csv"]
        self.payments_json_options = config["file_options"]["payments_json"]

        self.report_year = config["report"]["year"]

        logger.info("Configurações carregadas com sucesso.")