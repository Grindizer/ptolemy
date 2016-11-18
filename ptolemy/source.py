# -*- coding: utf-8 -*-

"""
ptolemy.source

This module implements the source functionality.

"""

import logging
import os

from jsonschema import validate
import yaml

from .exceptions import InvalidFileError
from .mapping import Mapping


class Source(object):  # pylint: disable=too-few-public-methods
    """Source reads in the source file, and implements the functionality to
    compile it to a DMS Mapping Table.

    :param source_file_path: Path to the source file.
    :type source_file_path: str

    """

    def __init__(self, source_file_path):
        self.logger = logging.getLogger(__name__)
        self.file_path = os.path.join(os.getcwd(), source_file_path)
        self.source = None

    def compile(self):
        """Compiles the source file to a valid DMS Mapping Table document.

        :param source_file_path: The path to the YAML source.
        :type source_file_path: str
        :returns: str
        :raises: ptolemy.exceptions.InvalidFileError

        """
        if not os.path.isfile(self.file_path):
            raise InvalidFileError(
                "The supplied source file '{0}' does not exist.".format(
                    self.file_path
                )
            )

        with open(self.file_path, "r") as source_file:
            self.source = yaml.safe_load(source_file)

        self._validate()

        return self._generate_mapping().to_json()

    def _validate(self):
        """Checks the user-defined source is correctly formatted.

        :raises: jsonschema.exceptions.ValidationError

        """
        source_schema_file_path = os.path.join(
            os.path.dirname(__file__), "data", "source-schema.yaml"
        )
        with open(source_schema_file_path, "r") as source_schema_file:
            source_schema = yaml.safe_load(source_schema_file)

        validate(self.source, source_schema)

    def _generate_mapping(self):
        """Returns the DMS Mapping Table.

        :param selection_data: The raw data used to build the selection rules
        :type selection_data: dict
        :returns: list

        """
        mapping = Mapping()
        rules = self._get_rules()
        mapping.mapping["rules"] = rules
        return mapping

    def _get_rules(self):
        """Return a list of un-numbered, unnamed DMS rules.

        :returns: list

        """
        rules = []
        for rule_type, rule_type_data in self.source.items():
            for rule_action, rule_action_data in rule_type_data.items():
                for data_item in rule_action_data:
                    object_locators = data_item["object-locators"]

                    object_locations = \
                        self._get_object_locations(object_locators)

                    for object_location in object_locations:
                        rule = {
                            "object-locator": object_location,
                            "rule-action": rule_action,
                            "rule-type": rule_type
                        }

                        rule.update({
                            k: v for k, v in data_item.items()
                            if k != "object-locators"
                        })
                        rules.append(rule)
        return rules

    @staticmethod
    def _get_object_locations(object_locators):
        """Return all combinations of schema, table and column names.

        object_locators should take the format:
        {
            "schema_names": [<schema_name>, ...]
            "table_names": [<table_name>, ...]
            "column_names": [<column_name>, ...]
        }

        :param object_locators: A dictionary of SQL object locators.
        :type object_locators: dict
        :returns: dict

        """
        # Get all combinations of schema, table and column names. If any key
        # isn't present, add None to the object_locations. This is to get the
        # list comp working. None values are then removed.
        object_locations = [
            {
                "schema-name": schema_name,
                "table-name": table_name,
                "column-name": column_name
            }
            for schema_name in object_locators.get(
                "schema-names", [None]
            )
            for table_name in object_locators.get(
                "table-names", [None]
            )
            for column_name in object_locators.get(
                "column-names", [None]
            )
        ]
        object_locations = [
            {
                k: v
                for k, v in object_location.items()
                if v is not None
            }
            for object_location in object_locations
        ]
        return object_locations
