from sqlalchemy import func
from app import app, db
from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm, AddCarForm, RouteOps
from app.models import Car, Route

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
    if form.validate_on_submit() and form.validate():
        car = Car(SPZ = form.SPZ.data,
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


@app.route("/edit_car/<int:car_id>", methods=['GET', 'POST'])
def edit_car(car_id):

    item = db.session.query(Car).get(car_id)

    form = AddCarForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('cars'))

    return render_template('add_car.html', form=form)

@app.route("/routes")
def routes():
    routes = Route.query.all()
    return render_template("routes.html", title="Routes", routes= routes)


@app.route("/newroute", methods=['GET', 'POST'])
def new_route():
    form = RouteOps()
    if form.validate_on_submit() and form.validate():
        car = Route(driver = form.driver.data,
                  car = form.car.data,
                  route_desc = form.route_desc.data,
                  route_purpose = form.route_purpose.data,
                  date = form.date.data,
                  own_gas = form.own_gas.data,
                  route_length = form.route_length.data
                  )       
        db.session.add(car)
        db.session.commit()
        # flash('Congratulations, you created a new car! userid: {}'.format(form.user_id))
        # flash('AddCar requested for car {}, SPZ: {}, leased_until: {}'.format(
            # form.description.data, form.spz.data, form.leased_until.data))
        return redirect(url_for('index'))
    return render_template("new_route.html", title="Nová Cesta", form = form)


@app.route("/edit_route/<int:route_id>", methods=['GET', 'POST'])
def edit_route(route_id):

    item = db.session.query(Route).get(route_id)

    form = RouteOps(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('routes'))

    return render_template('new_route.html', form=form)

@app.route("/get_km/<int:car_id>", methods=['GET', 'POST'])
def get_total_km(car_id):

    item = db.session.query(func.sum(Route.route_length)).filter(Route.car == car_id).one()[0]
    if item == None:
        item = 0

    return str(item)

