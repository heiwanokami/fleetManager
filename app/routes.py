from app import app
from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm, AddCarForm

@app.route("/")
@app.route("/index")
def index():
    username= "Marek"
    return render_template("index.html", title="home", username=username)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign In", form = form)

@app.route("/cars")
def cars():
    return render_template("cars.html", title="Cars")

@app.route("/addcar", methods=['GET', 'POST'])
def add_car():
    form = AddCarForm()
    if form.validate_on_submit():
        flash('AddCar requested for car {}, SPZ: {}, leased_until: {}'.format(
            form.description.data, form.SPZ.data, form.leased_until.data))
        return redirect(url_for('index'))
    return render_template("add_car.html", title="Add Car", form = form)