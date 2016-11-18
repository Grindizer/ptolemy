# -*- coding: utf-8 -*-

"""
ptolemy.cli

This module implements the CLI for ptolemy.

"""

import argparse
import logging
import sys

from jsonschema.exceptions import ValidationError

from . import __version__
from .source import Source
from .exceptions import PtolemyBaseError


def parse_arguments(args):
    """
    Parse the arguments supplied to ptolemy.

    :returns: argparse.Namespace

    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--debug", action="store_true",
        default=False, help="enable debug logs"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version="ptolemy version {0}".format(__version__)
    )
    parser.add_argument("source", help="path to the source file")

    return parser.parse_args(args)


def setup_logger(debug):
    """
    Setup logging.

    :param debug: A boolean specifying whether the debug level should be set \
    to debug or critical
    :type debug: bool
    :returns: logging.Logger()

    """
    level = logging.DEBUG if debug else logging.CRITICAL
    logging.basicConfig(
        format="[%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level
    )
    return logging.getLogger(__name__)


def main():
    """
    Run ptolemy.

    """
    arguments = parse_arguments(sys.argv[1:])
    logger = setup_logger(arguments.debug)

    try:
        source = Source(arguments.source)
        mapping_table = source.compile()
    except PtolemyBaseError as error:
        logger.exception(error)
        sys.exit(error)
    except ValidationError as error:
        logger.exception(error)
        sys.exit(
            "The source file could not be validated. {0}".format(error.message)
        )
    else:
        sys.stdout.write(mapping_table + "\n")


if __name__ == "__main__":
    main()  # pragma: no cover
