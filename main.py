from flask import Flask, render_template, request
from news.news import NewsLoader
from model import model
import time
import os

app = Flask(__name__)
news_loader = NewsLoader()

@app.route('/get_news', methods=['GET'])
def predict_product():
    last_news = news_loader.GetNews()
    category = request.args.get('category', default=1, type=int)
    return render_template('index.html', news=last_news, category=category)

if __name__ == '__main__':
    app.run(host='localhost', port='5050', debug=False)