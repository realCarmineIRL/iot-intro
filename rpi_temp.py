from grovepi import *
import time
import requests
import json

port = 7

url = "https://dweet.io:443/dweet/for/test1-car-skerries-2019"

while True:
    [temp, hum] = dht(port, 0)
    r = requests.post(url, json={"temperature": temp, "humidity": hum})
    print(r.text)
    time.sleep(2)