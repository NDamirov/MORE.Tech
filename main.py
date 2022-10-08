from flask import Flask, render_template, request
from datetime import datetime, timedelta
from news.news import NewsLoader
from model import model
import threading

app = Flask(__name__)
news_loader = NewsLoader()

@app.route('/get_news', methods=['GET'])
def predict_product():
    last_news = news_loader.GetNews()
    category = request.args.get('category', default=1, type=int)
    return render_template('index.html', news=last_news, category=category)

def worker():
    last_update = datetime.today()
    while (datetime.today() - last_update) > timedelta(hours=3):
        news_loader.GetNews()
        last_update = datetime.today()

if __name__ == '__main__':
    t = threading.Thread(target=worker)
    t.start()
    app.run(host='localhost', port='5050', debug=True)