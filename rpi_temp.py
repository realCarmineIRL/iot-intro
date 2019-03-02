from grovepi import *
import time
import requests
import json

port = 7

url = "https://dweet.io:443/dweet/for/test1-car-skerries-2019?content="

while True:
    [temp, hum] = dht(port, 0)
    payload = '{"temperature": "%s", "humumidity": "%s"}' % (temp, hum)
    print(json.dumps(payload))
    r = requests.post(url + payload)
    print(r.text)
    time.sleep(2)