"""
API for the Salty Hacker Build Week Project

API Developers:
Iuliia Stanina
Robert Sharp
"""
from flask import Flask, make_response, request, jsonify
import pandas as pd


app = Flask(__name__)
data = pd.read_csv('hacker-comments.csv')


@app.route('/')
@app.route('/docs')
def documentation():
    return jsonify({
        'Project': 'Saltiest Hacker API',
        'Developers': [
            'Iuliia Stanina',
            'Robert Sharp',
        ],
        'End Points': [
            '/',
            '/score-by-author/<author>',
            '/comment-by-id/<comment_id>',
            '/comments-by-author/<author>',
        ]
    })


@app.route('/score-by-author/<author>')
def score_by_author(author):
    if author in data['hacker_name'].values:
        score = data[data['hacker_name'] == author]['hacker_score']
        return jsonify({
            'score': str(list(score)[0]),
        })
    else:
        return jsonify({
            'score': '0',
        })


@app.route('/comments-by-author/<author>')
def comments_by_author(author):
    if author in data['hacker_name'].values:
        comments = data[data['hacker_name'] == author][[
            'hacker_comment', 'comment_saltiness']]
        return jsonify({
            'comments': comments.to_list()[:10],
        })
    else:
        return jsonify({
            'comments': [],
        })


@app.route('/comment-by-id/<comment_id>')
def comment_by_id(comment_id):
    _id = int(comment_id)
    if _id in data.index:
        comment = data['hacker_comment'][_id]
        saltiness = str(data['comment_saltiness'][_id])
        author = data['hacker_name'][_id]
        return jsonify({
            'author': author,
            'comment': comment,
            'saltiness': saltiness,
        })
    else:
        return jsonify({
            'author': 'Author not found',
            'comment': 'Comment not found',
            'saltiness': '0',
        })


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
