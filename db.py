from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Float, Index, VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://tst1:1234@192.168.0.100:5432/ts_db')
base = declarative_base()


class DeviceData(base):
    __tablename__ = 'devicedata'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    deviceid = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    d_time = Column(DateTime, default=datetime.now)
    device_index = Index('device_index', deviceid, unique=False)


class Device(base):
    __tablename__ = 'device'
    deviceid = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
