from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    name = StringField('Вас зовут')
    phone = StringField('Ваш телефон')
    message = StringField('Сообщение')
    submit = SubmitField('Записаться на пробный урок')


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Записаться на пробный урок')
