import zmq
import base64

class TestClient:
    def __init__(self, address: str = "localhost", port: int = 5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, port))

    def mainloop(self):
        with open("longcat.jpg", "rb") as image_file:
            encoded_message = base64.b64encode(image_file.read()).decode('utf-8')
        message = {"type": "img", "payload": encoded_message}
        self.socket.send_json(message)

        reply:dict = self.socket.recv_json()
        print(reply)

        with open("longcat.pdf", "wb+") as pdf_file:
            decoded_file = base64.b64decode(reply['payload'])
            pdf_file.write(decoded_file)
        print("PDF received")


if __name__ == "__main__":
    client = TestClient("localhost", 5555)
    client.mainloop()
