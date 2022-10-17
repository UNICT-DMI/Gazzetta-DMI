from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString
import requests
from utils.formatting import format_dumb_site_text
from utils.site import Site

class Bandi(Site):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
    
    def get_table(self) -> NavigableString:
        soup = BeautifulSoup(self.page.content, 'html5lib')
        self.table = soup.find_all('table')[0]
        return self.table
    
    def get_headers(self) -> NavigableString:
        self.key_element = 'Oggetto e Decreto di emanazione'
        self.thead = self.table.find('thead')
        header_cells = self.thead.find_all("th")
        self.headers = [format_dumb_site_text(header.getText()) for header in header_cells]
        if '' in self.headers:
            self.headers.remove('')
        return self.thead.find_next_sibling().find_next('tr')

    def get_row(self, tr: NavigableString) -> None:
        return tr.find_all('td')

    def get_attachments(self, tr: NavigableString) -> list[str]:
        a_attachments = tr.find_all('a')
            
        link_to_attachments = urljoin (self.link, a_attachments[0]['href'])
        attachments_page = requests.get(link_to_attachments, timeout=None)
        attachments_container = BeautifulSoup(attachments_page.content, 'html5lib')
            
        return self.get_all_pdfs_in_container(attachments_container)