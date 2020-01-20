import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField


with open('goals.json', 'r') as f:
    goals_data_json = f.read()

goals_data = json.loads(goals_data_json)


with open('teachers.json', 'r') as f:
    teachers_data_json = f.read()

teachers_data = json.loads(teachers_data_json)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
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
    goals = db.relationship(
        'Goal', secondary=teachers_goals_association, back_populates='teachers')

    def __repr__(self):
        return 'Teacher %r' % self.name


# скрипт для первой загрузки данных из teachers.json
#for t in teachers_data.values():
#    teacher = Teacher(name=t['name'], about=t['about'], rating=t['rating'], picture=t['picture'], price=t['price'])
#    db.session.add(teacher)
#db.session.commit()


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.String, primary_key=True)  # travel
    title = db.Column(db.Unicode, nullable=False)  # для путешествий
    teachers = db.relationship(
        'Teacher', secondary=teachers_goals_association, back_populates='goals')

# скрипт для первой загрузки данных из  goals.json
#for goal, title in goals_data.items():
#    goal = Goal(goal=goal, title=title)
#    db.session.add(goal)
#db.session.commit()


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)


db.create_all()

t = db.session.query(Teacher).get_or_404(1)
print(t.goals)

g = db.session.query(Goal).get_or_404(1)
print(g)


@app.route('/')
def index():
    goals = db.session.query(Goal).all()
    teachers = db.session.query(Teacher).all()
    output = render_template("index.html",
                             goals=goals,   # данные из БД
                             teachers=teachers)   # данные из БД

    return output


@app.route('/goals/<goal>')
def goals(goal):
    goal_new = db.session.query(Goal).get_or_404(goal)
    goals_new = db.session.query(Goal).all()
    teachers = db.session.query(Teacher).all()
    output = render_template("goal.html",
                             goal=goal,
                             goals=goals_data.items(),
                             goals_new=goals_new,
                             teachers=teachers)   # данные из БД

    return output


@app.route('/profiles/<teacher_id>')
def profiles(teacher_id):
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    output = render_template("profile.html",
                             teacher=teacher,   # данные из БД
                             profile=teachers_data[teacher_id])   # данные расписания из json

    return output


@app.route('/message')
def message():
    output = render_template("message.html")

    return output


@app.route('/request')
def pick():
    output = render_template("pick.html")

    return output


@app.route('/booking/<teacher_id>')
def booking(teacher_id):
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    output = render_template("booking.html",
                             teacher=teacher)   # данные из БД

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
