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
    locations_28 = [
    Location(country='Latvia', city='Riga', address='Brīvības iela 10', latitude=56.9519, longitude=24.1132, timeframe='09:00-10:00', route_id=test_route.id),
    Location(country='Latvia', city='Riga', address='Daugavgrīvas iela 15', latitude=56.9672, longitude=24.0327, timeframe='10:00-11:00', route_id=test_route.id),
    Location(country='Latvia', city='Riga', address='Tērbatas iela 33', latitude=56.9574, longitude=24.1239, timeframe='11:00-12:00', route_id=test_route.id),
    Location(country='Latvia', city='Riga', address='Kr.Valdemāra iela 12', latitude=56.9589, longitude=24.1114, timeframe='12:00-13:00', route_id=test_route.id),
    Location(country='Latvia', city='Riga', address='Ģertrūdes iela 23', latitude=56.9515, longitude=24.1284, timeframe='13:00-14:00', route_id=test_route.id),
    Location(country='Latvia', city='Riga', address='Maskavas iela 260', latitude=56.9208, longitude=24.1737, timeframe='14:00-15:00', route_id=test_route.id),
    Location(country='Latvia', city='Liepaja', address='Ganību iela 21', latitude=56.5077, longitude=21.0139, timeframe='10:00-11:00', route_id=test_route.id),
    Location(country='Latvia', city='Liepaja', address='Zivju iela 12', latitude=56.5098, longitude=21.0145, timeframe='11:00-12:00', route_id=test_route.id),
    Location(country='Latvia', city='Daugavpils', address='Rīgas iela 10', latitude=55.8704, longitude=26.5141, timeframe='09:00-10:00', route_id=test_route.id),
    Location(country='Latvia', city='Daugavpils', address='Cietokšņa iela 1', latitude=55.8710, longitude=26.5359, timeframe='12:00-13:00', route_id=test_route.id),
    Location(country='Latvia', city='Ventspils', address='Lielais prospekts 35', latitude=57.3942, longitude=21.5731, timeframe='14:00-15:00', route_id=test_route.id),
    Location(country='Latvia', city='Ventspils', address='Tirgus iela 5', latitude=57.3908, longitude=21.5691, timeframe='15:00-16:00', route_id=test_route.id),
    Location(country='Latvia', city='Valmiera', address='Rīgas iela 20', latitude=57.5386, longitude=25.4233, timeframe='10:00-11:00', route_id=test_route.id),
    Location(country='Latvia', city='Valmiera', address='Bastiona iela 8', latitude=57.5380, longitude=25.4279, timeframe='11:00-12:00', route_id=test_route.id),
    Location(country='Latvia', city='Sigulda', address='Pils iela 16', latitude=57.1539, longitude=24.8545, timeframe='12:00-13:00', route_id=test_route.id),
    Location(country='Latvia', city='Sigulda', address='Dārza iela 9', latitude=57.1524, longitude=24.8582, timeframe='13:00-14:00', route_id=test_route.id),
    Location(country='Latvia', city='Ogre', address='Brīvības iela 2', latitude=56.8177, longitude=24.6134, timeframe='11:00-12:00', route_id=test_route.id),
    Location(country='Latvia', city='Ogre', address='Tīnūžu iela 14', latitude=56.8147, longitude=24.6195, timeframe='12:00-13:00', route_id=test_route.id),
    Location(country='Latvia', city='Cēsis', address='Rīgas iela 18', latitude=57.3127, longitude=25.2670, timeframe='10:00-11:00', route_id=test_route.id),
    Location(country='Latvia', city='Cēsis', address='Vienības laukums 1', latitude=57.3136, longitude=25.2707, timeframe='11:00-12:00', route_id=test_route.id),
    Location(country='Latvia', city='Jēkabpils', address='Madonas iela 5', latitude=56.4977, longitude=25.8544, timeframe='09:00-10:00', route_id=test_route.id),
    Location(country='Latvia', city='Saldus', address='Kalna iela 7', latitude=56.6620, longitude=22.4881, timeframe='13:00-14:00', route_id=test_route.id),
    Location(country='Latvia', city='Dobele', address='Bērzes iela 8', latitude=56.6228, longitude=23.2789, timeframe='14:00-15:00', route_id=test_route.id),
    Location(country='Latvia', city='Dobele', address='Tirgoņu iela 10', latitude=56.6220, longitude=23.2772, timeframe='15:00-16:00', route_id=test_route.id),
    Location(country='Latvia', city='Rēzekne', address='Atbrīvošanas aleja 93', latitude=56.5078, longitude=27.3433, timeframe='09:00-10:00', route_id=test_route.id),
    Location(country='Latvia', city='Kuldīga', address='Kalna iela 5', latitude=56.9682, longitude=21.9750, timeframe='12:00-13:00', route_id=test_route.id),
    Location(country='Latvia', city='Talsi', address='Kroņu iela 4', latitude=57.2465, longitude=22.5882, timeframe='10:00-11:00', route_id=test_route.id),
    Location(country='Latvia', city='Talsi', address='Saules iela 12', latitude=57.2471, longitude=22.5827, timeframe='11:00-12:00', route_id=test_route.id)
]

    db.session.add_all(locations_28)
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
