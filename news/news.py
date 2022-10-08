from .scrappers import *
from datetime import datetime

class NewsLoader:
    def __init__(self, buffer_size=300):
        self.scrappers_ = news_scrappers
        self.last_loaded_ = datetime.today()
        self.last_news_ = []
        self.buffer_size_ = buffer_size * len(self.scrappers_)
        self.GetLastNews(30)
        
    def GetNews(self):
        self.GetLastNews(1)
        return self.last_news_

    def GetLastNews(self, amount):
        for scrapper in self.scrappers_:
            new_news = scrapper.Get(amount)
            flag = True
            for news in new_news:
                for old in self.last_news_:
                    if old['url'] == news['url']:
                        flag = False
                        break
                if flag:
                    self.last_news_.append(news)
                if not flag:
                    break

        if len(self.last_news_) > self.buffer_size_:
            self.last_news_ = self.last_news_[len(self.last_news_) - self.buffer_size_:]

            
        