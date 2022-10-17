import re
from typing import List

# Special Headers in which is preferable to put a break line character before to separate section of tg message
break_line_headers = [ "Oggetto e Decreto di emanazione" ]
useless_headers = []

def escape_char(text: str, char_to_escape: List[str] = ['_', '*', '[', '`']) -> str:
    for char in char_to_escape:
        text = text.replace(char, "\\" + char)
    return text

def get_formatted_message(data: dict, headers: List[str]) -> str:
    message = ""
    for header in headers:
        if header in break_line_headers:
            message += "\n"
        content = data[header]
        if header in useless_headers or content == "":
            continue
        message += "*" + header.capitalize() + "*: " + escape_char(content) + "\n"
    return message.strip()

def format_tag (tag: str) -> str:
    return "*[" + tag + "]*"

def format_dumb_site_text(text: str) -> str:
    text = re.sub(' +', ' ', text)
    text = re.sub('\n*', '', text)
    return text.strip().replace('\n\t\t\t','-')
