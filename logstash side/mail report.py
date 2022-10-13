import os
import time
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from getpass import getpass


class MailReport(object):
    
    def __init__(self,sendr,password,to,path):
        self.sendr = sendr
        self.password = password
        self.to = to
        self.path = path
        
    def __load_excel__(self,subject, content):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sendr
        msg['To'] = self.to
        msg.set_content(content)
        with open(self.path, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=file_data)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
            smtp.login(self.sendr, self.password)
            smtp.send_message(msg)
            
    def sendReport(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y")
        time_string = now.strftime("%d/%m/%Y/%H:%M:%S")
        subject = 'Report ESET for'+dt_string
        content = 'Report '+time_string
        self.send_excel(subject,content)
    

   
            
if __name__=="__main__":
    sender = input('Enter your mail account: ')
    to = input('Enter mail account to send: ')
    password = getpass('Enter mail passeord: ')
    path = input('Enter path to logs file')
    MailReport(sender,to,password,path).sendReport()