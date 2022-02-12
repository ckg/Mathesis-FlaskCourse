from flask import (render_template, 
                    redirect, url_for,
                    request, flash, abort
                    )
from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm, AccountUpdateForm
from FlaskBlogApp import app, db, bcrypt
from FlaskBlogApp.models import User, Article
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image # for Pillow library(manipulate images)

# for custom error pages
@app.errorhandler(404)
def page_not_found(e): #the method has to have the name of the error
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404
@app.errorhandler(415)
def unsupported_media_type(e): #the method has to have the name of the error
    # note that we set the 415 status explicitly
    return render_template('errors/415.html'), 415

#for image manipulation
def image_save(image, where, size): # size is of tuple form (640,480)
    #create a (2*12)char token < 30 that we set on models-db.strings
    random_file_name = secrets.token_hex(12)
    #to split name and extension
    _, file_extension = os.path.splitext(image.filename)
    #create new random name
    image_filename = random_file_name + file_extension
    # create the absolute path to save the file
    image_path = os.path.join(app.root_path, 'static/images', where, image_filename)
    # open resize and save image
    img = Image.open(image)
    img.thumbnail(size) #thumbnail or resize
    img.save(image_path)

    # we return the filename so we can import it to database on routes.py
    return image_filename



@app.route ("/index/")
@app.route ("/")
def root():
    #we get the page number from ?page=<user input>
    page = request.args.get("page", 1, type=int) # default page=1, type=integer
    #articles = Article.query.all()
    articles = Article.query.order_by(Article.date_created.desc()).paginate(per_page=2, page=page) #to show only 2 articles per page
    return render_template("index.html", articles=articles)

@app.route("/articles_by_author/<int:author_id>")
def articles_by_author(author_id):
    user = User.query.get_or_404(author_id)
    
    #we get the page number from ?page=<user input>
    page = request.args.get("page", 1, type=int) # default page=1, type=integer
    # we bring all the articles written by the specific user
    articles = Article.query.filter_by(author=user).order_by(Article.date_created.desc()).paginate(per_page=2, page=page) #to show only 2 articles per page

    return render_template("articles_by_author.html", articles=articles, author=user)

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
        
        if form.article_image.data:
            
            try: #because someone may bypass the validator and upload a file of another file type but with the right extension
                # image_save(image, where, size) returns the image_filename
                image_file = image_save(form.article_image.data, 'articles_images', (640, 360))
            except:
                abort(415) # Unsupported Media Type (RFC 7231)
            
            #Instanciate an article using models
            article = Article(article_title=article_title,
                         article_body=article_body,
                         author=current_user, 
                         article_image = image_file
                         )

            
        else:
            #Instanciate an article with an image using models
            article = Article(article_title=article_title,
                            article_body=article_body,
                            author=current_user
                            ) # We pass the whole user object to the author backreference but another way could be user_id=current_user.id
        #add article to database
        db.session.add(article)
        #commit changes to database
        db.session.commit()
        flash(f"Το άρθρο με τίτλο {article.article_title} δημιουργήθηκε με επιτυχία", "success")
        return redirect(url_for('root'))

    return render_template("new_article.html", form=form, page_title="Εισαγωγή Νέου Άρθρου")

@app.route("/full_article/<int:article_id>", methods=["GET"])
def full_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("full_article.html", article=article)

@app.route("/delete_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def delete_article(article_id):
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()
    if article: # it is not needed really because we use first_or_404
        db.session.delete(article)
        db.session.commit()

        flash(f"Το άρθρο με τίτλο {article.article_title} διαγράφηκε με επιτυχία", "success")

        return redirect(url_for('root'))
   
    flash(f"Το άρθρο δεν βρέθηκε", "warning")
    return redirect(url_for('root'))



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

        
        if form.profile_image.data:
            #we keep the old image path in order to delete the old image later from the storage
            old_image_path = os.path.join(app.root_path, 'static/images', 'profiles_images', current_user.profile_image)
            
            try: #because someone may bypass the validator and upload a file of another file type but with the right extension
                # image_save(image, where, size) returns the image_filename
                image_file = image_save(form.profile_image.data, 'profiles_images', (150, 150))
                current_user.profile_image = image_file

                #we remove the old image from the storage
                os.remove(old_image_path)
            except:
                abort(415) # Unsupported Media Type (RFC 7231)

            
        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b>{current_user.username}</b> ενημερώθηκε με επιτυχία", "success")

        return redirect(url_for('root'))
    
    return render_template("account_update.html", form=form)

@app.route("/edit_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    
    # check if exists and then if the current user is the author of the article
    """
    article = Article.query.get_or_404(article_id)
    if article:
        if article.author != current_user:
            abort(403)
    """
    # or more simply filter article and user at the same time
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()
    # we use the same form of new article because fields are the same
     # Pre-filling the fields with the found article's data
    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)
    #we should check the method of request
    if request.method == "POST" and form.validate_on_submit(): 
        # we update the fetched article
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data

        if form.article_image.data:
            
            #we keep the old image path in order to delete the old image later from the storage
            old_image_path = os.path.join(app.root_path, 'static/images', 'articles_images', article.article_image)
            
            try: #because someone may bypass the validator and upload a file of another file type but with the right extension
                # image_save(image, where, size) returns the image_filename
                image_file = image_save(form.article_image.data, 'articles_images', (640, 360))

                #we remove the old image from the storage
                os.remove(old_image_path)
            except:
                abort(415) # Unsupported Media Type (RFC 7231)
            
            # We change or add to an existing article
            article.article_image = image_file


        db.session.commit()
        
        flash(f"Το άρθρο με τίτλο <b>{article.article_title}</b> ενημερώθηκε με επιτυχία", "success")

        return redirect (url_for("root"))
    
    return render_template("new_article.html", form=form, page_title="Επεξεργασία Άρθρου")

