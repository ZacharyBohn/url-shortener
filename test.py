"""
Run this file to run all tests in the test directory.
Test file names must start with test_
Test files must use unittest by
-creating a class that inherits from unittest.TestCase
-and that class starts with Test

Use the command: python tests.py
to run this file
"""

# This is necessary to set the correct path
# when the tests are running. The path should be
# the project root, but when the tests start normally
# the path is the project folder, so imports don't work.
#
# This patches python so that imports will work across the app.
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import unittest

loader = unittest.TestLoader()
tests = loader.discover('tests', pattern='test_*.py')

unittest.TextTestRunner().run(tests)
