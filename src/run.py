from FlaskBlogApp import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080') #host='0.0.0.0' to be able to access it from anywhere not only from localhost

