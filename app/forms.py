from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def get_users():
    return User.query.all()

class AddCarForm(FlaskForm):
    spz = StringField('SPZ', validators=[DataRequired()])
    description = StringField('Popis', validators=[DataRequired()])
    VIN = StringField("VIN", validators=[DataRequired()])
    leasing_company = StringField("Leasingová společnost")
    leased_until = DateField("Leasnuto do")
    insurance_company = StringField("POjišťovna")
    insurance_until = DateField("Pojištěno do")
    highway = DateField("Dálniční známka do")
    user_id = SelectField("Uživatel", choices=get_users)
    submit = SubmitField('Submit')