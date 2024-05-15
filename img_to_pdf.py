from PIL import Image


def img_to_pdf(payload, **kwargs) -> bytes:
    """
    Converts an image into a pdf.
    :param payload: Image data. JPG, PNG, and other PIL library formats accepted. [bytes]
    :param kwargs: Unused arguments
    :return: Image converted to PDF [bytes]
    """

    with open("received_image.jpg", "wb+") as img_file:
        img_file.write(payload)
    image_to_convert = Image.open("received_image.jpg")
    image_to_convert.save("received_image.pdf", "PDF")
    with open("received_image.pdf", "rb") as pdf_data:
        return pdf_data.read()

