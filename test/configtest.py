
from unittest import TestCase
from core import *
import os

class ConfigTest(TestCase):

  def setUp(self):
    self.logger = logfactory.getLogger("ConfigTest")
    self.config_file = ""

  def test_default_file_create(self):
    x = os.getenv("HOME") + "/.mysqllogger"
    self.config_file = x
    print self.config_file
    os.remove(self.config_file)
    self.config = config.Config()
    self.assertTrue(os.access(self.config_file, os.R_OK), "config file shold exists")

  def runTest(self):
    return "ConfigTest"




