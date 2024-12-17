from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config


# Aplikācijas un konfigurācijas inicializācija
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Importē modeļus un maršrutus
from models import User, Drivers, Route, Location
import routes

def seed_database():
    # Pārbauda, vai ir vismaz viens lietotājs
    if User.query.first():
        print('Datu bāze jau satur datus. Pārlēcam sēšanas soli.')
        return

    # Pievieno testa lietotāju
    test_user = User(email='1@mail.com')
    test_user.set_password('1')
    db.session.add(test_user)

    # Pievieno testa maršrutu
    test_route = Route(name='Test Route NR.1', user=test_user)
    db.session.add(test_route)
    db.session.commit()

    # Pievieno atrašanās vietas
    location_1 = Location(
        address='Āzenes iela 6, Rīga, Latvija', latitude=56.950929, longitude=24.082404,
        priority=1, timeframe='08:00-09:00', route_id=test_route.id
    )
    location_2 = Location(
        address='Lielezeres iela 10, Rīga, Latvija', latitude=56.959268, longitude=24.055293,
        priority=2, timeframe='09:00-10:00', route_id=test_route.id
    )
    db.session.add_all([location_1, location_2])
    db.session.commit()

    # Pievieno konkrētu vadītāju
    specific_driver = Drivers(
        name='Jānis',
        surname='Bērziņš',
        user_id=test_user.id,
        tel_num=12345678,
        depot_address='Rīga, Latvija'
    )
    # Ja nepieciesams pievienot vairakus vaditajus, tad jakope dati un javeido lidzigi ka ar location, obligati pievienojot add_all
    specific_driver2 = Drivers(
        name='Kārlis',
        surname='Liepa',
        user_id=test_user.id,
        tel_num=20202020,
        depot_address='Rēzekne, Latvija'
    )
    db.session.add_all([specific_driver, specific_driver2])
    db.session.commit()

    print('Testa dati pievienoti.')
    
# Datu bāzes inicializācija ar testa datiem
with app.app_context():
    db.drop_all()
    db.create_all()
    seed_database()
    print('Datu bāze inicializēta un pievienoti testi dati.')

if __name__ == '__main__':
    app.run(debug=True)

    # Pagaidām flask run nedarbojas 18:27
