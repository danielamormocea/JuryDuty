from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class GivePerm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    admin_user = BooleanField('Make Admin')
    organizer_user = BooleanField('Make Organizer')
    apply = SubmitField('Apply ')