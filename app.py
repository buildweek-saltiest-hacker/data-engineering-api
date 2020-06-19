"""
API for the Salty Hacker Build Week Project

Developers:
Iuliia Stanina
Robert Sharp
"""
from flask import Flask, make_response, request, jsonify
import gunicorn

app = Flask(__name__)


@app.route('/')
@app.route('/test')
def test_api():
    return jsonify({'User': 'Broken', 'Rank': 1, 'Score': 9000})


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
