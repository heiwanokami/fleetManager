import os
import pathlib
from urllib.parse import urlparse
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow 
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_login import current_user, login_user, logout_user,login_required

from sqlalchemy import func
from app import app, db
from flask import render_template, redirect, flash, url_for, jsonify
from app.forms import LoginForm, AddCarForm, RouteOps
from app.models import Car, Route, User

GOOGLE_CLIENT_ID = "320557972351-45t22fcflec03q8er86pp93aqdike9uh.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is
flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)



@app.route("/")
@app.route("/index")
@login_required
def index():
    username= "Marek"
    try:
        session["name"]
        username = current_user.username
    except:
        username = "Please log in"
    return render_template("index.html", title="home", username=username)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("login.html", title="Přihlášení")

@app.route("/cars")
@login_required
def cars():
    cars = Car.query.all()
    return render_template("cars.html", title="Cars", cars= cars)

def dict_helper(objlist):
    if isinstance(objlist, list):
        result2 = [item.obj_to_dict() for item in objlist]
    else:
        result2 = objlist.obj_to_dict()
    return result2

@app.route("/carsapi")
@login_required
def cars_api():
    cars = Car.query.all()
    # flash(cars)
    dict = dict_helper(cars)
    return jsonify(dict)

@app.route("/addcar", methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def routes():
    routes = Route.query.all()
    return render_template("routes.html", title="Routes", routes= routes)


@app.route("/newroute", methods=['GET', 'POST'])
@login_required
def new_route():
    default_car = Car.query.filter_by(user_id=current_user.id).first()
    if default_car:
        default_car_id = default_car.id
    else:
        default_car_id=0
    form = RouteOps(driver=current_user.id, car=default_car_id)
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
        return redirect(url_for('routes'))
    return render_template("new_route.html", title="Nová Cesta", form = form)


@app.route("/edit_route/<int:route_id>", methods=['GET', 'POST'])
@login_required
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
@login_required
def get_total_km(car_id):

    item = db.session.query(func.sum(Route.route_length)).filter(Route.car == car_id).one()[0]
    if item == None:
        item = 0

    return str(item)


@app.route("/processlogin")  #the page where the user can login
def start_login():
    authorization_url, state = flow.authorization_url()  #asking thue flow class for the athorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    
    username = session["email"].split("@")[0]
    session["username"] = username



    if not User.query.filter_by(email = session["email"] ).first():

        user = User(user_name = session["name"], username = username, email = session["email"], google_id = sesison["google_id"])
        db.session.add(user)
        db.session.commit()

    login_user(User.query.filter_by(email = session["email"] ).first())
    next_page = request.args.get('next')
    if not next_page or urlparse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)



@app.route("/logout")  #the logout page and function
def logout():
    logout_user()
    session.clear()
    return redirect("/")

