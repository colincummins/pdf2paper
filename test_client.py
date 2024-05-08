import json
import zmq
import base64
class TestClient:
    def __init__(self,address:str="localhost", port:int=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, port))

    def mainloop(self):
        for i in range(10):
            message = input("Enter message:")
            encoded_message = base64.b64encode(bytes(message, 'utf-8'))
            self.socket.send(encoded_message)
            print(self.socket.recv())


if __name__ == "__main__":
    client = TestClient("localhost", 5555)
    client.mainloop()

