
from SiemplifyConnectors import SiemplifyConnectorExecution
from SiemplifyConnectorsDataModel import AlertInfo
from SiemplifyUtils import output_handler,unix_now
import ast
import socket
import datetime
import time
from cryptography.fernet import Fernet
from base64 import b64encode
from hashlib import sha256
import json
import random
import ast



class Client(object):
    
    def __init__(self,password):
        self.Port = 9211
        self.server = '20.106.132.201'
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.server,self.Port))
        self.keyencrypt = b64encode(password)
        self.password = password
        self.fer = Fernet(self.keyencrypt)

    def sync(self):
        while True:
            m = self.client.recv(1)
            if m==bytes([114]):
                return True

    def send_key(self):
        self.client.send(self.fer.encrypt(self.password))
        return self.sync()
    

    def sendMessage(self,message):
        message = self.fer.encrypt(message)
        self.client.send(str(len(message)).encode())
        if self.sync():
            self.client.send(message)
        return True

    def rscvlogs(self):
        header = int(self.client.recv(64).decode().strip())
        #print(header)
        if len(str(header)) > 0:
            self.client.send(bytes([114]))
            msg = bytes()
            while len(msg) < header:
                msg += self.client.recv(header)
                if len(msg) == header:
                    break
            self.client.send(bytes([114]))
            if len(msg)>0:
                return(self.fer.decrypt(msg))
        else:
            raise Exception ('encorrect header')
            


class Connector(object):
    
    def __init__(self,connectorName,vendor,ruleGen):
        self.connectorName = connectorName
        self.vendor = vendor
        self.severitys = {"Information":10, "Warning":50, "Critical":80, "Fatal":100}
        self.defaultSeverity=60
        self.RULE_GENERATOR_EXAMPLE = ruleGen


    def create_alert(self,siemplify, testAlert,datetime_in_unix_time,created_event):
        siemplify.LOGGER.info(f"-------------- Started processing Alert {testAlert['event_type']}")
        alert_info = AlertInfo()
        alert_info.display_id = str(random.randint(2,1000000000000))
        alert_info.ticket_id = testAlert['source_uuid']
        alert_info.name = testAlert['event_type']
        alert_info.rule_generator = testAlert['event_type']
        alert_info.start_time = datetime_in_unix_time 
        alert_info.end_time = datetime_in_unix_time 
        alert_info.priority = self.severitys[testAlert['severity']]
        alert_info.device_vendor = self.vendor
        alert_info.device_product = self.vendor 
        siemplify.LOGGER.info(f"---------- Events creating started for alert  {testAlert['event_type']}")
        try:
            if created_event:
                alert_info.events.append(created_event)
            siemplify.LOGGER.info(f"Added Event {testAlert['source_uuid']} to Alert {testAlert['source_uuid']}")
        except Exception as e:
            siemplify.LOGGER.error(f"Failed to process event {testAlert['source_uuid']}")
            siemplify.LOGGER.exception(e)
        return alert_info

    def create_event(self,siemplify,testAlert,datetime_in_unix_time):
        siemplify.LOGGER.info(f"--- Started processing Event:  alert_id: {testAlert['source_uuid']} | event_id: {testAlert['source_uuid']}")
        event = {}
        keys = list(testAlert.keys())
        event["StartTime"] = datetime_in_unix_time 
        event["EndTime"] = datetime_in_unix_time
        for i in keys:
            event[i]=testAlert[i]
        siemplify.LOGGER.info(f"--- Finished processing Event: alert_id: {testAlert['source_uuid']} | event_id: {testAlert['source_uuid']}")
        return event



    @output_handler
    def start(self,is_test_run):
        alerts = [] 
        siemplify = SiemplifyConnectorExecution()
        siemplify.script_name = self.connectorName 
        password = siemplify.extract_connector_param("password", default_value=None, input_type=bytes, is_mandatory=True, print_value=False)
        password = sha256(password).digest()

        if (is_test_run):
            clientside = Client(password)        
            clientside.send_key()
            clientside.sendMessage(bytes((103,101,116,32,108,111,103,115)))
            logs = clientside.rscvlogs()

            if len(logs) > 0:
                for i in ast.literal_eval(logs.decode(errors='replase')):
                    try:
                        datetime_in_unix_time = time.mktime(datetime.datetime.now().timetuple())
                    except:
                        datetime_in_unix_time = unix_now()
                    created_event = self.create_event(siemplify,i,datetime_in_unix_time)
                    created_alert = self.create_alert(siemplify,i, datetime_in_unix_time, created_event)
                    if created_alert is not None:
                        alerts.append(created_alert)
                        siemplify.LOGGER.info(f"Added Alert {i['event_type']} to package results")

        else: 
             siemplify.LOGGER.info(f"False")

        siemplify.return_package(alerts)

if __name__ == "__main__":
    Connector().start(True)
    
