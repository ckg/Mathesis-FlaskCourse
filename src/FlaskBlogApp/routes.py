from flask import (render_template, 
                    redirect, url_for,
                    request, flash
                    )
from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm, AccountUpdateForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article
from flask_login import login_user, current_user, logout_user, login_required

@app.route ("/index/")
@app.route ("/")
def root():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)

@app.route("/signup/", methods=["GET", "POST"])
def signup():

    form = SignupForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #Instanciate a user using models
        user = User(username=username,
                    email=email,
                    password=encrypted_password)
        #add user to database
        db.session.add(user)
        #commit changes to database
        db.session.commit()

        flash(f"Ο λογαριασμός για τον χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία", "success")

        #print(username, email, password, password2)
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('root'))
    form = LoginForm()

    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        #print(email, password)

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη {email} έγινε με επιτυχία", "success") # the 'success' is used for defining the category of message 
            login_user(user, remember=form.remember_me.data) # remember set for remembering the user session
            next_link = request.args.get("next") # we get the link of the page we asked before transered to login
            return redirect(next_link) if next_link else redirect(url_for('root'))
        else:
            flash(f"Η είσοδος του χρήστη με email {email} ήταν ανεπιτυχής", "warning")


    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    flash("Έγινε αποσύνδεση του χρήστη", "success")

    return redirect(url_for("root")) #we call the method name in url

@app.route("/new_article/", methods=["GET", "POST"])
@login_required # User must login to see this page
def new_article():
    form = NewArticleForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        article_title = form.article_title.data
        article_body = form.article_body.data
        print(article_title, article_body)
    return render_template("new_article.html", form=form)

@app.route("/account/", methods=["GET", "POST"])
@login_required # User must login to see this page
def account():
     # Pre-filling the fields with the current's user data
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)
    # or another way of Pre-filling the fields with the current's user data
    #form.username.data = current_user.username
    #form.email.data = current_user.email
    if request.method == "POST" and form.validate_on_submit(): 
        # using current user we can commit to the database without adding the user
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b>{current_user.username}</b> ενημερώθηκε με επιτυχία", "success")

        return redirect(url_for('root'))
    
    return render_template("account_update.html", form=form)
