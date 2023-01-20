from app import app
from flask import render_template

@app.route("/")
@app.route("/index")
def index():
    username= "Marek"
    return render_template("index.html", title="home", username=username)