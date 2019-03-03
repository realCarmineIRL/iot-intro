from grovepi import *
import time
import requests
import yaml
from sensor_db import SensorData
from base import Session, engine, Base
import json

Base.metadata.create_all(engine)

session = Session()

with open('config.yml', 'r') as c:
    conf = yaml.load(c)

url = conf['URL']
port = conf['GROVEPIPORT']
seconds = conf['SECONDS']
device = conf['DEVICE_NAME']
dweet = conf['DWEET']

def get_readings():
    [temp, hum] = dht(port, 0)
    payload = {"temperature": temp, "humidity": hum}
    return payload

def post_dweet(url, payload):
    req = requests.post(url, json=payload)
    status = req.status_code
    return status

def get_dweet(dweet,device):
    get_url = dweet + device
    req = requests.get(get_url)
    res_body = json.loads(req.text)
    for item in res_body['with']:
        res = item['content']
    return res

while True:
    readings = get_readings()
    post = post_dweet(url, readings)

    if post is 200:
        print('reading posted')
    else:
        print('error porting readings')

    get_last_reading = get_dweet(dweet, device)

    if get_last_reading:
        for sensor in get_last_reading:
            sensor_reading = SensorData(sensor, get_last_reading[sensor])
            session.add(sensor_reading)
            session.commit()
    else:
        print('error retrieving readings')

    time.sleep(seconds)