import json
import datetime
import zmq
import message_handler


class ZMQServer:
    def __init__(self, port: int, handler_functions: dict) -> None:
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))
        self.message_handler = message_handler.MessageHandler(handler_functions)

    def mainloop(self):
        print("{date} - ZMQ REP/REQ server listening on port {port} :".format(date=datetime.datetime.now(),
                                                                              port=self.port))

        while True:
            try:
                message = self.socket.recv_json()
                print("{date} - Message received :".format(date=datetime.datetime.now()))
                print(json.dumps(message, indent=4))

                reply = self.message_handler.generate_reply(message)
                print("{date} - Sending reply:".format(date=datetime.datetime.now()))
                print(json.dumps(reply, indent=4))

            except Exception as error:
                print("{date} Server error {error}".format(date=datetime.datetime.now(), error=error))
                reply = {"status": "error", "payload": "Server error: " + str(error)}

            self.socket.send_json(reply)


