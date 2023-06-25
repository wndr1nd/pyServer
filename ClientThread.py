import json
import socket
import threading

from Message import DataMessage, AbstractMessage


class ClientThread(threading.Thread):
    def __init__(self, address=None, sock=None, data_queue=None, event=None):
        super().__init__()
        self.event = event
        self.data_queue = data_queue
        self.client_socket = sock
        self.address = address
        print(f'Подключение {self.address}')

    def run(self):
        while True:
            if self.event.is_set():
                break

            try:
                msg = self.client_socket.recv(4096)
            except socket.error:
                print('alarm')
                break

            try:
                print(self.address)
                data = msg.decode('utf-8')
            except AttributeError:
                print('need encode')
                break

            try:
                json_data = json.loads(data)
            except json.decoder.JSONDecodeError:
                print('что-то с json')
                break

            print(AbstractMessage(json_data))
            new_data = DataMessage(json_data)
            self.data_queue.put(new_data)
