# -*- coding: utf-8 -*-

import tempfile
import unittest

from mock import Mock, patch, sentinel

from jsonschema.exceptions import ValidationError

from ptolemy.exceptions import InvalidFileError
from ptolemy.source import Source


class SourceTestCase(unittest.TestCase):

    def setUp(self):
        self.source = Source("file/path")

    @patch("ptolemy.source.os.getcwd")
    def test_init(self, mock_getcwd):
        mock_getcwd.return_value = "/path/"
        source = Source("file.yaml")
        self.assertEqual(source.file_path, "/path/file.yaml")
        self.assertEqual(source.source, None)

    def test_compile_with_invalid_file(self):
        self.source.file_path = "/this/file/does/not.exist"
        with self.assertRaises(InvalidFileError):
            self.source.compile()

    @patch("ptolemy.source.Source._generate_mapping")
    @patch("ptolemy.source.Source._validate")
    def test_compile_with_valid_file(
            self, mock_validate, mock_generate_mapping
    ):
        mock_mapping = Mock()
        mock_mapping.to_json.return_value = sentinel.mapping
        mock_generate_mapping.return_value = mock_mapping
        with tempfile.NamedTemporaryFile() as f:
            self.source.file_path = f.name
            mapping = self.source.compile()
        self.assertEqual(self.source.source, None)
        self.assertEqual(mapping, sentinel.mapping)

    def test_validate_with_valid_source(self):
        self.source.source = {
            "selection": {
                "include": [
                    {
                        "object-locators": {
                            "schema-names": ["Test"],
                            "table-names": ["%"]
                        }
                    }
                ]
            }
        }
        self.source._validate()

    def test_validate_with_invalid_source(self):
        self.source.source = {
            "selection": {
                "incorrect-key": []
            }
        }
        with self.assertRaises(ValidationError):
            self.source._validate()

    @patch("ptolemy.source.Source._get_rules")
    @patch("ptolemy.source.Mapping")
    def test_generate_mapping(self, mock_Mapping, mock_get_rules):
        mock_Mapping.return_value.mapping = {}
        mock_get_rules.return_value = sentinel.rules

        mapping = self.source._generate_mapping()
        self.assertEqual(mapping.mapping, {"rules": sentinel.rules})

    def test_get_rules(self):
        # This is not a very thorough test. It assumes that Source.source
        # is correctly formed, which is fair given the source will have
        # previously been validated with Source._validate. More extensive tests
        # of this area of code are carried out in the integration tests.
        self.source.source = {
            "selection": {
                "include": [
                    {
                        "object-locators": {
                            "schema-names": ["Test"],
                            "table-names": ["%"]
                        }
                    }
                ]
            }
        }
        expected_rules = [
            {
                "object-locator": {
                    "schema-name": "Test",
                    "table-name": "%"
                },
                "rule-action": "include",
                "rule-type": "selection"
            }
        ]

        rules = self.source._get_rules()
        self.assertEqual(rules, expected_rules)

    def test_get_object_locations(self):
        # See comment in test_get_rules().
        object_locators = {
            "schema-names": ["s1", "s2"],
            "table-names": ["t1", "t2"],
            "column-names": ["c1", "c2"]
        }
        expected_object_locations = [
            {"column-name": "c1", "schema-name": "s1", "table-name": "t1"},
            {"column-name": "c2", "schema-name": "s1", "table-name": "t1"},
            {"column-name": "c1", "schema-name": "s1", "table-name": "t2"},
            {"column-name": "c2", "schema-name": "s1", "table-name": "t2"},
            {"column-name": "c1", "schema-name": "s2", "table-name": "t1"},
            {"column-name": "c2", "schema-name": "s2", "table-name": "t1"},
            {"column-name": "c1", "schema-name": "s2", "table-name": "t2"},
            {"column-name": "c2", "schema-name": "s2", "table-name": "t2"}
        ]
        object_locations = self.source._get_object_locations(object_locators)

        self.assertEqual(object_locations, expected_object_locations)
