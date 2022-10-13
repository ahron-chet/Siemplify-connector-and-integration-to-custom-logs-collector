import sqlite3
import json
import ast
from openpyxl import Workbook
from os import getcwd
from os.path import isfile
import sqlite3
from ast import literal_eval
import smtplib
import ssl
from email.message import EmailMessage

class AllStat(object):

    def __init__(self,path):
        self.path = path
        assert(isfile(self.path))

    def extractData(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT Log FROM cases')
        data = cursor.fetchall()
        #conn.close()
        #cursor.close()
        return data


    def loadJson(self,data):
        jsonRes = []
        for i in data:
            try:
                jsonRes.append(ast.literal_eval(i[0]))
            except:
                pass
        return jsonRes


    def __getAllKeys__(self,jsonRes):
        k = []
        for i in jsonRes:
            keys = i.keys()
            for n in list(keys):
                if n not in k:
                    k.append(n)
        return k

    def genReport(self):
        wb = Workbook()
        ws = wb.active
        jsonRes = self.loadJson(self.extractData())
        k = self.__getAllKeys__(jsonRes)
        ws.append(k)
        for i in jsonRes:
            test = []
            for n in k:
                try:
                    test.append(i[n])
                except Exception as e:
                    test.append('     ---   ')
            ws.append(test)
        wb.save('statAll.xlsx')
        return getcwd()+'\\statAll.xlsx'


def isPasswordValid(password,sender):
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        mailserver.starttls()
        mailserver.login(sender, password)
        mailserver.close()
        return True
    except:
        return False

def send_excel(recipient_email, subject, content, sender, password):
    msg = EmailMessage()
    msg['Subject'], msg['From'], msg['To'] = subject,sender,recipient_email
    msg.set_content(content)
    with open(getcwd()+'\\statAll.xlsx', 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename='Report.xlsx')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

def main():
    path = input('Please enter full path to the database: ')
    print('Processing...')
    print('The full report is located on -> '+AllStat(path).genReport())
    recmail = input('To send the reasult to your mail account please enter your mail: ')
    if recmail:
        send_excel(recmail,'Full report.','Full report','reportexsel@gmail.com','vijrzfbwfymkkgcp')
        print('successfully completed!')


if __name__ == '__main__':
    main()