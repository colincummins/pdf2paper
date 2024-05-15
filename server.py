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
    handler: object | None

    def __init__(self, port: int, msg_handler: message_handler.MessageHandler):
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))
        self.handler: message_handler.MessageHandler = msg_handler

    def mainloop(self):
        print("{date} - ZMQ REP/REQ server listening on port {port} :".format(date=datetime.datetime.now(),
                                                                              port=self.port))

        while True:
            try:
                message = self.socket.recv_json()
                print("{date} - Message received :".format(date=datetime.datetime.now()))
                print(json.dumps(message, indent=4))

                reply = self.handler.generate_reply(message)

            except Exception as error:
                print("{date} {error}".format(date=datetime.datetime.now(), error=error))
                reply = {"status": "error", "payload": str(error)}

            print("{date} - Sending reply:".format(date=datetime.datetime.now()))
            print(json.dumps(reply, indent=4))
            self.socket.send_json(reply)


if __name__ == "__main__":
    handler: message_handler.MessageHandler = message_handler.MessageHandler()
    for filetype, f in HANDLER_FUNCTIONS.items():
        handler.add_function(filetype, f)
    server = Server(PORT, handler)
    server.mainloop()
