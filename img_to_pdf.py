from PIL import Image


def img_to_pdf(payload, **kwargs) -> bytes:
    """
    Takes base64 encoded image file dump and converts to pdf.
    Returns base64 encoded file dump of resulting pdf file
    :param payload: Base64 encoded image file dump
    :return: Base64 encoded file dump of resulting pdf
    """

    with open("received_image.jpg", "wb+") as img_file:
        img_file.write(payload)
    image_to_convert = Image.open("received_image.jpg")
    image_to_convert.save("received_image.pdf", "PDF")
    with open("received_image.pdf", "rb") as pdf_data:
        return pdf_data.read()

