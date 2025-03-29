import logging

from . import install

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
logger.debug("START: Install dart-sass by CLI")
install()
logger.debug("END: Install dart-sass by CLI")
