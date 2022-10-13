import os
import sqlite3
from filterLogs import FilterLogs

class SqlRep(object):

    def __init__(self):
        self.path = FilterLogs.temp()+os.sep+'data.db'

    def creatDataBase(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS cases(Id integer primary key autoincrement, EventType varchar(255), Sourceuuid varchar(255), customerid int(11), Occured date, severity varchar(255),Action varchar(255),ipv4 varchar(255),HostName varchar(255),VTdetect varchar(255), VTvendors varchar(255), VTurl text, Log text, Time date)")
        conn.commit()
        c.close()
        conn.close()

    def data_entry(self,tupleVal,dbpath):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        c.execute("""INSERT INTO cases('customerid', 'EventType', 'Sourceuuid', 'Occured', 'severity', 'Action', 'ipv4' ,'HostName', 'VTdetect', 'VTvendors', 'VTurl', 'Log', 'Time')
                VALUES"""+str(tupleVal)+";")
        conn.commit()
        c.close()
        conn.close()
