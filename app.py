from flask import Flask, jsonify, request


def create_app():
    my_app = Flask(__name__)
    return my_app


app = create_app()


@app.route("/")
@app.route("/index.html")
def index():
    return "Hello from Flask!!!"


if __name__ == '__main__':
    app.run(debug=True)
