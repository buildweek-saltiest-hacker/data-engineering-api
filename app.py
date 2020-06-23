"""
API for the Salty Hacker Build Week Project

API Developers:
Iuliia Stanina
Robert Sharp
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, make_response, request, jsonify
from models import db, migrate, Comment, parse_records
from bs4 import BeautifulSoup
from random import choice, randint
import requests
import os
import re


# from dotenv import load_dotenv
# load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)
db.init_app(app)
migrate.init_app(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
sid_obj = SentimentIntensityAnalyzer()


def sentiment_score(sentence: str) -> int:
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return int(-sentiment_dict['compound'] * 10000)


@app.route('/sentiment/<text>')
def sentiment(text):
    return jsonify(text=text, score=sentiment_score(text))


@app.route('/')
def home():
    return jsonify((
        'Project: The Saltiest Hacker API',
        'Developers: Iuliia Stanina & Robert Sharp',
    ))


@app.route('/docs')
def docs():
    return jsonify((
        ':: HTTP Routes ::',
        '/',
        '/docs',
        '/comments-by-author/<author>',
        '/score-by-author/<author>',
        '/comment-by-id/<comment_id>',
        '/top-hackers/<number>',
        '/recent',
        'sentiment/<text>',
    ))


@app.before_request
def before_request():
    """ CORS preflight, required for off-server access """

    def _build_cors_prelight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    if request.method == "OPTIONS":
        return _build_cors_prelight_response()


@app.after_request
def after_request(response):
    """ CORS headers, required for off-server access """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/comments-by-author/<author>')
def comments_by_author(author):
    """ Returns list of the top 3 most salty comments for any author
        /comments-by-author/po """
    comments = Comment.query.filter_by(author=author)
    parsed = parse_records(comments.order_by(Comment.saltiness).all())
    ordered = [{
        'id': item['id'],
        'comment': item['comment'],
        'saltiness': item['saltiness'],
    } for item in reversed(parsed[-3:])]
    return jsonify(ordered)


@app.route('/score-by-author/<author>')
def score_by_author(author):
    """ Returns the average saltiness of their comments
    /score-by-author/po """
    return jsonify(score=Comment.query.filter_by(author=author).first().score)


@app.route('/comment-by-id/<comment_id>')
def comment_by_id(comment_id):
    """ Comment text by comment_id
    /comment-by-id/42 """
    comment = Comment.query.filter_by(id=comment_id).first()
    return jsonify({
        'author': comment.author,
        'comment': comment.comment,
        'saltiness': comment.saltiness,
    })


@app.route('/recent')
def recent():
    page = requests.get("https://news.ycombinator.com/newcomments")
    soup = BeautifulSoup(page.content, features='html.parser')
    comments = []
    usr_com = zip(soup.find_all('a', class_='hnuser'),
                  soup.find_all('div', class_='comment'),
                  soup.find_all('span', class_='storyon'))
    for usr, com, head in usr_com:
        text = com.get_text().strip()
        comments.append({
            'author': usr.get_text(),
            'saltiness': sentiment_score(text),
            'headline': head.find('a').get_text(),
            'comment': text,
        })
    comments.sort(key=lambda x: x['saltiness'], reverse=True)
    return jsonify(data=comments)


# @app.route('/top-hackers/<number>')
# def top_hackers(number=3):
#     hackers = parse_records(Hacker.query.limit(number).all())
#     return jsonify([{
#         'rank': hacker.rank,
#         'name': hacker.name,
#         'score': hacker.score,
#     } for hacker in hackers])


# @app.route('/random-comment')
# def random_comment():
#     return comment_by_id(randint(0, 230702))


# @app.route('/random-author')
# def random_author():
#     author = choice([hacker.name for hacker in Hacker.query.all()])
#     comments = comments_by_author(author)
#     return jsonify(author=author, comments=comments)


if __name__ == '__main__':
    app.run()
