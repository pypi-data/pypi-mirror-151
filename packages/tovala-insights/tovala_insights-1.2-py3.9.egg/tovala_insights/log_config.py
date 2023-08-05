import yaml
import logging

logger = logging.getLogger(__name__)

def load_configuration():
    with open('log_config.yaml', 'r') as log_file_stream:
        try:
            log_config = yaml.full_load(log_file_stream)
            return log_config
        except yaml.YAMLError:
            logger.error("Error on loading log configuration")