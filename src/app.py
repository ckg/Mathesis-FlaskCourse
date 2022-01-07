from flask import (Flask, render_template, 
                    redirect, url_for,
                    request, flash
                    )
from forms import SignupForm, LoginForm, NewArticleForm
#for random key generation we could use 
#the following libray:
import secrets

app = Flask(__name__)

secret_key_general = secrets.token_hex(16) #for general lock use 
secret_key_wtf = secrets.token_hex(16) #for use exclusive on wtf forms
app.config['SECRET_KEY'] = secret_key_general
app.config['WTF_CSRF_SECRET_KEY'] = secret_key_wtf



@app.route ("/index/")
@app.route ("/")
def root():
    return render_template("index.html")

@app.route("/signup/", methods=["GET", "POST"])
def signup():

    form = SignupForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data
        print(username, email, password, password2)
 
    return render_template("signup.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        print(email, password)

        flash(f"Η είσοδος του χρήστη {email} έγινε με επιτυχία", "success") # the 'success' is used for defining the category of message 

    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    return redirect(url_for("root")) #we call the method name in url

@app.route("/new_article/", methods=["GET", "POST"])
def new_article():
    form = NewArticleForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        article_title = form.article_title.data
        article_body = form.article_body.data
        print(article_title, article_body)
    return render_template("new_article.html", form=form)




if __name__ == '__main__':
    app.run(debug=True)

