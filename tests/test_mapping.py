# -*- coding: utf-8 -*-

import unittest

from mock import patch, sentinel

from ptolemy.mapping import Mapping


class MappingTestCase(unittest.TestCase):

    def setUp(self):
        self.mapping = Mapping()

    def test_init(self):
        self.assertEqual(self.mapping.mapping, {"rules": []})

    @patch("ptolemy.mapping.Mapping._number_rules")
    def test_to_json(self, mock_number_rules):
        expected_response = """{
    "rules": []
}"""
        response = self.mapping.to_json()
        self.assertEqual(response, expected_response)

    def test_number_rules_with_rule_with_no_name(self):
        self.mapping.mapping["rules"] = [
            {
                "rule-action": "selection"
            }
        ]
        expected_rules = [
            {
                "rule-action": "selection",
                "rule-id": "1",
                "rule-name": "1"
            }
        ]
        self.mapping._number_rules()
        self.assertEqual(self.mapping.mapping["rules"], expected_rules)

    def test_number_rules_with_rule_with_name(self):
        self.mapping.mapping["rules"] = [
            {
                "rule-action": "selection",
                "rule-name": sentinel.rule_name
            }
        ]
        expected_rules = [
            {
                "rule-action": "selection",
                "rule-id": "1",
                "rule-name": sentinel.rule_name
            }
        ]
        self.mapping._number_rules()
        self.assertEqual(self.mapping.mapping["rules"], expected_rules)
