import logging
from datetime import datetime, date
from typing import Optional

import os
import yaml
import click
from box import Box

from elasticcsv import elastic_csv

logger = logging.getLogger(__name__)
config: Optional[Box] = None


def _load_config():
    global config
    logger.info("Loading connection.yaml file")
    if not os.path.exists("./connection.yaml"):
        logger.critical(f"Can't load csv into elastic without 'connection.yaml' config file")
        logger.critical(f"See https://gitlab.com/juguerre/elasticcsv")
        exit(1)
    with open("./connection.yaml") as conn_file:
        conn_d = yaml.load(conn_file, Loader=yaml.FullLoader)
        config = Box(conn_d, box_dots=True)


@click.group()
def cli():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        level="WARNING"
    )
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    logging.getLogger("elasticcsv").setLevel(logging.DEBUG)


@cli.command()
@click.option("--csv", type=click.Path(exists=True), help="CSV File", required=True)
@click.option("--sep", type=click.STRING, help="CSV field sepator", required=True)
@click.option("--index", type=click.STRING, help="Elastic Index", required=True)
@click.option("--csv-date-format", type=click.STRING, help="date format for *_date columns as for ex: '%Y-%m-%d'")
@click.option("--logic_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              help="Date reference for interfaces", required=False)
def load_csv(csv: str, index: str, csv_date_format: str, sep: str, logic_date: datetime):
    """Loads csv to elastic index"""
    _load_config()
    logger.info(f"Loading file: {csv}")
    logger.info(f"CSV Date Format: {csv_date_format}")

    logic_date = logic_date.date() if logic_date else date.today()
    elastic_csv.load_csv(config=config,
                         csv_file_name=csv,
                         index=index,
                         delimiter=sep,
                         csv_date_format=csv_date_format,
                         logic_date=logic_date)


@cli.command()
@click.option("--csv", type=click.Path(exists=False), help="CSV File", required=True)
@click.option("--sep", type=click.STRING, help="CSV field sepator", required=True)
@click.option("--index", type=click.STRING, help="Elastic Index", required=True)
def download_index(csv: str, index: str, sep: str):
    """Download index to csv file"""
    _load_config()
    logger.info(f"Downloading index: {index}")
    elastic_csv.download_csv(config=config,
                             index=index,
                             csv_file_name=csv,
                             delimiter=sep)


if __name__ == "__main__":
    cli()
