from grovepi import *
import time
import requests
import yaml
from sensor_db import SensorData
from base import Session, engine, Base
import json

# using sqlalchemy to create db and table
Base.metadata.create_all(engine)

# opening db session
session = Session()

# loading configuration file
with open('config.yml', 'r') as c:
    conf = yaml.load(c)

# extracting config values from the config.yml file
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

# funtion to return temp/hum
def get_temp():
    [temp, hum] = dht(temp_port, 0)
    temp = {"temperature": temp, "humidity": hum}
    return temp

# function that reads from the ligth sensor and depend on the threshold set in the config will turn on/off the led
def get_light():

    sensor_value = analogRead(light_sensor)

    # Calculate resistance of sensor in K
    resistance = (float)(1023 - sensor_value) * 10 / (float)(sensor_value)

    if resistance > threshold:
        digitalWrite(led_port,1)
        led = 1
    else:
        digitalWrite(led_port,0)
        led = 0

    light = {"light": led, "light_intensity": resistance}
    return light

# function that adds readings into a python dictionary
def get_readings():
    payload = get_temp()
    payload.update(get_light())
    print(payload)
    return payload

# function that post reading to dweet.io
def post_dweet(url, payload):
    req = requests.post(url, json=payload)
    status = req.status_code
    return status

# function that retrieve the last posted reading from dweet.io
def get_dweet(dweet,device):
    get_url = dweet + device
    req = requests.get(get_url)
    res_body = json.loads(req.text)
    for item in res_body['with']:
        res = item['content']
    return res

# infinity loop where the main program will execute above funtions
while True:
    readings = get_readings()
    post = post_dweet(url, readings)

    # checking if the post was successfully
    if post is 200:
        print('reading posted')
    else:
        print('error porting readings')

    get_last_reading = get_dweet(dweet, device)

    # inserting sensor data into the db using sqlalchemy
    if get_last_reading:
        for sensor in get_last_reading:
            sensor_reading = SensorData(sensor, get_last_reading[sensor])
            session.add(sensor_reading)
            session.commit()
    else:
        print('error retrieving readings')

    # sleep time
    time.sleep(seconds)