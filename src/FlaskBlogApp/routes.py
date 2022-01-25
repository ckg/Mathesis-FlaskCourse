from flask import (render_template, 
                    redirect, url_for,
                    request, flash, session
                    )
from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article

@app.route ("/index/")
@app.route ("/")
def root():
    user = None
    if "user" in session:
        user = session["user"]
    articles = Article.query.all()
    return render_template("index.html", articles=articles, myuser = user)

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
    session.permanent = True #activate permanent sessions
    form = LoginForm()
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        
        #Instanciate a user using models
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            #make login using session
            #and pass a dictionary
            session['user'] = {"username": user.username,
                                "email": user.email,
                                "profile_image": user.profile_image,
                                "id": user.id}
            flash(f"Η είσοδος του χρήστη με email {user.email} έγινε με επιτυχία", "success") # the 'success' is used for defining the category of message
            # Since login is succesfull we redirect the user
            return redirect(url_for("root"))
        else:
            flash(f"Η είσοδος του χρήστη απέτυχε", "warning")
        #print(email, password)

         

    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("root")) #we call the method name in url

@app.route("/new_article/", methods=["GET", "POST"])
def new_article():
    user = None
    if "user" in session:
        user = session["user"]

        form = NewArticleForm()
        #we should check the method of request
        if request.method == "POST" and form.validate_on_submit(): 
            article_title = form.article_title.data
            article_body = form.article_body.data
            print(article_title, article_body)

            #Instanciate an article using models
            article= Article(article_title=article_title,
                            article_body=article_body,
                            user_id=user.get("id")
                            )
            #add article to database
            db.session.add(article)
            #commit changes to database
            db.session.commit()
            
            username = user.get("username")
            flash(f"Το άρθρο του χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία", "success")

        return render_template("new_article.html", form=form)
    else:
        flash("Για να δείτε αυτή την σελίδα πρέπει να έχετε συνδεθεί", "warning")
        return redirect(url_for("root"))
