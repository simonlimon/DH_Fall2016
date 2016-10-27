import pandas as pd

def parse_entry(text):
    return pd.DataFrame()

def parse_page(text):

    entries = text.split('\n')
    print entries[1]
    exit()

    result = pd.DataFrame()
    for entry in entries:
        page = parse_entry(entry)
        result.append(entry)
    return result

def parse_chapter(texts):
    result = pd.DataFrame()
    for text in texts:
        page = parse_page(text)
        result.append(page)
    return result

# def parse_