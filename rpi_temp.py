from grovepi import *
import time

port = 7

while True:
    [temp, hum] = dht(port, 1)
    print "temp: %s, hum: %s" % (temp, hum)
    time.sleep(2)