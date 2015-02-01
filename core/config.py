

import os
import json
from logfactory import getLogger

class Config(object):
  """
    Load configuration from json file
  """

  def __init__(self):
    self.logger = getLogger(__name__)
    self.config_file = os.getenv("HOME") + "/.mysqllogger"
    if not  os.access(self.config_file, os.R_OK):
      self.logger.debug("Config file not found")
      self.values = {'host' : 'localhost', 'database' : 'mysql', 'dbport' : '3306' \
           ,'user' : 'root', 'password' : ''}

      with open(self.config_file, 'w') as f:
        json.dump(self.values, f)

    else:
      with open(self.config_file, 'r') as f:
        self.values = json.load(f)
      self.logger.debug("Config file loaded")


  def __done__(self):
    print "Done"

  def _doctest(self):
    import doctest
    doctest.testmod()

  def __str__(self):
    return "Arquivo de configuracao"


config = Config()
values = config.values
