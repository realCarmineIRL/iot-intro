from grovepi import *
import time
import requests
import yaml
from sensor_db import SensorData
from base import Session, engine, Base

Base.metadata.create_all(engine)

session = Session()

with open('config.yml', 'r') as c:
    conf = yaml.load(c)

url = conf['URL']
port = conf['GROVEPIPORT']
seconds = conf['SECONDS']

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
    readings = get_readings()
    post = post_dweet(url, readings)

    if post is 200:
        print('reading posted')
    else:
        print('error porting readings')

    temperature = SensorData('temperature', readings['temperature'])
    humidity = SensorData('humidity', readings['humidity'])
    session.add(temperature)
    session.add(humidity)
    session.commit()
    
    data = session.query(SensorData).all()
    for reading in data:
        print("%s : %s : %s" % (reading.sensor, reading.value, reading.create_date))
    time.sleep(seconds)