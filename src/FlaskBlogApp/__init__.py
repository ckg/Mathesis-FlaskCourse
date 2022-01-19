from flask import Flask
# for random key generation we could use 
# the following libray:
import secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

secret_key_general = secrets.token_hex(16) #for general lock use 
secret_key_wtf = secrets.token_hex(16) #for use exclusive on wtf forms
app.config['SECRET_KEY'] = secret_key_general
app.config['WTF_CSRF_SECRET_KEY'] = secret_key_wtf

# Database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_course_database.db'
# Disable modification warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect application with the database
db = SQLAlchemy(app)

# we must import routes here, after the app initialization 
# and we must do the import of routes because otherwise 
# there is nothing to call the routes
from FlaskBlogApp import routes, models