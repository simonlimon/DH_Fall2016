# coding=utf-8
import os

import pandas as pd
import re
import roman
import glob


### ------- helpers for data retrieval ------- ###

def get_num(text):
    num_strings = re.findall(r'\A\d+\s?\d+', text)
    if len(num_strings) == 0:
        print 'Number not found: ' + text
        return None
    num_string = num_strings[0]
    num_string = num_string.replace(' ', '')
    num = int(re.sub(r'\D', "", num_string))
    return num

def get_site(text):
    strings = re.findall(r'Sk.|Dh.|Bm.|Jl.|Mm.|Jn.|Kn.|Gr.|Bl.', text)
    if len(strings) == 0:
        print 'Place not found: ' + text
        return None
    site_string = strings[0]
    return site_string[:-1]

def get_year(text):
    strings = re.findall(r'’\d\d', text)
    if len(strings) == 0:
        print 'Year not found: ' + text
        return None
    string = strings[0]
    year_string = '19' + string[3:]
    return year_string

def get_block(text):
    strings = re.findall(r'Block .|Trench [A-Z]\d+, .|T\d', text)
    if len(strings) == 0:
        print 'Block not found: ' + text
        return None
    string = strings[0]
    block_string = string.replace('Block ', '').replace('Trench ', 'T-')
    return block_string

def square_list(text):
    strings = []
    split_text = text.split("; ")
    for item in split_text:
        if "sq. " in item:
            strings.append(item)
    return strings    

def get_raw_square(text):
    #couldn't find regex of proper sensitivity. best I got was
    #re.findall(r'sq. \d+.?\d+.?', text)
    strings = square_list(text)
    if len(strings) == 0:
        return None
    all_squares = ""
    for i in range(len(strings)):
        s = strings[i]    
        s = s.replace('sq. ', '')
        all_squares += s + ", "
    return all_squares[:-2]

def get_square(text):
    raw_squarelist = square_list(text)
    if len(raw_squarelist) == 0:
        return None
    squarelist = []
    xystring = ""
    for raw_square in raw_squarelist:
        raw_square = raw_square.replace(" ", "")
        square = re.findall(r'\d+.\d+',raw_square)
        if len(square) >= 1:
            for squarestring in square:
                coord = re.split("\D",squarestring)
                xystring += "(%s,%s),"%(coord[0],coord[1])
    return xystring[:-1]

def get_first_XY(text): #return the first X,Y
    raw_squarelist = square_list(text)
    if len(raw_squarelist) == 0:
        return None
    xystring = ""
    for raw_square in raw_squarelist:
        raw_square = raw_square.replace(" ", "")
        square = re.findall(r'\d+.\d+',raw_square)
        if len(square) >= 1:
            for squarestring in square:
                coord = re.split("\D",squarestring)
                return coord

def get_stratum(text):
    strings = re.findall(r'stratum \w{1,3}', text)
    if len(strings) == 0:
        print 'Stratum not found: ' + text
        return None
    string = strings[0]
    string = string.replace('1', 'I').replace('stratum ', '')
    return str(roman.fromRoman(string))

def get_plate(text):
    strings = re.findall(r'\(P[l1]\..*?\)', text)
    if len(strings) == 0:
        print 'Plate not found: ' + text
        return None
    plates = ""
    for i in range(len(strings)):
        s = strings[i]
        s = re.sub(r'Pl. |P1. |no. |[()]', '', s)
        s = s.replace(', ', '-')
        if s[-1] == '.': s = s[:-1]
        plates += s.strip() + ", "
    plates = plates[:-2] #remove last ", "
    return plates

### ------------------------------------------ ###

def parse_entry(text, _class):

    entry = pd.Series()

    entry.name = get_num(text)
    entry['site'] = get_site(text)
    entry['year'] = get_year(text)
    entry['block'] = get_block(text)
    entry['stratum'] = get_stratum(text)
    entry['plate'] = get_plate(text)
    entry['description'] = text
    # entry['(X,Y)'] = get_square(text)
    entry['class'] = _class
    square = get_first_XY(text)
    if square:
        entry['X'] = square[0]
        entry['Y'] = square[1]
    else:
        entry['X'] = None
        entry['Y'] = None    
    return entry

def parse(text):
    lines = text.split('\n')
    entries = []
    classes = []
    current_class = ''

    for line in lines:
        if len(line) == 0: continue
        # Check for titles and blobs that are not entries.
        if re.match(r'\A\d+\s?\d+\..+', line):
            entries.append(line)
            classes.append(current_class)
        elif re.match(r'\Aclass|\ACLASS', line):
            line = line.replace('CLASS', '').replace('class', '')
            current_class = line
        elif len(entries) > 0:
            entries[-1] = entries[-1] + ' ' + line

    result = pd.DataFrame()
    for entry, _class in zip(entries, classes):
        parsed = parse_entry(entry, _class)
        result = result.append(parsed)
    return result

def parse_directory(path):
    text = ''
    for filename in glob.glob(os.path.join(path, '*.txt')):
        # print filename
        text += '\n' + (open(filename).read())
    return parse(text)

if __name__ == '__main__':
    x = parse_directory('/Users/simonposada/src/DH_Fall2016/Extraction/result')
    # x = parse(open('result/page_4.txt', 'r').read())
    print x
    # x.to_csv("output.csv")