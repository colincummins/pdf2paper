import base64
from fpdf import FPDF


def text_to_pdf(payload, font="Courier", size="12", left="20", top="20", right="-1", **kwargs) -> str:
    """
    Converts text file to pdf
    Adapted from https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/

    :param payload: Base64 encoded text
    :param font: Font [str]
    :param size: Font size [str]
    :param image_data: Json with Base64 encoded image file dump as 'payload'
    :return: Base64 encoded file dump of resulting pdf
    """

    with open("temp_text_file", "wb+") as txt:
        txt.write(base64.b64decode(payload))
    with open("temp_text_file", "r") as txt:
        pdf = FPDF()
        pdf.set_margins(float(left), float(top), float(right))
        pdf.add_page()
        pdf.set_font(font, size=int(size))
        # insert the texts in pdf
        for x in txt:
            pdf.cell(200, 10, txt=x, ln=1, align='L')

        # save the pdf with name .pdf
        pdf.output("temp.pdf")

    with open("temp.pdf", "rb") as temp:
        payload = base64.b64encode(temp.read()).decode('utf-8')
    return payload
