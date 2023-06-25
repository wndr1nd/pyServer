import threading

import paho.mqtt.client as mqtt


class MqttSub(threading.Thread):
    def __init__(self, data_queue, event):
        super().__init__()
        self.data_queue = data_queue
        self.event = event

    def run(self):
        subscriber = mqtt.Client('test1')
        subscriber.on_message = self.on_message
        subscriber.on_disconnect = self.on_disconnect
        subscriber.connect('192.168.0.100')
        while True:
            if self.event.is_set():
                break
            subscriber.loop_start()
            subscriber.subscribe('/data')
            subscriber.loop_stop()
        subscriber.disconnect()

    def on_message(self, client, userdata, message):
        self.data_queue.put(message.payload.decode("utf-8"))

    @staticmethod
    def on_disconnect(client, userdata, flags, rc=0):
        print('Disconnect code ' + str(rc))
