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

def read_pdf(filepath):
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

def main(pdf_path, result_directory):
    texts = read_pdf(pdf_path)

    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    page_num = 1
    for text in texts:
        file = open(result_directory + '/page_' + str(page_num) + '.txt', 'w+')
        file.write('\n' + text)
        file.close()
        page_num += 1

if __name__ == '__main__':
    error_message = "Usage: ./ocr.py <file_to_read.pdf> <destination_directory>"
    if len(sys.argv) < 3:
        sys.stderr.write(error_message)
    elif not sys.argv[1].endswith('.pdf'):
        sys.stderr.write(error_message)
    else:
        main(sys.argv[1], sys.argv[2])