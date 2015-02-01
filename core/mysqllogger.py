#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql.connector
import time as tim
from datetime import date
import os
import sys
import metadatabase
import re
import md5
import sqlite3 as lite
import sys
import base64
import report
from logfactory import getLogger
import config

cnx = None

class Execution():

  def __init__(self, year, month, day, pid, time):
    if year & month & day & pid:
      self.key   = "%s%s%s%d" % (self.year, self.month, self.day, self.pid)
    self.year = year
    self.month= month
    self.day  = day
    self.time = time
    self.pid  = pid

  def loadFromDataBase(self):
    sql = "Select * from executions where "

class Command:
  pid       = ""
  user      = ""
  host      = ""
  db        = ""
  status    = ""
  time      = 0
  sql       = ""
  clearsql  = ""
  key       = ""
  timestamp = tim.time()
  localtime = tim.localtime(timestamp)
  year      = localtime[0]
  month     = localtime[1]
  day       = localtime[2]
  hour      = localtime[3]
  minute    = localtime[4]
  second    = localtime[5]
  md5       = ""
  variablePattern = re.compile(r"(\d+(\.\d+)?)|('[^']*')")
  con = None
  metaDatabase = None

  def __init__(self, pid, user, host, db, status, time, sql):
    self.pid   = pid
    self.user  = user
    self.host  = host
    self.db    = db
    self.status= status
    self.time  = time
    self.sql   = sql
    self.key   = "{0}{1}{2}{3}".format(self.year, self.month, self.day, self.pid)
    self.metaDatabase = metadatabase.MetaDataBase()
    self.con = self.metaDatabase.getCon()

    self.clearsql = self.puresql()
    _md5 = md5.new()
    _md5.update(self.clearsql)
    self.md5 = base64.b64encode(_md5.digest())
    self.variablePattern = re.compile(r"(\d+(\.\d+)?)|('[^']*')")
    self.scape_pattern   = re.compile(r"([^'])'([^'])")

  def existsInDataBase(self):
    c = self.con.cursor()
    result = False
    c.execute("Select 1 from queries where id = '{0}'".format(self.md5))
    r = c.fetchall()
    result = len(r) != 0
    c.close()
    return result

  def save_execution(self):
    update = """
      update executions set time = ?
      where id = ?
    """
    insert = "insert into executions(id, pid, query, time, year,month,day,hour, minute, second, timestamp) values('{0}',?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(self.key)

    c2 = self.con.cursor()
    if self.execution_exists():
      c2.execute(update, (self.time, self.key,))
    else:
      c2.execute(insert, (self.pid, self.md5, self.time, self.year, self.month, self.day, self.hour, self.minute, self.second, self.timestamp,))
    self.con.commit()

  def saveToDataBase(self):
    command = ""
    if (self.sql == "show full processlist") | (self.sql == "null"):
      return
    if not self.existsInDataBase():
      try:
        command = "insert into queries(id, sql, example) values(? , ? , ?)"
        c = self.con.cursor()
        c.execute(command, (self.md5, self.clearsql, self.scapeSQL(self.sql),))
        c.close()

        self.con.commit()
      except lite.Error as ex:
        print "Erro ao executar o comando: [%s]" % command
        print ex.args[0]
        print self._str_()
        sys.exit(1)

  def execution_exists(self):
    c = self.con.cursor()
    c.execute("Select 1 from executions where id = ?",(self.key,))
    r = c.fetchone()
    return r != None

  def scapeSQL(self, sql):
    if sql:
      return self.scape_pattern.sub("''", sql)
    else:
      return "null"

  def dispose(self):
    self.con = None
    self.metaDatabase.close()

  def __exit__(self):
    self.dispose()

  def puresql(self):
    if self.sql:
      return self.variablePattern.sub("?", self.sql)
    else:
      return "null"

  def _str_(self):
    return """pid={0}
              user={1}
              host={2}
              time={3}
              db={4}
              sql={5}""".format(self.pid, self.user, self.host, self.time, self.db,  self.puresql())

  def writeToFile(self):
    with open("sql/{0}".format(self.pid), "w") as f:
      f.write(self._str_())


commands = {}

def appendCommand(c):
  commands[c.pid] = c

def getCommand(pid):
  return commands[pid]

checkCommand = lambda pid: commands[pid]




class Monitor():
  count = 0
  logger = getLogger(__name__)

  def __init__(self):
    self.cnx = mysql.connector.connect(user= config.values["user"],
                              password= config.values["password"],
                              host    = config.values["host"],
                              database= config.values["database"])

  def start(self):

    self.logger.debug("Stating monitor")
    db = metadatabase.MetaDataBase()
    try:
      while True:
        self.count = self.count + 1
        if self.count == options.iterations:
          break
        os.system("clear")
        cursor = self.cnx.cursor()
        cursor.execute("""
                   show full processlist
                       """)
        result = cursor.fetchall()
        for i in result:
          c = None
          if i[7] == None:
            continue
          try:
            c = checkCommand(i[0])
            c.time = i[4]
          except Exception:
            c = Command(i[0], i[1], i[2], i[3], i[4],i[5], i[7])

          c.con = db.getCon()
          commands[c.pid] = c
          c.saveToDataBase()
          c.save_execution()
          del c
          print i[0], i[5], i[2]
        tim.sleep(options.interval);
    finally:
      if self.cnx:
        self.cnx.close()
      db.close()
