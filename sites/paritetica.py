from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString
import requests
from utils.formatting import format_dumb_site_text
from utils.site import Site

class Paritetica(Site):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
    
    def get_table(self) -> NavigableString:
        soup = BeautifulSoup(self.page.content, 'html5lib')
        self.table = soup.find('aside', id="service-column")
        return self.table
    
    def get_headers(self) -> NavigableString:
        self.key_element = 'Oggetto'
        self.headers = ['Oggetto']
        return self.table.find_next('a').find_next('a')

    def get_row(self, tr: NavigableString) -> None:
        return [tr]

    def get_attachments(self, tr: NavigableString) -> list[str]:
        return [urljoin(self.link, tr['href'])]
    
    def find_next_node(self, node: NavigableString) -> NavigableString:
        result = node.find_next('a')
        while result is not None and not result['href'].endswith('.pdf'):
            result = result.find_next('a')
        return result

    def find_previous_node(self, node: NavigableString) -> NavigableString:
        result = node.find_previous('a')
        while result is not None and not result['href'].endswith('.pdf'):
            result = result.find_previous('a')
        return result