import base64
import json

import zmq
import base64
from PIL import Image
class Server:
    def __init__(self, port:int=5555):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

    def mainloop(self):
        while True:
            message = self.socket.recv()
            with open("received_image.jpg","wb+") as img_file:
                img_file.write(base64.b64decode(message))
            image_to_convert = Image.open("received_image.jpg")
            image_to_convert.save("received_image.pdf","PDF")
            with open("received_image.pdf", "rb") as pdf_data:
                encoded_pdf = base64.b64encode(pdf_data.read())

            self.socket.send(encoded_pdf)

if __name__ == "__main__":
    server = Server(5555)
    server.mainloop()

