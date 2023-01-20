from app import app, db
from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm, AddCarForm
from app.models import Car

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
    cars = Car.query.all()
    return render_template("cars.html", title="Cars", cars= cars)

@app.route("/addcar", methods=['GET', 'POST'])
def add_car():
    form = AddCarForm()
    if form.validate_on_submit():
        car = Car(SPZ = form.spz.data,
                  description = form.description.data,
                  VIN = form.VIN.data,
                  leasing_company = form.leasing_company.data,
                  leased_until = form.leased_until.data,
                  insurance_company = form.insurance_company.data,
                  insured_until = form.insured_until.data,
                  highway = form.highway.data,
                  user_id =form.user_id.data
                  )       
        db.session.add(car)
        db.session.commit()
        # flash('Congratulations, you created a new car! userid: {}'.format(form.user_id))
        # flash('AddCar requested for car {}, SPZ: {}, leased_until: {}'.format(
            # form.description.data, form.spz.data, form.leased_until.data))
        return redirect(url_for('cars'))
    return render_template("add_car.html", title="Add Car", form = form)
