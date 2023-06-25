import json
import queue
import threading

import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

from Message import DataMessage
from db import engine, Device, DeviceData


class DataProcessThread(threading.Thread):
    def __init__(self, event, data_queue):
        super().__init__()
        self.db_session = sessionmaker(bind=engine)()
        self.data_queue = data_queue
        self.event = event

    def run(self):
        while True:
            if self.event.is_set():
                break

            try:
                data = self.data_queue.get(timeout=1)
            except queue.Empty:
                continue

            if type(data) is DataMessage:
                try:
                    data_db = DeviceData(deviceid=data.devid, temperature=data.temperature, humidity=data.humidity)
                    self.db_session.add(data_db)
                    self.db_session.commit()
                    print('successful commit DeviceData')
                except sqlalchemy.exc.IntegrityError:
                    print('error in table Device')

                try:
                    if not self.db_session.query(Device).get(data.devid):
                        device_db = Device(deviceid=data.devid)
                        self.db_session.add(device_db)
                        self.db_session.commit()
                        print('successful commit Device')
                except sqlalchemy.exc.IntegrityError:
                    print('error in table DeviceData')
            else:
                try:
                    new_json = json.loads(data)
                except json.decoder.JSONDecodeError:
                    print('wrong json')
                    break
                new_json = DataMessage(new_json)
                self.data_queue.put(new_json)
