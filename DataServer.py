import socket
import threading

from ClientThread import ClientThread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))

server.settimeout(1)

server.listen()


class DataServerThread(threading.Thread):
    def __init__(self, event, data_queue, sock=None, address=None):
        super().__init__()
        self.data_queue = data_queue
        self.event = event
        self.client_socket = sock
        self.client_address = address

    def run(self):
        while True:
            if self.event.is_set():
                break

            try:
                self.client_socket, self.client_address = server.accept()
            except TimeoutError:
                continue

            newthread = ClientThread(self.client_address, self.client_socket, self.data_queue, self.event)
            newthread.start()
            newthread.join()
            self.client_socket.close()
