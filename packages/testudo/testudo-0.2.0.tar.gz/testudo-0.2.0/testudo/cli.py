from pathlib import Path
from signal import signal, SIGINT
from threading import Event
from typing import Optional
from logging import DEBUG, INFO

import click
from yaml import safe_load
from logzero import loglevel as set_loglevel

from testudo.config import TaskConfig
from testudo.log import log
from testudo.runner import run_with_reporter

DEFAULT_CONFIG = Path.cwd() / 'config.yaml'


@click.command()
@click.option('-c', '--config-file', default=None,
              type=click.Path(exists=True, file_okay=True, dir_okay=False,
                              writable=False, readable=True,
                              resolve_path=True, allow_dash=False),
              help="Path to the configuration file, defaults to ./config.yaml")
@click.option('-d', '--database-file', required=True,
              type=click.Path(file_okay=True, dir_okay=False,
                              writable=True, readable=True,
                              resolve_path=True, allow_dash=False),
              help="Path to the database file")
@click.option('--debug', is_flag=True, help='Set logging level to DEBUG')
def main(config_file: Optional[str], database_file: str, debug: bool) -> None:
    """A script for printing hello world based on some configured values"""
    set_loglevel(DEBUG if debug else INFO)
    halt_flag = Event()

    def handle_sigint(_, __):
        log.info("SIGINT Received, sending shutdown signal...")
        halt_flag.set()

    log.debug('Configuring SIGINT handler...')
    signal(SIGINT, handle_sigint)
    config_path = DEFAULT_CONFIG if config_file is None else Path(config_file)
    config = TaskConfig(**safe_load(config_path.open(encoding="utf8")))  # type: ignore
    run_with_reporter(Path(database_file), config, halt_flag)
