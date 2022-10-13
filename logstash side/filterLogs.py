import os
from openpyxl import Workbook
import threading
import requests
import random
from datetime import datetime
import time
import pytz
import sqlite3
from VT import VirusScannerVT
from sql import SqlRep

class FilterLogs(object):

    def __init__(self):
        self.fields = ['Event Type','Source uuid','Occured','Severity','Action','Ipv4','Host-Name','VT detect','VT Vendors','VT url','Log','Time']
        self.alertfield = ['event_type','source_uuid','occured','severity','action','ipv4','hostname']
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(self.fields)
        self.path = self.temp()+'Report.xlsx'
        self.apikey = 'e08d3ae2419f5a7f27b37db6adaf27b6d31d06d1c522b71d9b0ad8f25b542702'
        self.zone = pytz.timezone('Asia/Jerusalem')


    def temp(self):
        try:
            os.remove(os.getcwd()+os.sep+'Report'+os.sep+'Report.xlsx')
        except:
            pass
        try:
            os.mkdir(os.getcwd()+os.sep+'Report'+os.sep)
        except FileExistsError:
            pass
        return os.getcwd()+os.sep+'Report'+os.sep

    def isVTpositive(self,jsonData):
        detect = False
        try:
            h = jsonData['hash']
            try:
                detect = VirusScannerVT(self.apikey).scanHash(h)
            except Exception as e:
                pass
        except:
            pass
        return detect


   

    def __filteruuid__(db,uuid):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = '''SELECT EventType FROM cases WHERE datetime(Time) >=datetime('now', '-30 Minute')
                and Sourceuuid = "'''+uuid+'"'
        cursor.execute(sql)
        if len(cursor.fetchall())<1:
            return False
        return True

    def filterSeverity(self,lst):
        nlst = []
        for i in lst:
            if i['severity'] == 'Critical' or i['severity'] == 'Fatal':
                try:
                    t = i['object_uri']
                    if 'file' in t[:6]:
                        t = str(t).replace('\\\\','\\')
                        t = t.split('\\')
                        n = []
                        for j in t:
                            if len(j)<1:
                                pass
                            else:
                                n.append(j)
                        if len(n)<=2:
                            continue
                except:
                    pass
                if i['event_type'] == 'Threat_Event':
                    if not self.__filteruuid__(SqlRep().path,i['source_uuid']):
                        continue
                nlst.append(i)

        t=threading.Thread(target=self.report,args=([lst]))
        t.start()
        return str(nlst)

    def report(self,jsonlst):
        if not os.path.isfile(self.path):
            self.path = self.temp()+'Report.xlsx'
        for i in jsonlst:
            t = []
            for n in self.alertfield:
                try:
                    t.append(i[n])
                except:
                    if n == 'action':
                        try:
                            t.append(i['action_taken'])
                        except:
                            t.append(' ')
                    else:
                        t.append(' ')
                    time.sleep(0.09)
            try:
                d = self.isVTpositive(i)
                if d:
                    keys = list(d.keys())
                    t.append(len(keys))
                    t.append(' ,'.join(keys))
                    t.append('https://www.virustotal.com/gui/file/'+i['hash'])
                else:
                    t.append(' ')
                    t.append(' ')
                    t.append(' ')
            except Exception as e:
                print(e)
                t.append(' ')
                t.append(' ')
                t.append(' ')
            t.append(str(i))
            t.append(str(datetime.now(self.zone).strftime('%Y-%m-%d %H:%M:%S')))
            self.ws.append(t)
        self.wb.save(self.path)
        self.wb.save(self.path)
        SqlRep().data_entry(tuple([121]+t),'other1.db')

