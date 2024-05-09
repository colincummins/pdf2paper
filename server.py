import base64
import json

import zmq
import base64
from PIL import Image

def message_to_json(message:str)->dict:
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {'status': 'error', 'payload': 'Message is not JSON'}
    except:
        return {'status': 'error', 'payload': 'Something went wrong'}



class Server:
    def __init__(self, port:int=5555):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

    def mainloop(self):
        while True:
            message = self.socket.recv()
            message = message_to_json(message)
            if message['status'] == 'error':
                print("Malformed message")
            else:
                with open("received_image.jpg","wb+") as img_file:
                    img_file.write(base64.b64decode(message['payload']))
                image_to_convert = Image.open("received_image.jpg")
                image_to_convert.save("received_image.pdf","PDF")
                with open("received_image.pdf", "rb") as pdf_data:
                    encoded_pdf = base64.b64encode(pdf_data.read())

                message = {"status": "success", "payload": encoded_pdf}

            self.socket.send_string(json.dumps(message))

if __name__ == "__main__":
    server = Server(5555)
    server.mainloop()

