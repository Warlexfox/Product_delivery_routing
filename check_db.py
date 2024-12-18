from app import db, app
from models import Drivers

def check_drivers():
    drivers = Drivers.query.all()
    for driver in drivers:
        print(f'Driver ID: {driver.id}, Name: {driver.name}, Surname: {driver.surname}, Tel: {driver.tel_num}, Depo: {driver.depot_address}')

if __name__ == "__main__":
    with app.app_context():
        check_drivers()
