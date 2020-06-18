from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def index():
    return "Hello from Flask!!!"


if __name__ == '__main__':
    app.run(debug=True)
