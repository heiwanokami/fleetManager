from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cars = db.relationship("Car", backref="car_user", lazy=True)
    routes = db.relationship("Route", backref="car_user",lazy=True)
    

    def __repr__(self):
        return '{}'.format(self.username)

class Car(db.Model):
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

class RoutePurpose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique = True)
    desc = db.Column(db.String(60))


