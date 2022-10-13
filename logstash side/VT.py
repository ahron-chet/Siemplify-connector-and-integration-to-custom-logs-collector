import requests
import random


class VirusScannerVT(object):

    def __init__(self,apiKey):
        self.apiKey=apiKey
        self.alterKeys = [
                     "8dd0c36fd4ef57dc1effd53d580a2d2c4413c65041abcc103fe60641dc001ea4",
                     "a2b51c4511a5da05b595cc57e57aad2428db72ed28d66d9c72ca394f6ce47963",
                     "e08d3ae2419f5a7f27b37db6adaf27b6d31d06d1c522b71d9b0ad8f25b542702",
                      self.apiKey
                      ]
        assert(self.isKeyValid(self.apiKey))

    def __spldate__(self,update):
        return update[:4]+':'+update[4:6]+':'+update[6:]

    def isKeyValid(self,key):
        params = {'apikey': self.apiKey}
        r=requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
        if r.status_code==200:
            return True
        return False

    def __sortDetected__(self,jsonRes):
        detected={}
        for i in jsonRes.keys():
            if jsonRes[i]['detected'] == True:
                isMalware=True
                detected[i]={'version':jsonRes[i]['version'],'result':jsonRes[i]['result'],'update':self.__spldate__(jsonRes[i]['update'])}
        return detected



    def scanHash(self,h,key=False):
        if not key:
            params = {'apikey': self.alterKeys[random.randint(0,3)], 'resource': h}
        else:
            params = {'apikey': key, 'resource': h}
        c=0
        while True:
            url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
            if url.status_code==200:
                res=url.json()
                break
            elif url.status_code==204:
                print(True)
                params = {'apikey': self.alterKeys[c], 'resource': h}
            if c==3:
                c=0
            else:
                c+=1
        if res['positives'] > 0:
            return self.__sortDetected__(res['scans'])
        return False