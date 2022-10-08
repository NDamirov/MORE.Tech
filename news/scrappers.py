from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timedelta
from multiprocessing import cpu_count
import requests
from requests_futures.sessions import FuturesSession
 
class Scrapper:
    def __init__(self, name, getter):
        self.session_ = requests.Session()
        self.name_ = name
        self.getter_ = getter
    
    def Get(self, amount=1):
        return self.getter_(self.session_, amount)

def RIAGetter(sess, amount):
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

def LentaGetter(sess, amount):
    endpoint = "https://lenta.ru/news/"
    time = datetime.today()
    for i in range(amount):
        news_page = endpoint + time.strftime("%Y/%m/%d")
        doc_tree = BeautifulSoup(sess.get(news_page).text, 'html.parser')
        news_list = doc_tree.find_all("a", "card-full-news _archive")
        links = tuple(f"https://lenta.ru{news['href']}" for news in news_list)
        result = []
        with FuturesSession() as session:
            futures = [session.get(url) for url in links]
            for id, future in zip(range(len(futures)), as_completed(futures)):
                inner_text = future.result()
                doc_tree = BeautifulSoup(inner_text.text, 'html.parser')
                tags = doc_tree.find("a", "item dark active")
                tags = tags.get_text() if tags else None
        
                text = doc_tree.find("div", "topic-body__content").get_text()
        
                topic = doc_tree.find("a", "b-header-inner__block")
                topic = topic.get_text() if topic else None
        
                title = doc_tree.find("span", "topic-body__title")
                title = title.get_text() if title else None
                result.append({"url": links[id], "title": title, "text": text, "date": links[id][22:32].replace('/', '')})
        time -= timedelta(days=1)
    return result

news_scrappers = [Scrapper('RIA', RIAGetter), Scrapper('Lenta', LentaGetter)]

