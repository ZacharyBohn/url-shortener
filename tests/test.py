"""
Run this file to run all tests in the test directory.
Test file names must start with test_
Test files must use unittest by
-creating a class that inherits from unittest.TestCase
-and that class starts with Test

Use the command: python tests.py
to run this file
"""
import unittest

loader = unittest.TestLoader()
integration_tests = loader.discover('integration_tests', pattern='test_*.py')
unit_tests = loader.discover('unit_tests', pattern='test_*.py')

suite = unittest.TestSuite([integration_tests, unit_tests])

unittest.TextTestRunner().run(suite)
