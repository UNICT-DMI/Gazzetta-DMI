from abc import abstractmethod
import traceback
from typing import Union
from urllib.parse import urljoin
from bs4 import  NavigableString
import requests
from utils.formatting import format_dumb_site_text, format_tag, get_formatted_message
from utils.resources import get_pdf_text, match_regex_tag


from utils.tg import TelegramBot

class Site:
    def __init__(self, name: str, link: str, token: str, chat_id: Union[int, str], dev_chat_ids: list[str]) -> None:
        self.name = name
        self.link = link
        self.bot = TelegramBot(token, chat_id, dev_chat_ids)
        pass

    @abstractmethod
    def get_table(self) -> NavigableString:
        # soup = BeautifulSoup(self.page.content, 'html5lib')
        # self.table = soup.find_all('table')[1]
        # return self.table
        pass

    @abstractmethod
    def get_headers(self) -> NavigableString:
        # self.thead = self.table.find('tr')
        # header_cells = self.thead.find_all("td") if self.thead.find_all("td") != [] else self.thead.find_all("th")
        # self.headers = [format_dumb_site_text(header.getText()) for header in header_cells]
        # if '' in self.headers:
        #     self.headers.remove('')
        # return self.thead.find_next('tr')
        pass

    @abstractmethod
    def get_row(self, tr: NavigableString) -> list[NavigableString]:
        # return tr.find_all('td')
        pass
    
    @abstractmethod
    def get_attachments(self, tr: NavigableString) -> list[str]:
        pass

    def get_main_page(self) -> requests.Response:
        self.page = requests.get(self.link)

        if self.page.status_code != 200:
            print("Impossibile accedere al sito di " + self.name + ", riprovare più tardi")
            raise Exception("Impossibile accedere al sito di " + self.name + ", controllare stato codice " + str(self.page.status_code))
        return self.page

    def find_next_node(self, node: NavigableString) -> NavigableString:
        return node.find_next_sibling()

    def find_previous_node(self, node: NavigableString) -> NavigableString:
        return node.find_previous_sibling()

    def get_all_pdfs_in_container(self, container: NavigableString) -> list[str]:
        attachment_links = []
        for link in container.find_all('a'):
            if link.has_attr('href'):
                if link['href'].endswith('.pdf'):
                    attachment_links.append(urljoin(self.link, link['href']))
        return attachment_links

    def save_attachments(self, pdf_links: list[str]) -> list[str]:
        local_files = []
        for pdf_link in pdf_links:
            response = requests.get(pdf_link, timeout=None)
            with open('tmp/' + pdf_link.split("/")[-1], 'wb') as f:
                f.write(response.content)
            local_files.append('tmp/' + pdf_link.split("/")[-1])
        return local_files
        
    def send_announcement(self, tr: NavigableString, data: dict) -> None:
        message =  format_tag(self.name) + "\n\n" + get_formatted_message(data, self.headers) 

        attachments = self.get_attachments(tr)
        
        attachments = self.save_attachments(attachments)
        
        pdf_text = get_pdf_text(attachments)

        tags = match_regex_tag(pdf_text + message)

        message =  '\n'.join(tags) + '\n\n' + message

        self.bot.send_telegram_announcements(attachments, message, tags == [])

    def  get_all_announcements(self) -> list[str]:
        announcements = [] 
        self.get_main_page()
        self.get_table()
        pointer = self.get_headers()
        while pointer is not None:
            announcements.append({
                'pointer': pointer, 
                'data': self.get_announcement_data(pointer)
            })
            pointer = self.find_next_node(pointer)
        return announcements
    
    def handle_error(self, exception: Exception) -> None:
        if type(exception) != requests.exceptions.ConnectionError:
            error_string = "An exception was raised while parsing " + self.name + ":\n" + "`" + traceback.format_exc() +  "`"
            print(error_string)
            self.bot.send_debug_messages(error_string)

        else:
            print("Connection error while parsing " + self.name)
            print("An exception was raised while parsing " + self.name + ":\n" + "`" + traceback.format_exc() +  "`")

    #data is a composite dictionary
    #["sitename"] -> [list of announcements]
    #each announcment is a dictionary with keys: object, date, odg, odgagg, pdf report link, verbale 
    def get_announcement_data(self, pointer: NavigableString) -> dict:
        row_elements = self.get_row(pointer)
        data = {}
        for i, header in enumerate(self.headers):
            data[header] = format_dumb_site_text(row_elements[i].getText())
        return data

    def already_sent(self, announcement: dict, sent_announcements: list[dict]) -> dict:
        if announcement[self.key_element] not in [ x[self.key_element] for x in sent_announcements ]:
            return {'announcement': True }
        else :
            return {'announcement': False}