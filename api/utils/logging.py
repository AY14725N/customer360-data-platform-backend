import logging.config
from pathlib import Path

import yaml


def configure_logging(path: Path = Path("config/logging.yaml")) -> None:
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            logging.config.dictConfig(yaml.safe_load(handle))
    else:
        logging.basicConfig(level=logging.INFO)
