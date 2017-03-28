from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


class CreateBookmarkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
