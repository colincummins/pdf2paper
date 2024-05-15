from fpdf import FPDF


def text_to_pdf(payload, font="Courier", size="12", left="20", top="20", right="-1", **kwargs) -> bytes:
    """
    Convert text to pdf
    :param payload: Plaintext to convert. User must include newlines if they want wrapping
    :param font: Font [str]
    :param size: Font size [str]
    :param left: Left Margin in cm [str]
    :param top: Top Margin in cm [str]
    :param right: Right Margin [str]
    :param kwargs: Unprocessed keywords [str]
    :return: Bytes dump of PDF version of the text, right justified [bytes]
    """

    with open("temp_text_file", "wb+") as txt:
        txt.write(payload)
    with open("temp_text_file", "r") as txt:
        pdf = FPDF()
        pdf.set_margins(float(left), float(top), float(right))
        pdf.add_page()
        pdf.set_font(font, size=int(size))
        # insert the texts in pdf
        for x in txt:
            pdf.cell(200, 10, txt=x, ln=1, align='L')

        # Return as a byte stream. The 'latin-1' encoding is per PyPDF instructions for coercing output to bytes
        return pdf.output(dest="S").encode('latin-1')
