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
temp_port = conf['TEMP_PORT']
led_port = conf['LED_PORT']
pinMode(led_port, "OUTPUT")
light_sensor = conf['LIGHT_SENSOR_PORT']
pinMode(light_sensor, "INPUT")
threshold = conf['LIGHT_THRESHOLD']
seconds = conf['SECONDS']
device = conf['DEVICE_NAME']
dweet = conf['DWEET']

def get_temp():
    [temp, hum] = dht(temp_port, 0)
    temp = {"temperature": temp, "humidity": hum}
    return temp

def get_light():

    sensor_value = analogRead(light_sensor)

    # Calculate resistance of sensor in K
    resistance = (float)(1023 - sensor_value) * 10 / sensor_value

    if resistance > threshold:
        led = digitalWrite(led_port,1)
    else:
        led = digitalWrite(led_port,0)
    light = {"light": led, "light_intensity": resistance}
    return light

def get_readings():
    payload = get_temp()
    payload.update(get_light())
    print(payload)
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