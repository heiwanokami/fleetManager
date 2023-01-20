from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SPZ = db.Column(db.String(10), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=False)
    VIN = db.Column(db.String(50), index=True, unique=True)
    leasing_company = db.Column(db.String(120), index=True, unique=False)
    leased_until = db.Column(db.DateTime,index=True)
    insurence_company = db.Column(db.String(120), index=True, unique=False)
    insureded_until = db.Column(db.DateTime,index=True)
    highway = db.column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Car {}, {}>'.format(self.SPZ,self.description)