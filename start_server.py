import queue
import threading
import time


from DataProcess import DataProcessThread
from DataServer import DataServerThread
from mqtt_sub import MqttSub

data_queue = queue.Queue()

event = threading.Event()

MQT = MqttSub(data_queue, event)
DTP = DataProcessThread(event, data_queue)
DTS = DataServerThread(event, data_queue)

MQT.start()
DTS.start()
DTP.start()
print('start')
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        event.set()
        break


if event.is_set():
    DTS.join()
    DTP.join()
    print('thread stop')
    MQT.join()
    print('exit')

