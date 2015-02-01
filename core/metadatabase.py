# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
from logfactory import getLogger

con = None

database_name = 'data.db'

class MetaDataBase():

  con = None
  logger = None

  def __init__(self):
    self.logger = getLogger(__name__)

  def __enter__(self):
    return self

  def close(self):
    if self.con != None:
      self.logger.debug("Closing metadatabase connection")
      self.con.close()
      self.con = None

  def __exit__(self, *args):
    self.logger.debug("Exiting object")
    self.close()

  def __del__(self):
    self.logger.debug("Deleting object")
    self.close()

  def version(self):
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()
    cur.close()
    print "SQLite version: %s" % data

  def getCon(self):
    if self.con != None:
      return self.con

    try:

       self.con = lite.connect(database_name)
       self.logger.debug("connecting to database [%s]" % (database_name))
       self.con.cursor().execute("""
          create table if not exists queries(id text primary key, sql text, example text);
       """)
       self.con.cursor().execute("""
          create table if not exists executions(id text primary key,
                                               pid int,
                                               query text,
                                               time int,
                                               year int,
                                               month int,
                                               day int,
                                               hour int,
                                               minute int,
                                               second int,
                                               timestamp number);
          """)

       self.con.cursor().execute("""
              create index if not exists ix_executions_pid on executions(pid, year, month, day);
                  """)

       return self.con
    except lite.Error as e:
      print "Error connecting to metadabase"
      self.logger.error("Error Connecting to database [%s]" % (str(e)))
      print "Error %s:" % e.args[0]
      sys.exit(1)



