import yaml
import logging
from importlib import resources
from . import configuration

logger = logging.getLogger(__name__)

def load_configuration():
    with resources.path(configuration, 'log_config.yaml') as log_file_path:
        with open(log_file_path, 'r') as log_file_stream:
            try:
                log_config = yaml.full_load(log_file_stream)
                return log_config
            except yaml.YAMLError:
                logger.error("Error on loading log configuration")