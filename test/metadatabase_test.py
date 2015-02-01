

import random
import unittest
import sys
import os
from core import *
# sys.path.insert(0, '../metadatabase') as metadatabase
# from core import logfactoy

metadatabase.database_name = 'test.db'


class DataBaseTest(unittest.TestCase):

  logger = logfactory.getLogger("DataBaseTest")
  def setUp(self):
    self.logger.debug("Stating databasetest")
    try:
      os.remove(metadatabase.database_name)
      self.logger.debug("Database test.db was removed")
    except OSError as e:
      self.logger.debug("Database test.db not exists")

  def tearDown(self):
    try:
      os.remove(metadatabase.database_name)
    except OSError as e:
      self.logger.error(str(e))

  def test_command_persist(self):
    c = mysqllogger.Command("XXX", "root", "localhost", "test.db", "running", 4, "Select *")
    self.assertTrue(c != None, "Command object is assigned")
    self.assertFalse(c.existsInDataBase(), "This command shold not exists in database")
    c.saveToDataBase()
    self.assertTrue(c.existsInDataBase(), "This command shold exists in database")

  def test_execution_persist(self):
    c = mysqllogger.Execution(2014, 11, 2, 7777, 0)
    self.assertTrue(c != None, "Execution object shold be assigned")


  def runTest(self):
    # self.__openconnection()
    # self.command_persist_test()
    return ""

  def test_openconnection(self):
    self.logger.debug("Testing connection to database")
    try:
      with metadatabase.MetaDataBase() as db:
        con = db.getCon()
        self.logger.debug("Testing if connection is assigned")
        self.assertFalse(con == None, "Connection is assigned")


    except Exception as ex:
      self.logger.error("Error connecting to database: [%s]" % (str(ex)))
      self.assertTrue(False)

