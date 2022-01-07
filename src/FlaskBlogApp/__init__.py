from flask import Flask
#for random key generation we could use 
#the following libray:
import secrets

app = Flask(__name__)

secret_key_general = secrets.token_hex(16) #for general lock use 
secret_key_wtf = secrets.token_hex(16) #for use exclusive on wtf forms
app.config['SECRET_KEY'] = secret_key_general
app.config['WTF_CSRF_SECRET_KEY'] = secret_key_wtf

# we must import routes here, after the app initialization 
# and we must do the import of routes because otherwise 
# there is nothing to call the routes
from FlaskBlogApp import routes