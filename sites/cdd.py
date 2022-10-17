import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString
import requests
from utils.site import Site

class CDD(Site):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
    
    def get_table(self) -> NavigableString:
        soup = BeautifulSoup(self.page.content, 'html5lib')
        self.table = soup.find_all('table')[0]
        return self.table
    
    def get_headers(self) -> NavigableString:
        self.key_element = 'Titolo'
        self.thead = self.table.find_next('tr')
        self.headers = ["Titolo"]
        return self.thead.find_next('tr').find_next('b')

    def get_row(self, tr: NavigableString) -> list[NavigableString]:
        return [tr]

    def get_attachments(self, tr: NavigableString) -> list[str]:
        a_attachments = tr.find_all('a')
            
        link_to_attachments = urljoin (self.link, a_attachments[0]['href'])
        attachments_page = requests.get(link_to_attachments, timeout=None)
        self.cookies = {attachments_page.cookies.keys()[0]: attachments_page.cookies.values()[0]}
        attachments_container = BeautifulSoup(attachments_page.content, 'html5lib').find('div', 'field-items')
            
        return self.get_api_links(attachments_container)
            
    def get_api_links(self, attachments_container: NavigableString):
        attachment_links = []
        for link in attachments_container.find_all('a'):
            if link.has_attr('href'):
                if re.match("\/gestione-verbali\/get_allegato\.php\?id=*", link['href']):
                    attachment_links.append(urljoin(self.link, link['href']))
        return attachment_links

    def save_attachments(self, pdf_links: list[str]) -> list[str]:
        local_files = []
        for i, pdf_link in enumerate(pdf_links):
            title = f'odg{i}.pdf'

            payload={}
            headers = {}

            response = requests.request("GET", pdf_link, headers=headers, data=payload, cookies=self.cookies)

            with open('tmp/' + title, 'wb') as f:
                f.write(response.content)
            local_files.append('tmp/' + title)
        return local_files
        
