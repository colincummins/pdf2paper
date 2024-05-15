from PIL import Image
import base64


def img_to_pdf(payload, **kwargs) -> str:
    """
    Takes base64 encoded image file dump and converts to pdf.
    Returns base64 encoded file dump of resulting pdf file
    :param payload: Base64 encoded image file dump
    :return: Base64 encoded file dump of resulting pdf
    """

    with open("received_image.jpg", "wb+") as img_file:
        img_file.write(base64.b64decode(payload))
    image_to_convert = Image.open("received_image.jpg")
    image_to_convert.save("received_image.pdf", "PDF")
    with open("received_image.pdf", "rb") as pdf_data:
        encoded_pdf = base64.b64encode(pdf_data.read()).decode('utf-8')
    return encoded_pdf
