import socket
import threading
import time
from cryptography import RSA_encryption, AES_encryption
import os
from filterLogs import FilterLogs
import sys


class Server(object):
    
    def __init__(self):
        self.Port = 9211
        self.serverIP = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.serverIP,self.Port))
        self.rsa = RSA_encryption()
        self.prvt = open(os.getcwd()+os.sep+'certs'+os.sep+'public.pem','rb').read()
        self.fl = FilterLogs()


    def rcv_key(self,conn,addr):
        key = self.aes.randomKey()
        conn.send(self.rsa.rsa_encryt(key))
        cipher = AES_encryption(key)
        if self.sync(conn,addr):
            return cipher
       

    def sync(conn,addr):
        while True:
            m = conn.recv(1)
            if m==b'r':
                return True

    def listen_for_connection(self):
        #print('{+}Server listening...')
        self.server.listen()
        while True:
            conn,addr=self.server.accept()
            host,_=addr
            #print('{+}New connection '+str(host))
            t=threading.Thread(target=self.connection,args=(conn,addr,host))
            t.start()
            #connection(conn,addr,host)


    def connection(self,conn,addr,host):
        cipher = self.rcv_key(conn,addr)
        return self.start(conn,addr,host,cipher)



    def sendMessage(self,message,conn,addr,cipher):
        message = cipher.encrypt_data_aes(message)
        conn.send(str(len(message)).encode())
        if self.sync(conn,addr):
            conn.send(message)
        if self.sync(conn,addr):
            return True

    def listenRcv(self,conn,addr,cipher):
        c = 0
        while True:
            try:
                header=int(conn.recv(64).decode().strip())
                if len(str(header))>0:
                    conn.send(b'r')
                    msg=conn.recv(header)
                    if len(msg)>0:
                        return self.cipher.decrypt_data_aes(msg)
            except Exception as e:
                c+=1
                time.sleep(0.5)
                if c >= 100:
                    return 'No connction Exception'
                pass



    def start(self,conn,addr,host,cipher):
        file = '/root/home/logsEset.log'
        while True:
            m = self.listenRcv(conn,addr,cipher)
            if m == 'No connction Exception':
                break
            if m == b'get logs':
                try:
                    with open(file,'rb')as f:
                        logs =  f.read()
                    os.remove(file)
                except Exception as e:
                    #print(e)
                    logs = False                                                                        
                try:
                    if logs:
                        message = self.fl.filterSeverity(self.parseToJson(logs.decode()))
                    else:
                         message = '[]'
                    self.sendMessage(message.encode(),conn,addr,cipher)
                    conn.close()
                    break
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    test = (exc_type, fname, exc_tb.tb_lineno)
                    print(str(test))
                    #print(str(logs))
            time.sleep(0.5)

if __name__=='__main__':
    Server().listen_for_connection()
    
