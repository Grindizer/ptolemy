# -*- coding: utf-8 -*-

import argparse
import logging
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

from mock import patch, sentinel
from jsonschema import exceptions as jsonschema_exceptions

from ptolemy import cli
from ptolemy import exceptions as ptolemy_exceptions


class CliTestCase(unittest.TestCase):

    def test_parse_arguments_with_source_file(self):
        arguments = cli.parse_arguments(["source_file"])
        assert arguments.source == "source_file"
        assert arguments.debug is False

    def test_parse_arguments_with_debug_flag(self):
        arguments = cli.parse_arguments(["-d", "source_file"])
        assert arguments.source == "source_file"
        assert arguments.debug is True

    def test_setup_logger_without_debug_flag(self):
        logger = cli.setup_logger(False)
        assert isinstance(logger, logging.Logger)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("ptolemy.cli.Source")
    @patch("ptolemy.cli.setup_logger")
    @patch("ptolemy.cli.parse_arguments")
    def test_main_with_valid_source(
            self, mock_parse_arguments, mock_setup_logger,
            mock_Source, mock_stdout
    ):
        mock_parse_arguments.return_value = \
            argparse.Namespace(debug=False, source=sentinel.source)
        mock_Source.return_value.compile.return_value = '{"rules": []}'

        cli.main()
        self.assertEqual(mock_stdout.getvalue(), '{"rules": []}\n')

    @patch("ptolemy.cli.Source")
    @patch("ptolemy.cli.setup_logger")
    @patch("ptolemy.cli.parse_arguments")
    def test_main_with_mock_non_existant_file(
            self, mock_parse_arguments, mock_setup_logger,
            mock_Source
    ):
        mock_parse_arguments.return_value = \
            argparse.Namespace(debug=False, source=sentinel.source)
        mock_Source.return_value.compile.side_effect = \
            ptolemy_exceptions.InvalidFileError()

        with self.assertRaises(SystemExit):
            cli.main()

    @patch("ptolemy.cli.Source")
    @patch("ptolemy.cli.setup_logger")
    @patch("ptolemy.cli.parse_arguments")
    def test_main_with_mock_invalid_source(
            self, mock_parse_arguments, mock_setup_logger,
            mock_Source
    ):
        mock_parse_arguments.return_value = \
            argparse.Namespace(debug=False, source=sentinel.source)
        mock_Source.return_value.compile.side_effect = \
            jsonschema_exceptions.ValidationError(sentinel.message)

        with self.assertRaises(SystemExit):
            cli.main()


if __name__ == "__main__":
    unittest.main()
