import requests
from os.path import basename
def getDatabase(url,path):
    return requests.post(url,files = {basename(path): open(path,'rb').read()})

if __name__=='__main__':
    url = input('Enter url: ')
    path = input('Enter path: ')
    print(getDatabase(url,path))