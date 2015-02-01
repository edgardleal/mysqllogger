

from metadatabase_test import DataBaseTest
from configtest import ConfigTest
import unittest


def suite():
  suite = unittest.TestSuite()
  suite.addTest(DataBaseTest())
  suite.addTest(ConfigTest())
  return suite


unittest.TextTestRunner(verbosity=2).run(suite())

