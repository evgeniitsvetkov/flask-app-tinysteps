import json
from random import randint

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import redirect
from forms import MessageForm, BookingForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dfdlfhqaqadkgd:2a03bd35a434942bf87161053906403340e2187b9f139b1a8ec3ad6eddebc361@ec2-46-137-188-105.eu-west-1.compute.amazonaws.com:5432/d3o5u8br75i2g7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


teachers_goals_association = db.Table('teachers_goals',
                                      db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                                      db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
                                      )


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.UnicodeText, nullable=False)
    rating = db.Column(db.Float, default=4.5)
    picture = db.Column(db.Unicode, default='../static/pict 1.png')
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.JSON, nullable=False)

    goals = db.relationship('Goal', secondary=teachers_goals_association, back_populates='teachers')
    bookings = db.relationship('Booking', back_populates='teacher')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)  # travel
    title = db.Column(db.Unicode, nullable=False)  # для путешествий

    teachers = db.relationship('Teacher', secondary=teachers_goals_association, back_populates='goals')


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    hour = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String, nullable=False)
    client_phone = db.Column(db.String, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='bookings')


db.create_all()


# скрипт для первой загрузки данных из teachers.json
with open('teachers.json', 'r') as f:
    teachers_data_json = f.read()

teachers_data = json.loads(teachers_data_json)

"""
for t in teachers_data.values():
    teacher = Teacher(name=t['name'], about=t['about'], rating=t['rating'],
                      picture=t['picture'], price=t['price'], free=t['free'])
    db.session.add(teacher)
db.session.commit()
"""


# скрипт для первой загрузки данных из goals.json
with open('goals.json', 'r') as f:
    goals_data_json = f.read()

goals_data = json.loads(goals_data_json)

"""
for goal, title in goals_data.items():
    goal = Goal(goal=goal, title=title)
    db.session.add(goal)
    #goal.teachers.append(teacher)
db.session.commit()
"""

"""
# скрипт для первой загрузки данных в teachers_goals_association
teacher = db.session.query(Teacher).get(randint(1, 12))
goal = db.session.query(Goal).get(randint(1, 4))
print(teacher)
print(goal)
goal.teachers.append(teacher)
db.session.commit()
"""


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
    hour = request.args.get('hour')
    teacher_id = request.args.get('teacher')
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    form = BookingForm()

    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
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
