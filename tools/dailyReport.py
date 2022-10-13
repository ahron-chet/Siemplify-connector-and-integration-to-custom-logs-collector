import sqlite3
from ast import literal_eval
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, date
from getpass import getpass
import time
from openpyxl import Workbook
import pytz



class DailyReport(object):

    def __init__(self):
        self.fields = ['Event Type','Source uuid','Occured','Severity','Action','Action Taken','Ipv4','Host-Name','VT detect','VT Vendors','VT url','Log','Time']
        self.alertfield = ['event_type','source_uuid','occured','severity','action','action_taken','ipv4','hostname','VTdetect','VTvendors','VTurl','Time']
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(self.fields)
        self.database = '/home/elastic/ahronConnector/other1.db'
        self.savePath = '/home/elastic/ahronConnector/dailyReport.xlsx'
        self.externalFields = 'VTdetect, VTurl, VTvendors, Time'

    def getdatat(self):
        c = sqlite3.connect(self.database)
        curr = c.cursor()
        sql = "SELECT log, "+self.externalFields+" FROM cases WHERE Time BETWEEN '"+str(date.today())+" 07:00:00' AND '"+str(date.today())+" 17:00:00'"
        curr.execute(sql)
        fetchLst = curr.fetchall()
        curr.close(),c.close()
        return self.__jsonParser__(fetchLst)

    def __fixJson__(self,dictionary,fetchLst):
        f, c = self.externalFields.split(', '), 0
        for i in fetchLst[1:]:
            dictionary[f[c]] = i
            c+=1
        return dictionary

    def __jsonParser__(self,fetchLst):
        jsonres = []
        for i in fetchLst:
            jsonres.append(self.__fixJson__(literal_eval(i[0]),i))
        return jsonres


    def __get_relevant_fields__(self,dictionary):
        res = []
        for i in self.alertfield:
            try:
                res.append(dictionary[i])
            except Exception as e:
                if i == 'action':
                        try:
                            t.append(i['action_taken'])
                        except:
                            res.append('      ---')
                else:
                    res.append('     ---')
                pass
        return res

    def getOriginLog(self,dictionary):
        for i in self.externalFields.split(', '):
            try:
                del dictionary[i]
            except:
                pass
        return dictionary

    def report(self,recipient_email, subject, content, sender, password):
        totaldata = self.getdatat()
        if len(totaldata)<1:
            return
        for i in totaldata:
            reldata = self.__get_relevant_fields__(i)
            tows = reldata[:-1]+[str(self.getOriginLog(i))]+[reldata[-1]]
            self.ws.append(tows)
        self.wb.save(self.savePath)
        self.__send_excel__(recipient_email, subject, content, sender, password)


    def __send_excel__(self,recipient_email, subject, content, sender, password):
        msg = EmailMessage()
        msg['Subject'], msg['From'], msg['To'] = subject,sender,recipient_email
        msg.set_content(content)
        with open(self.savePath, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename='Report.xlsx')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

def isPasswordValid(password,sender):
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        mailserver.starttls()
        mailserver.login(sender, password)
        mailserver.close()
        return True
    except:
        return False

def main():
    sendTime = input('Please enter an hour that you would like to automatically send email (24 hours formmat): ').strip()
    timeZone = input('Please enter time Zone (EX: Asia/Jerusalem): ').strip()
    sender = input('Please enter email account of the sender: ').strip()
    password = getpass('Please enter password of the sender email: ').strip()
    assert(isPasswordValid(password,sender))
    recipient_email = input('Please enter recipient email account: ').strip()
    subject = input('Please enter the subject of the mail \n(to add current time in the subject type -t in the current position EX: daily Report -t)\n: ').strip()
    content = input("Please enter the content of the mail \n(to add current time in the subject type -t in the current position EX: daily Report -t)\n: ").strip()
    if '-t' in subject:
        subject = subject.replace('-t',str(datetime.now())[:-7])
    if '-t' in content:
        content = content.replace('-t',str(datetime.now())[:-7])
    zone = pytz.timezone(timeZone)

    while True:
        if datetime.now(zone).strftime('%H') in sendTime:
            DailyReport().report(recipient_email, subject, content, sender, password)
            print('Successfully completed.')
        else:
            time.sleep(60)

if __name__ == "__main__":
    main()