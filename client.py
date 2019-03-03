from sqlalchemy import create_engine
from base import Session
from sensor_db import SensorData
import yaml

with open('config.yml', 'r') as c:
    conf = yaml.load(c)

db_url = conf['DB']

engine = create_engine(db_url, echo=False)
session = Session()

data = session.query(SensorData).all()
for reading in data:
    print("%s : %s : %s" % (reading.sensor, reading.value, reading.create_date))