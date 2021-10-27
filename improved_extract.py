import re
import jiagu


def improved_extract(text):
    text = text.replace('\n','').replace('\r','')
    pattern = r"'''(.*?)=="
    match = re.search(pattern, text)
    if match is not None:
        text = match.group(1)
    pattern2 = re.compile(r'[{<](.*?)[>}]')
    text = re.sub(pattern2, '', text)
    pattern3 = re.compile(r'[\[\]\{\}\|\';,./\\&\?"]')
    text = re.sub(pattern3, '', text)
    extracted_triples = jiagu.knowledge(text)
    
    return extracted_triples