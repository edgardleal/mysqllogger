#/usr/env python
import __init__
import sys
from core import *
from optparse import OptionParser
from core.report import HtmlReport


parser = OptionParser(usage="run.sh [options]", version="0.0.0.2")

parser.add_option("-i", "--interval", dest="interval", \
              help="Set interval between queries", \
              action="store", default=2, type="int")

parser.add_option("-m", "--max", dest="iterations", \
              help="Max number of queries executed", default=5, type="int")

parser.add_option("-r", "--report", dest="report", \
    help="Generate html report", default=False, action="store_true")

options = parser.parse_args()

print options[0].report

if len(sys.argv) > 1:
  if sys.argv[1] == "test":
    import unittest
    import test
    # sys.path.insert(0, '../metadatabase') as metadatabase

    unittest.main()
  else:
    if options[0].report:
      _report = HtmlReport()
      _report.generate()
    else:
      mysqllogger.Monitor().start()
else:
  mysqllogger.Monitor().start()




