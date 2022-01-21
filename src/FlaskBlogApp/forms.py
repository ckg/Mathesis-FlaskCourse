from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from FlaskBlogApp.models import User

# Custom validator for email outside class-1st way for creating custom validator
def validate_email(form, email): #form ans not self because we are outside form class
   email = User.query.filter_by(email=email.data).first() # takes the username from the form
   if email:
         raise ValidationError("Αυτό το email υπάρχει ήδη")

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
                              Email(message="Παρακαλώ εισάγετε ένα σωστό email"),
                              validate_email
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

   # Custom validator for username inside class-2nd way for creating custom validator
   def validate_username(self, username): #must have the form validate_fieldOfInterest so the wtforms knows where to use it
      user = User.query.filter_by(username=username.data).first() # takes the username from the form
      if user:
         raise ValidationError("Αυτό το username υπάρχει ήδη")


   submit = SubmitField(label="Εγγραφή")

class LoginForm(FlaskForm):
    
   email = StringField(label="email",
                         validators=[
                              DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                              Email(message="Παρακαλώ εισάγετε ένα σωστό email")
                         ]
                       )

   password = StringField(label="password",
                           validators=[
                              DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό")  
                           ] 
                          )

   submit = SubmitField(label="Είσοδος")


class NewArticleForm(FlaskForm):

   article_title = StringField(label='Τίτλος Άρθρου', 
                               validators=[
                                 DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                                 Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")
                            ]
                           )
    
   article_body = TextAreaField(label="Κείμενο Άρθρου",
                                validators=[
                                    DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό"), 
                                    Length(min=5, message="Αυτό το πεδίο πρέπει να είναι από μεγαλύτερο από 3 χαρακτήρες")
                               ]
                       )

   submit = SubmitField(label="Υποβολή")
