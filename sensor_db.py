import datetime
from sqlalchemy import Column, String, Integer, DateTime

from base import Base

class SensorData(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    sensor = Column(String)
    value = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, sensor, value):
        self.sensor = sensor
        self.value = value