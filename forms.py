from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MessageForm(FlaskForm):
    name = StringField('Вас зовут')
    phone = StringField('Ваш телефон')
    message = StringField('Сообщение')
    submit = SubmitField('Записаться на пробный урок')


class BookingForm(FlaskForm):
    name = StringField('Вас зовут')
    phone = StringField('Ваш телефон')
    submit = SubmitField('Записаться на пробный урок')
