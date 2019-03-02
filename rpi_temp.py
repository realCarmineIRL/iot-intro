from grovepi import *
import time
import requests
import yaml

with open('config.yml', 'r') as c:
    conf = yaml.load(c)

url = conf['URL']
port = conf['GROVEPIPORT']

def get_readings():
    [temp, hum] = dht(port, 0)
    payload = {"temperature": temp, "humidity": hum}
    return payload

def post_dweet(url, payload):
    req = requests.post(url, json=payload)
    status = req.status_code
    print(req.text)
    return status

while True:
    post = post_dweet(url, get_readings())
    if post is 200:
        print('reading posted')
    else:
        print('error porting readings')
    time.sleep(300)