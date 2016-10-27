#!/usr/local/bin/python
import os

import pytesseract
import sys
from tqdm import tqdm
from wand.image import Image
from PIL import Image as PI
import io

import pyocr
import pyocr.builders

def extract_pdf_pyocr(filepath):
    final_texts = []
    req_image = []

    print "Converting pdf to jpeg"
    image_pdf = Image(filename=filepath, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')

    for img in tqdm(image_jpeg.sequence, "Separating pages"):
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (lang))
    # Ex: Will use lang 'fra'
    # Note that languages are NOT sorted in any way. Please refer
    # to the system locale settings for the default language
    # to use.

    for img in tqdm(req_image, "Recognizing text"):
        txt = tool.image_to_string(
            Image.open('test.png'),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_texts.append(txt)


def extract_pdf(filepath):
    final_texts = []
    req_image = []

    print "Converting pdf to jpeg"
    image_pdf = Image(filename=filepath, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    
    for img in tqdm(image_jpeg.sequence, "Separating pages"):
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in tqdm(req_image, "Recognizing text"):
        txt = pytesseract.image_to_string(PI.open(io.BytesIO(img)))
        final_texts.append(txt)

    return final_texts

if __name__ == '__main__':
    error_message = "Usage: ./ocr.py <file_to_read.pdf> <destination_directory>"
    if len(sys.argv) < 3:
        sys.stderr.write(error_message)
    elif not sys.argv[1].endswith('.pdf'):
        sys.stderr.write(error_message)
    else:
        texts = extract_pdf(sys.argv[1])

        if not os.path.exists(sys.argv[2]):
            os.makedirs(sys.argv[2])

        page_num = 1
        for text in texts:
            file = open(sys.argv[2] + '/page_' + str(page_num) + '.txt', 'w+')
            file.write('\n' + text)
            file.close()
            page_num += 1