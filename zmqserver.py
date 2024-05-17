import json
import datetime
import zmq
import message_handler


class ZMQServer:
    """
    Listens on designated port for incoming JSON objects, sends them to file handler for processing.
    """
    def __init__(self, port: int, handler_functions: dict) -> None:
        """
        :param port: Port for server to listen on [int]
        :param handler_functions: A dictionary of file_types:functions. The function will be used by the file handler
        to process incoming payloads
        """
        self.port = str(port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))
        self.message_handler = message_handler.MessageHandler(handler_functions)

    def mainloop(self):
        """
        Main logic loop. Run this method to start server.
        :return:
        """
        print("{date} - ZMQ REP/REQ server listening on port {port} :".format(date=datetime.datetime.now(),
                                                                              port=self.port))

        while True:
            try:
                message = self.socket.recv_json()
                print("{date} - Message received :".format(date=datetime.datetime.now()))
                print(json.dumps(message, indent=4))

                print("Converting payload...\n")
                reply = self.message_handler.generate_reply(message)
                print("{date} - Sending reply:".format(date=datetime.datetime.now()))
                print(json.dumps(reply, indent=4))

            except Exception as error:
                print("{date} Server error {error}".format(date=datetime.datetime.now(), error=error))
                reply = {"status": "error", "payload": "Server error: " + str(error)}

            self.socket.send_json(reply)


