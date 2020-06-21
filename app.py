"""
API for the Salty Hacker Build Week Project

API Developers:
Iuliia Stanina
Robert Sharp
"""
from flask import Flask, make_response, request, jsonify
from models import db, migrate, Comment, parse_records
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)
db.init_app(app)
migrate.init_app(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL


@app.route('/')
def documentation():
    return jsonify((
        'Project: The Saltiest Hacker API',
        'Developers: Iuliia Stanina & Robert Sharp',
    ))


@app.route('/test')
def test():
    all_records = Comment.query.limit(10).all()
    records = parse_records(all_records)
    return jsonify(records)


@app.route('/comments-by-author/<author>')
def comments_by_author(author):
    """ Returns list of the top 3 most salty comments for any author
        http://127.0.0.1:5000/comments-by-author/po """
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
    """ Returns the average saltiness of all comments by this author
    http://127.0.0.1:5000/score-by-author/po """
    return jsonify(Comment.query.filter_by(author=author).first().score)


@app.route('/comment-by-id/<comment_id>')
def comment_by_id(comment_id):
    """ Comment text by comment_id
    http://127.0.0.1:5000/comment-by-id/42 """
    return jsonify(Comment.query.filter_by(id=comment_id).first().comment)


# @app.route('/top-hackers/<number>')
# def top_hackers(number=3):
#     hackers = parse_records(Hacker.query.limit(number).all())
#     return jsonify([{
#         'rank': hacker.rank,
#         'name': hacker.name,
#         'score': hacker.score,
#     } for hacker in hackers])


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


if __name__ == '__main__':
    app.run()
