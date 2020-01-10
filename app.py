from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    output = render_template("index.html")

    return output


if __name__ == '__main__':
    app.run()