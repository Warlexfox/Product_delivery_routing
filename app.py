from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from models import User, Drivers, Route, Location
import routes

def seed_database():
    if User.query.first():
        print('Database already contains data. Skipping seeding.')
        return

    # Add a test user
    test_user = User(email='1@mail.com')
    test_user.set_password('1')
    db.session.add(test_user)
    db.session.commit()

    # Add routes
    test_route = Route(name='Test Route NR.1', user=test_user)
    db.session.add(test_route)
    db.session.commit()

    # Add drivers for the user
    driver1 = Drivers(
        name='Jānis',
        surname='Bērziņš',
        user_id=test_user.id,
        tel_num=12345678,
        depot_address='Rīga, Latvija',
        priority=3
    )
    driver2 = Drivers(
        name='Kārlis',
        surname='Liepa',
        user_id=test_user.id,
        tel_num=20202020,
        depot_address='Rēzekne, Latvija',
        priority=2
    )
    db.session.add_all([driver1, driver2])
    db.session.commit()

    # Add locations and assign them a driver
    # Assign first location to driver1, second to driver2
    location_1 = Location(
        address='Āzenes iela 6, Rīga, Latvija',
        latitude=56.950929,
        longitude=24.082404,
        priority=1,
        timeframe='08:00-09:00',
        route_id=test_route.id,
        driver_id=driver1.id
    )
    location_2 = Location(
        address='Lielezeres iela 10, Rīga, Latvija',
        latitude=56.959268,
        longitude=24.055293,
        priority=2,
        timeframe='09:00-10:00',
        route_id=test_route.id,
        driver_id=driver2.id
    )
    db.session.add_all([location_1, location_2])
    db.session.commit()

    print('Test data inserted.')

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_database()
    print('Database initialized and test data inserted.')

if __name__ == '__main__':
    app.run(debug=True)
