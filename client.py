from sqlalchemy import create_engine
from base import Session
from sensor_db import SensorData

engine = create_engine('sqlite:///sensors.db:memory:', echo=True)

session = Session()

data = session.query(SensorData).all()
for reading in data:
    print("%s : %s : %s" % (reading.sensor, reading.value, reading.create_date))