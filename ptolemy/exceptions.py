# -*- coding: utf-8 -*-

"""
ptolemy.exceptions

This module implements the exceptions for ptolemy.

"""


class PtolemyBaseError(Exception):
    """
    The base class which all ptolemy errors should inherit from. This allows
    the cli to easily catch all ptolemy errors.

    """


class InvalidFileError(PtolemyBaseError):
    """
    The file supplied does not exist.

    """
