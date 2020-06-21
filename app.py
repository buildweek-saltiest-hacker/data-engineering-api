"""
API for the Salty Hacker Build Week Project

API Developers:
Iuliia Stanina
Robert Sharp
"""
from flask import Flask, make_response, request, jsonify
from models import db, migrate, Comment, parse_records
import pandas as pd
import os


DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)
db.init_app(app)
migrate.init_app(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL


@app.route('/')
def documentation():
    return jsonify({
        'Project': 'Saltiest Hacker API',
        'Developers': [
            'Iuliia Stanina',
            'Robert Sharp',
        ],
        'Planned End Points': [
            '/',
            '/score-by-author/<author>',
            '/comment-by-id/<comment_id>',
            '/comments-by-author/<author>',
        ]
    })


@app.route('/test')
def test():
    all_records = Comment.query.limit(100).all()
    records = parse_records(all_records)
    return jsonify(records)


@app.route('/comments-by-author/<author>')
def get_author(author=None):
    print(author)
    author_comments = parse_records(Comment.query.filter_by(author=author).all())
    comments_list = {'author': {'comments': []}}
    for c in author_comments:
        comments_list['author']['comments'].append({
            'id': c['id'],
            'comment': c['comment'],
            'saltiness': c['saltiness'],
        })
    return jsonify(comments_list)


@app.before_request
def before_request():
    """ CORS preflight """

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
    """ CORS headers """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()
