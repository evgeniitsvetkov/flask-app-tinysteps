import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


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
    free = db.Column(JSON, nullable=False)

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


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)


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