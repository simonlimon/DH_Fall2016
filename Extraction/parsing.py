# coding=utf-8
import pandas as pd
import re
import roman

### ------- helpers for data retrieval ------- ###

def get_num(text):
    num_strings = re.findall(r'\A\d+\s*\.', text)
    if len(num_strings) == 0:
        print 'Number not found: ' + text
        return None
    num_string = num_strings[0]
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

def get_square(text):
    strings = re.findall(r'sq. \d+-\d+', text)
    if len(strings) == 0:
        print 'Square not found: ' + text
        return None
    string = strings[0]
    square_string = string.replace('sq. ', '')
    return square_string.split('-')

def get_stratum(text):
    strings = re.findall(r'stratum \w{1,3}', text)
    if len(strings) == 0:
        print 'Stratum not found: ' + text
        return None
    string = strings[0]
    string = string.replace('1', 'I').replace('stratum ', '')
    return str(roman.fromRoman(string))

def get_plate(text):
    strings = re.findall(r'\(P[l1]\..+\)', text)
    if len(strings) == 0:
        print 'Plate not found: ' + text
        return None
    string = strings[0]
    string = re.sub(r'Pl. |P1. |no. |[()]', '', string)
    string = string.replace(', ', '-')
    if string[-1] == '.': string = string[:-1]
    return string.strip()

### ------------------------------------------ ###

def parse_entry(text):

    entry = pd.Series()

    entry.name = get_num(text)
    entry['site'] = get_site(text)
    entry['year'] = get_year(text)
    entry['block'] = get_block(text)
    entry['stratum'] = get_stratum(text)
    entry['plate'] = get_plate(text)
    # entry['description'] = text

    square  = get_square(text)
    if square:
        entry['x'] = square[0]
        entry['y'] = square[1]
    else:
        entry['x'] = None
        entry['y'] = None

    return entry

def parse_page(text):
    lines = text.split('\n')
    entries = []

    for line in lines:
        if len(line) == 0: continue
        # Check for titles and blobs that are not entries.
        if re.match(r'\d+\s?\.\s+(..)\..*', line):
            entries.append(line)
        elif len(entries) > 0:
            entries[-1] = entries[-1] + ' ' + line

    result = pd.DataFrame()
    for entry in entries:
        parsed = parse_entry(entry)
        result = result.append(parsed)
    return result

def parse_chapter(texts):
    result = pd.DataFrame()
    for text in texts:
        page = parse_page(text)
        result.append(page)
    return result

if __name__ == '__main__':
    print parse_page(open('/Users/simonposada/src/DH_Fall2016/Extraction/result/page_4.txt', 'r').read())