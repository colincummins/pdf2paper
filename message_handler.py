import binascii
import base64


class UnrecognizedFileTypeError(Exception):
    """
    Raised when handler does not recognize value in the 'file_type' field
    """

    def __init__(self):
        self.message = f"File type not recognized"
        super().__init__(self.message)


class MissingPayloadError(Exception):
    """
    Raised when JSON message has no payload
    """

    def __init__(self):
        self.message = f"Message has no payload"
        super().__init__(self.message)


class PayloadNotBase64Error(Exception):
    """
    Raised when message payload cannot be decoded from base64
    """

    def __init__(self):
        self.message = f"Message payload cannot be decoded from base64"
        super().__init__(self.message)


class CantEncodePayloadError(Exception):
    """
    Raised when message payload cannot be encoded into base64
    """

    def __init__(self):
        self.message = f"Cannot encode payload into base64"
        super().__init__(self.message)


def decode_payload(message: dict) -> dict:
    """
    Decodes the 'payload' attribute of 'message' from base64
    :type message: [dict]
    :param message: Dict with 'payload' attribute of base64 encoded data [dict]
    :return: 'message' dict but with 'payload' decoded
    :except: PayloadNotBase64Error
    """
    try:
        message['payload'] = base64.b64decode(message['payload'])
        return message
    except binascii.Error:
        raise PayloadNotBase64Error


def encode_payload(message: dict) -> dict:
    """
    Encodes the 'payload' attribute of message into base64
    :param message: Dict with attribute 'payload' [dict]
    :return: Dict with updated payload attribute [dict]
    """
    try:
        message['payload'] = base64.b64encode(message['payload']).decode("utf-8")
        return message
    except binascii.Error:
        raise CantEncodePayloadError


class MessageHandler:
    """
    This class acts as a kind of router for incoming messages.
    It validates them, checks what file type the payload is, processes the payload according to that type, and
    composes a response JSON (or error JSON if an error occurs)
    """
    def __init__(self, string_to_func=None) -> None:
        """
        Constructor
        :param string_to_func: Dictionary of file_types and the functions we use to process payloads of that type [dict]
        """
        if string_to_func is None:
            self.function_dictionary = dict()
        else:
            self.function_dictionary = string_to_func

    def add_function(self, file_type: str, f: object) -> None:
        """
        Although we normally add file_type/function pairs at creation, we can add more with this function
        :param file_type: Type of file to be routed [str]
        :param f: Function to process the incoming file [function]
        :return: None
        """
        self.function_dictionary[file_type] = f

    def validate_json(self, message_json: dict) -> None:
        """
        Checks that file type can be handled by this handler
        """
        if message_json['type'] not in self.function_dictionary:
            raise UnrecognizedFileTypeError

    def generate_reply(self, message: dict):
        """
        Takes an incoming message, validates it, decodes payload, processes that payload according to file type,
        re-encodes payload to base64, then composes and sends a response with the
        processed payload (or an error response)
        :param message: JSON-type dict with at least a 'type' and 'payload' attribute, plus any others required by
        the file processing function [dict]
        :return:
        """
        try:
            self.validate_json(message)
            message = decode_payload(message)
            reply_payload = self.function_dictionary[message['type']](**message)
            reply = {"status": "ok", "payload": reply_payload}
            reply = encode_payload(reply)
        except (UnrecognizedFileTypeError, MissingPayloadError, PayloadNotBase64Error, CantEncodePayloadError) as error:
            reply = {"status": "error", "payload": error.message}
        except KeyError as error:
            reply = {"status": "error", "payload": "JSON object missing required field" + str(error)}
        except Exception as error:
            reply = {"status": "error", "payload": "Server error: " + str(error)}
        finally:
            return reply
