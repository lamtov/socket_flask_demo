from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')
