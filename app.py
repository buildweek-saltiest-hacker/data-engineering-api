from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def index():
    return "Hello from Flask!!!"
### samples
# @app.route("/comments")
# def comments():
#     return "Comments"
#
# @app.route("/rankings")
# def rankings():
#     return "Rankings"
#
# @app.route("/negativity-score")
# def negativity_score():
#     return "Negativity Score"

if __name__ == '__main__':
    app.run()
