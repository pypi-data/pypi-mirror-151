from sys import exc_info
import yaml
import logging
import logging.config
from .log_config import load_configuration

log_config = load_configuration()

def configure_logging(log_config):
    if log_config:
        try:
            logging.config.dictConfig(log_config)
            logger = logging.getLogger(__name__)
        except (ValueError, TypeError, AttributeError, RuntimeError):
            logger.exception("Exception occured while configuring logging: ", exc_info = True)
    else:
        logger.error("Error on getting log configuration")

    return logger