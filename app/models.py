from dataclasses import dataclass
from app import db
from flask_login import UserMixin
from app import login
from sqlalchemy_serializer import SerializerMixin
import datetime


class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (datetime, lambda x: str(x)),
    )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    user_name =  db.Column(db.String(120), index=True)
    google_id = db.Column(db.String(120), index=True)
    cars = db.relationship("Car", backref="car_user", lazy=True)
    routes = db.relationship("Route", backref="car_user",lazy=True)
    

    def __repr__(self):
        return '{}'.format(self.username)

# @dataclass
class Car(db.Model,CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    SPZ = db.Column(db.String(10), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=False)
    VIN = db.Column(db.String(50), index=True, unique=True)
    leasing_company = db.Column(db.String(120), index=True, unique=False, nullable=True)
    leased_until = db.Column(db.DateTime,index=True, nullable=True)
    insurance_company = db.Column(db.String(120), index=True, unique=False, nullable=True)
    insured_until = db.Column(db.DateTime,index=True, nullable=True)
    highway = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    cars = db.relationship("Route", backref="car_spz", lazy=True)

    def __repr__(self):
        return '<Car {}, {}>'.format(self.SPZ,self.description)
    
    def obj_to_dict(self):
        return {
            "id" :self.id ,
            "SPZ" :self.SPZ,
            "description" :self.description,
            "VIN"  :self.VIN,
            "leasing_company" :self.leasing_company,
            "leased_until"  :self.leased_until,
            "insurance_company"  :self.insurance_company,
            "insured_until"  :self.insured_until,
            "highway" :self.highway,
            "user_id"  :self.user_id
        }

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=True)
    route_desc = db.Column(db.String(120), index=True)
    route_purpose = db.Column(db.Integer)
    date = db.Column(db.DateTime,index=True, nullable=True)
    own_gas = db.Column(db.Integer)
    route_length = db.Column(db.Integer)

    def __repr__(self):
        return '<Route {}, {}>'.format(self.route_desc,self.route_length)



