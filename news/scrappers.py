from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

class Scrapper:
    def __init__(self, name, getter):
        self.session_ = requests.Session()
        self.name_ = name
        self.getter_ = getter
    
    def Get(self, amount=1):
        return self.getter_(self.session_, amount)

def RIA_getter(sess, amount):
    time = datetime.today()
    result = []
    for i in range(amount):
        url = "https://ria.ru/services/economy/more.html?id=1&date=" + time.strftime("%Y%m%dT%H%M%S")
        r = sess.get(url)
        inner = r.text
        doc_tree = BeautifulSoup(inner, "html.parser")
        links = doc_tree.find_all("a", "list-item__title color-font-hover-only")
        with FuturesSession() as session:
            futures = [session.get(link["href"]) for link in links]
            for id, future in zip(range(len(futures)), as_completed(futures)):
                inner_text = future.result()
                inner_tree = BeautifulSoup(inner_text.text, "html.parser")
                temp = inner_tree.find("div", "article__body js-mediator-article mia-analytics")
                if temp:
                    result.append({"url": links[id]["href"], "date": time.strftime("%Y%m%d"), "title": links[id].get_text(), "text": temp.get_text()})
            time -= timedelta(hours=5)
    
    return result

def Lenta_getter():
    pass

news_scrappers = [Scrapper('RIA', RIA_getter)]
# news_scrappers = [Scrapper('RIA', RIA_getter), Scrapper('Lenta', Lenta_getter)]

