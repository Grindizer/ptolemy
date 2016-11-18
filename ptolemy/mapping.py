# -*- coding: utf-8 -*-

"""
ptolemy.mapping

This module implements the mapping functionality.

"""

import json


class Mapping(object):  # pylint: disable=too-few-public-methods
    """Mapping stores information about the DMS Mapping Table.

    """

    def __init__(self):
        self.mapping = {"rules": []}

    def to_json(self):
        """
        Return the JSON mapping.

        :returns: str

        """
        self._number_rules()
        return json.dumps(
            self.mapping, indent=4, sort_keys=True, separators=(',', ': ')
        )

    def _number_rules(self):
        """
        Add rule-id and rule-names to each rule. Rules are numbered from 1,
        as per AWS examples.
        """
        for i, rule in enumerate(self.mapping["rules"]):
            rule_number = str(i + 1)
            rule["rule-id"] = rule_number
            rule.setdefault("rule-name", rule_number)
