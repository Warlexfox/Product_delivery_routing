from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Import models and routes after initializing app and db
from models import User, Drivers, Route, Location, OptimizedRoute
import routes

from utils import run_optimization

def seed_database():
    if User.query.first():
        print('Database already contains data. Skipping seeding.')
        return

    # Add a test user
    test_user = User(email='1@mail.com')
    test_user.set_password('1')
    db.session.add(test_user)
    db.session.commit()

    # Add a test route
    test_route = Route(name='Test Route NR.1', user=test_user)
    db.session.add(test_route)
    db.session.commit()

    # Add drivers for the user
    driver1 = Drivers(
        name='Jānis',
        surname='Bērziņš',
        user_id=test_user.id,
        tel_num=12345678,
        depot_address='Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004',
        priority=1
    )
    driver2 = Drivers(
        name='Kārlis',
        surname='Liepa',
        user_id=test_user.id,
        tel_num=20202020,
        depot_address='Kandavas iela 3, Daugavpils, LV-5401',
        priority=2
    )
    driver3 = Drivers(
        name='Sergejs',
        surname='Zembkovskis',
        user_id=test_user.id,
        tel_num=20202020,
        depot_address='Skolas iela 3, Ventspils, LV-3601',
        priority=3
    )
    db.session.add_all([driver1, driver2, driver3])
    db.session.commit()

    # Add locations for the test route
    location_1 = Location(
        country='Latvia',
        city='Riga',
        address='Brivibas iela 1',
        latitude=56.950929,
        longitude=24.082404,
        timeframe='09:00-10:00',
        route_id=test_route.id,
    )
    location_2 = Location(
        country='Latvia',
        city='Riga',
        address='Daugavgrivas iela 2',
        latitude=56.959268,
        longitude=24.055293,
        timeframe='10:00-11:00',
        route_id=test_route.id,
    )
    location_3 = Location(
        country='Latvia',
        city='Daugavpils',
        address='Rīgas iela 1',
        latitude=55.870231,
        longitude=26.513495,
        timeframe='09:00-10:00',
        route_id=test_route.id,
    )
    location_4 = Location(
        country='Latvia',
        city='Ilukste',
        address='Kastanu iela 3',
        latitude=55.981721,
        longitude=26.285224,
        timeframe='10:00-11:00',
        route_id=test_route.id,
    )
    location_5 = Location(
        country='Latvia',
        city='Liepaja',
        address='Skolas iela 1',
        latitude=56.511127,
        longitude=21.015855,
        timeframe='10:30-11:30',
        route_id=test_route.id,
    )
    location_6 = Location(
        country='Latvia',
        city='Ventspils',
        address='Rīgas iela 1',
        latitude=57.393644,
        longitude=21.559496,
        timeframe='09:00-10:00',
        route_id=test_route.id,
    )
    db.session.add_all([location_1, location_2, location_3, location_4, location_5, location_6])
    db.session.commit()

    print('Test data inserted.')

    # Run optimization for the test route
    run_optimization(test_route.id, test_user.id)
    print('Optimization completed after seeding data.')


with app.app_context():
    db.drop_all()
    db.create_all()
    seed_database()
    print('Database initialized and test data inserted.')

if __name__ == '__main__':
    app.run(debug=True)
