import argparse
import logging

from . import installer

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("--clean", action="store_true", default=False)
parser.add_argument("--os", default=None, type=str)
parser.add_argument("--arch", default=None, type=str)

logging.basicConfig(level=logging.DEBUG)

logger.debug("START: Install dart-sass by CLI")

args = parser.parse_args()
if args.clean:
    installer.clean()
if args.os and args.arch:
    installer.install(os_name=args.os, arch_name=args.arch)
else:
    installer.install()
logger.debug("END: Install dart-sass by CLI")
