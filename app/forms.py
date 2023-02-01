from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,RadioField, SelectField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange
from app.models import User, Car

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def get_users():
    choices = list()
    users = User.query.order_by(User.username)
    for user in users:  # <- assumes store_id and store_names are unique
        choices.append((user.id,user))
    return choices

class AddCarForm(FlaskForm):
    SPZ = StringField('SPZ', validators=[DataRequired()])
    description = StringField('Popis', validators=[DataRequired()])
    VIN = StringField("VIN", validators=[DataRequired()])
    leasing_company = StringField("Leasingová společnost", validators=[Optional()])
    leased_until = DateField("Leasnuto do", validators=[Optional()])
    insurance_company = StringField("Pojišťovna", validators=[Optional()])
    insured_until = DateField("Pojištěno do", validators=[Optional()])
    highway = DateField("Dálniční známka do", validators=[Optional()])
    user_id = SelectField("Uživatel", choices=get_users, validators=[Optional()])
    submit = SubmitField('Submit')


def get_cars():
    choices = list()
    cars = Car.query.order_by(Car.SPZ)
    for car in cars:  # <- assumes store_id and store_names are unique
        choices.append((car.id,car.SPZ))
    return choices

class RouteOps(FlaskForm):
    car = SelectField("SPZ", choices=get_cars, validators=[DataRequired()])
    driver = SelectField("Uživatel", choices=get_users, validators=[DataRequired()])
    route_desc = StringField('Popis', validators=[DataRequired()])
    route_purpose = RadioField("Účel cesty", coerce=int, choices=[(1, "Služebně"),(2,"Soukromě")], validators=[DataRequired()])
    date = DateField("Datum cesty", validators=[DataRequired()])
    own_gas = BooleanField('Vlastní palivo', validators=[Optional()])
    route_length = IntegerField("Počet KM", validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Submit')