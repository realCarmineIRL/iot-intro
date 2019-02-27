from grovepi import *
import time

port = 7

while True:
    [temp, hum] = dht(port, 0)
    print "temp: %s, hum: %s" % (temp, hum)
    time.sleep(2)