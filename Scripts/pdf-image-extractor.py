"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

import sys
import PyPDF2
from PyPDF2.filters import _xobj_to_image


def main(pdf: str):
    reader = PyPDF2.PdfFileReader(pdf)
    page = reader.pages[30]

    if "/XObject" in page["/Resources"]:
        xObject = page["/Resources"]["/XObject"].getObject()

        for obj in xObject:
            if xObject[obj]["/Subtype"] == "/Image":
                extension, byte_stream = _xobj_to_image(xObject[obj])
                if extension is not None:
                    filename = obj[1:] + ".png"
                    with open(filename, "wb") as img:
                        img.write(byte_stream)
    else:
        print("No image found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: python {} input_file\n".format(sys.argv[0]))
        sys.exit(1)

    pdf = sys.argv[1]
    main(pdf)
