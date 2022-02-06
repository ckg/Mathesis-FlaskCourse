from typing import Optional
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #file field and validator is a special case that uses binary data   
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from FlaskBlogApp.models import User
from flask_login import  current_user

# Custom validator for email outside class-1st way for creating custom validator
def validate_email(form, email): #form and not self because we are outside form class
   email = User.query.filter_by(email=email.data).first() # takes the username from the form
   if email:
         raise ValidationError("Αυτό το email υπάρχει ήδη")

# Custom validator for max file size outside class
def maxImageSize(max_size=2): #2MB but form understands bytes so we need to transform it below
   max_bytes = max_size * 1024 * 1024
   #create an internal method so we start the name with underscore
   def _check_file_size(form, field): #we use not specific field name because we will use it on different forms
      if len(field.data.read()) > max_bytes:
         raise ValidationError(f"Το μέγεθος της εικόνας δεν μπορει να υπερβαίνει τα {max_size} MB")

   return _check_file_size #because as validator we call the outside function and not the internal      

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
   
   # for remembering the session of flask login
   remember_me = BooleanField(label="Remember me")

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

class AccountUpdateForm(FlaskForm):
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
                        ]
                      )
   
   profile_image = FileField('Εικόνα Προφίλ',
                              validators=[
                                 Optional(strip_whitespace=True),
                                 FileAllowed(['jpg', 'jpeg', 'png'], 
                                             'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!'),
                                 maxImageSize(max_size=3)
                              ] 
                           )


   # Custom validator for username inside class-2nd way for creating custom validator
   def validate_username(self, username): #must have the form validate_fieldOfInterest so the wtforms knows where to use it
      if username.data != current_user.username: # Check only if another user with the same value exists
         user = User.query.filter_by(username=username.data).first() # takes the username from the form
         if user:
            raise ValidationError("Αυτό το username υπάρχει ήδη")
   
    # Custom validator for username inside class-2nd way for creating custom validator
   def validate_email(self, email): #must have the form validate_fieldOfInterest so the wtforms knows where to use it
      if email.data != current_user.email: # Check only if another user with the same value exists
         email = User.query.filter_by(email=email.data).first() # takes the email from the form
         if email:
            raise ValidationError("Αυτό το email υπάρχει ήδη")



   submit = SubmitField(label="Αποστολή")
