from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SignupForm(FlaskForm):
    username = StringField(label='Username')
    email = StringField(label="email")
    password = StringField(label="password")
    password2 = StringField(label="Επιβεβαίωση password")
    submit = SubmitField(label="Εγγραφή")