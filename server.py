import json
import datetime
import zmq
import message_handler
from img_to_pdf import img_to_pdf
from text_to_pdf import text_to_pdf
from server_env import PORT

HANDLER_FUNCTIONS = {'img': img_to_pdf, 'text': text_to_pdf}
HANDLER_REQUIRED_FIELDS = ['type', 'payload']


class Server:
    def __init__(self, port: int):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

    def mainloop(self):
        print("{date} - ZMQ REP/REQ server listening on port {port} :".format(date=datetime.datetime.now(),
                                                                              port=self.port))
        msg_handler = message_handler.MessageHandler(HANDLER_FUNCTIONS)

        while True:
            try:
                message = self.socket.recv_json()
                print("{date} - Message received :".format(date=datetime.datetime.now()))
                print(json.dumps(message, indent=4))

                reply = msg_handler.generate_reply(message)

            except Exception as error:
                print("{date} {error}".format(date=datetime.datetime.now(), error=error))
                reply = {"status": "error", "payload": str(error)}

            print("{date} - Sending reply:".format(date=datetime.datetime.now()))
            print(json.dumps(reply, indent=4))
            self.socket.send_json(reply)


if __name__ == "__main__":
    server = Server(PORT)
    server.mainloop()
