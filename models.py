from app import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    demand = db.Column(db.Float, nullable=False)
    ready_time = db.Column(db.Float, nullable=False)
    due_time = db.Column(db.Float, nullable=False)
    service_time = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Location {self.address}>"
