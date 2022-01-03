from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    username = StringField(label='Username', 
                            validators=[
                               DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                               Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")
                            ]
                           )

    email = StringField(label="email",
                         validators=[
                               DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                               Email(message="Παρακαλώ εισάγετε ένα σωστό email")
                          ]
                        )

    password = StringField(label="password",
                            validators=[
                               DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                               Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")
                            ] 
                           )

    password2 = StringField(label="Επιβεβαίωση password",
                             validators=[
                               DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                               Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                               EqualTo("password", message="Τα password πρέπει να ταιριάζουν")
                             ]
                            )

    submit = SubmitField(label="Εγγραφή")