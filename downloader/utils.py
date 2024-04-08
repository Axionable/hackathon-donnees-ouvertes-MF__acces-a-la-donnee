import json
import logging
import os
import sys


FORMAT = "%(asctime)-15s [%(filename)s:%(lineno)s - %(funcName)2s()] %(message)s"
log_level = os.environ.get("LOG_LEVEL") if os.environ.get(
    "LOG_LEVEL") is not None else "INFO"
logging.basicConfig(
    stream=sys.stdout, format=FORMAT, level=logging.getLevelName(log_level)
)
LOGGER = logging.getLogger(__name__)


def is_source_key_available(source_key: str) -> bool:
    """
    Check if "source_key" is available in the file: downloader/conf/sim.json
    :param source_key: Key corresponding to the desired data source
    :return: Verification status (true or false)
    """
    if source_key is None:
        return False

    else:
        with open("downloader/conf/conf.json", "r") as file:
            content = json.load(file)
            return source_key in content["sources"].keys()


def get_data_info(source_key: str) -> dict:
    """
    Return elements within the config file.
    :param source_key: Key corresponding to the desired data source
    :return: Config element's value
    """
    if source_key is not None:
        with open("downloader/conf/conf.json", "r") as file:
            content = json.load(file)
            return content["sources"][source_key]
