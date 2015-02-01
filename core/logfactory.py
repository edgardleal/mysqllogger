

import logging

logging.basicConfig(filename="mysqllogger.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def getLogger(name):
  return logging.getLogger(name)

