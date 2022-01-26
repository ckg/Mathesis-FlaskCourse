from flask import Flask
# for random key generation we could use 
# the following libray:
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)

secret_key_general = secrets.token_hex(16) #for general lock use 
secret_key_wtf = secrets.token_hex(16) #for use exclusive on wtf forms
app.config['SECRET_KEY'] = secret_key_general
app.config['WTF_CSRF_SECRET_KEY'] = secret_key_wtf

# Database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_course_database.db'
# Disable modification warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=10)

# Connect application with the database
db = SQLAlchemy(app)
# Connect hash tool with our app
bcrypt = Bcrypt(app)
# Create an instance of LoginManager
#login_manager = LoginManager()
# Connect LoginManager with our app
#login_manager.init_app(app)
# Create and connect LoginManager with our app
login_manager = LoginManager(app)
# redirect us to login page whenever we call a login_required page
login_manager.login_view = "login"
# To change the message
login_manager.login_message_category = "warning"
login_manager.login_message = "Παρακαλoύμε κάντε login για να δείτε αυτή τη σελίδα"

# we must import routes here, after the app initialization 
# and we must do the import of routes because otherwise 
# there is nothing to call the routes
from FlaskBlogApp import routes, models