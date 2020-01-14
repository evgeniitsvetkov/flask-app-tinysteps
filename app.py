import json
from flask import Flask, render_template, request


with open('teachers.json', 'r') as f:
    contents = f.read()

teachers = json.loads(contents)
print(teachers)

app = Flask(__name__)


@app.route('/')
def index():
    output = render_template("index.html")

    return output


@app.route('/goals/<goal>')
def goals(goal):
    output = render_template("goal.html",
                             goal=goal,
                             teachers=teachers)

    return output


@app.route('/profiles/<id>')
def profiles(id):
    output = render_template("profile.html",
                             profile=teachers[id],
                             teacher_id=id)

    return output


@app.route('/message')
def message():
    output = render_template("message.html")

    return output


@app.route('/request')
def pick():
    output = render_template("pick.html")

    return output


@app.route('/booking/<id>')
def booking(id):
    output = render_template("booking.html",
                             profile=teachers[id])

    return output


@app.route('/sent', methods=['GET', 'POST'])
def sent():
    client_name = request.form.get("c_name")
    client_phone = request.form.get("c_phone")
    output = render_template("sent.html",
                             client_name=client_name,
                             client_phone=client_phone)

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
