import zmq
import message_handler
from img_to_pdf import img_to_pdf
from server_enf import PORT

HANDLER_FUNCTIONS = {'img':img_to_pdf}
HANDLER_REQUIRED_FIELDS = ['type','payload']




class Server:
    def __init__(self, port:int):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

    def mainloop(self):
        msg_handler = message_handler.MessageHandler(HANDLER_FUNCTIONS, HANDLER_REQUIRED_FIELDS)

        while True:
            try:
                message = self.socket.recv_json()

                reply = msg_handler.generate_reply(message)

            except Exception as error:
                reply = {"status": "error", "payload": "Server error: " + str(error)}

            self.socket.send_json(reply)


if __name__ == "__main__":
    server = Server(PORT)
    server.mainloop()

