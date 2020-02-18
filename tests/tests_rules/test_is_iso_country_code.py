"""Module for test class of OSIValidationRules class"""

import unittest
from osivalidator.osi_rules_checker import OSIRulesChecker


class TestIsIsoCountryCode(unittest.TestCase):
    def setUp(self):
        self.FRC = OSIRulesChecker()

    def tearDown(self):
        del self.FRC

    def test_comply_iso_country_code(self):
        self.assertTrue(self.FRC.is_iso_country_code("DEU", None))

    def test_not_comply_iso_country_code(self):
        self.assertFalse(self.FRC.is_iso_country_code("1234", None))
