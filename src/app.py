from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route ("/index/")
@app.route ("/")
@app.route ("/<name>")
def root(name=None):
    return render_template("index.html", myname=name)

@app.route ("/books/")
def books():
    with open("src/mybooks.json") as json_file:
        jlist = json.load(json_file)
        # print(jlist) #prints to console
    return render_template("books.html", jlist=jlist)


@app.route ("/hello/")
@app.route("/hello/<int:id>")
def hello(id=None):
    return f"hello {id}"

if __name__ == '__main__':
    app.run(debug=True)
