import re
import os
import requests
from PyPDF2 import PdfReader
import yaml

reg = [
    
]

#data is a composite dictionary
#["sitename"] -> [list of announcements]
#each announcment is a dictionary with keys: object, date, odg, odgagg, pdf report link, verbale 
def read_all_sent_announcements(filename: str):
    if not os.path.exists(filename):
        with open(filename, 'w'): pass
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

def write_all_sent_announcements(filename: str, sent_announcements):
    with open(filename, "w") as f_announcements:
        yaml.dump(sent_announcements, f_announcements)
        #print(sent_announcements)

def match_regex_tag(text: str) -> list[str]:
    tags_found = []
    for tag in reg:
        if re.search(tag['exp'], text, re.IGNORECASE):
            tags_found.append('*' + tag['tag'] + '*')
    return tags_found

def get_pdf_text(pdf_files: list[str]) -> str:
    text = ""
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)        
            number_of_pages = len(reader.pages)
            for i in range (number_of_pages):
                page = reader.pages[i]
                text += page.extract_text() + " "
        except Exception as e:
            print(e)
    return text
