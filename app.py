from random import randint

from flask import Flask, render_template, request, session
from flask_migrate import Migrate
from werkzeug.utils import redirect
from forms import MessageForm, BookingForm

from config import Config
from models import db, Teacher, Goal, Booking, teachers_data

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    goals = db.session.query(Goal).all()
    teachers = db.session.query(Teacher).all()
    output = render_template("index.html",
                             goals=goals,
                             teachers=teachers)

    return output


@app.route('/goals/<goal>')
def goals(goal):
    goal = db.session.query(Goal).get_or_404(goal)
    teachers = db.session.query(Teacher).all()
    output = render_template("goal.html",
                             goal=goal,
                             teachers=teachers)

    return output


@app.route('/profiles/<teacher_id>')
def profiles(teacher_id):
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    output = render_template("profile.html",
                             teacher=teacher,
                             profile=teachers_data[teacher_id])   # данные расписания из json

    return output


@app.route('/message', methods=['GET', 'POST'])
def message():
    teacher_id = request.args.get('teacher')
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    form = MessageForm()
    output = render_template("message.html",
                             teacher=teacher,
                             form=form)

    return output


@app.route('/message_sent', methods=['POST'])
def message_sent():
    return 'Сообщение отправлено'


@app.route('/request')
def pick():
    output = render_template("pick.html")

    return output


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    day = request.args.get('day')
    session['day'] = day
    hour = request.args.get('hour')
    session['hour'] = hour
    teacher_id = request.args.get('teacher')
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    form = BookingForm()

    if form.validate_on_submit():
        name = form.name.data
        session['c_name'] = name
        phone = form.phone.data
        session['c_phone'] = phone

        new_booking = Booking(day=day, hour=hour, client_name=name, client_phone=phone, teacher=teacher)
        db.session.add(new_booking)
        db.session.commit()

        return redirect('/sent')

    output = render_template("booking.html",
                             day=day,
                             hour=hour,
                             teacher=teacher,
                             form=form)

    return output


@app.route('/sent', methods=['GET', 'POST'])
def sent():
    day = session.get('day')
    hour = session.get('hour')
    client_name = session.get('c_name')
    client_phone = session.get('c_phone')
    output = render_template("sent.html",
                             day=day,
                             hour=hour,
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
