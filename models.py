from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    routes = db.relationship('Route', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
  
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    locations = db.relationship('Location', backref='route', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Route {self.name}>"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    timeframe = db.Column(db.String(50), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)

    # New field: link a driver to a location
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    driver = db.relationship('Drivers', backref='locations', lazy=True)

    def __repr__(self):
        return f"<Location {self.address}>"


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tel_num = db.Column(db.Integer, nullable=False)
    depot_address = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref='drivers', lazy=True)

    def __repr__(self):
        return f"<Driver {self.name} {self.surname} Priority={self.priority}>"
