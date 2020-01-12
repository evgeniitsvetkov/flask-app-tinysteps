from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    output = render_template("index.html")

    return output


@app.route('/goals/<goal>')
def goals(goal):
    output = render_template("goal.html")

    return output


@app.route('/profiles/<id>')
def profiles(id):
    output = render_template("profile.html")

    return output


@app.route('/request')
def pick():
    output = render_template("pick.html")

    return output


@app.route('/booking/<id>')
def request(id):
    output = render_template("booking.html")

    return output


@app.route('/search')
def search():
    return "Выполняем поиск по строке " + request.values.get("s")


@app.errorhandler(404)
def not_found(e):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def server_error(e):
    return "Что-то не так, но мы все починим"


if __name__ == '__main__':
    app.run()