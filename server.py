import base64
import json

import zmq
import base64
class Server:
    def __init__(self, port:int=5555):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

    def mainloop(self):
        while True:
            message = self.socket.recv()
            decoded_message = base64.b64decode(message)
            print("Message received {}".format(decoded_message))
            self.socket.send(b"Hello")

if __name__ == "__main__":
    server = Server(5555)
    server.mainloop()

