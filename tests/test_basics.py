import unittest
from flask import current_app
from basics import BasicsTestCase

class SimpleTestCase(BasicsTestCase):
    def test_app_is_in_test_mode(self):
        self.assertTrue(current_app.config.get('TESTING'))
    