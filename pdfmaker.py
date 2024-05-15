"""
To set up a pdfmaker microservice, set PORT and run this file
"""
from zmqserver import ZMQServer

# Import any functions you want the server to be able to run on payloads
from img_to_pdf import img_to_pdf
from text_to_pdf import text_to_pdf

# Keys are file types the message handler can route to the corresponding function for processing
HANDLER_FUNCTIONS = {'img': img_to_pdf, 'text': text_to_pdf}

# Port for server to listen on
PORT = 5555


if __name__ == "__main__":
    srv = ZMQServer(PORT, HANDLER_FUNCTIONS)
    srv.mainloop()

