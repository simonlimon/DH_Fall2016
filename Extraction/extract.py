#!/usr/local/bin/python

import sys

import ocr
import parsing

def main(pdf_path, result_dir):
    ocr.main(pdf_path, result_dir)
    df = parsing.parse_directory(result_dir)
    df.to_csv(result_dir + '/result.csv')

if __name__ == '__main__':
    error_message = "Usage: ./extract.py <file_to_read.pdf> <destination_directory>"
    if len(sys.argv) < 3:
        sys.stderr.write(error_message)
    elif not sys.argv[1].endswith('.pdf'):
        sys.stderr.write(error_message)
    else:
        main(sys.argv[1], sys.argv[2])