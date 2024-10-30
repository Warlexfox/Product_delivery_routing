from app import app, db
from flask import render_template, redirect, url_for, request, flash
from models import Location
from forms import LocationForm, UploadLocationsForm
from utils import get_coordinates, solomon_algorithm
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        address = form.address.data
        latitude, longitude = get_coordinates(address)
        if latitude is not None and longitude is not None:
            location = Location(
                address=address,
                latitude=latitude,
                longitude=longitude,
                demand=form.demand.data,
                ready_time=form.ready_time.data,
                due_time=form.due_time.data,
                service_time=form.service_time.data
            )
            db.session.add(location)
            db.session.commit()
            flash('Lokācija veiksmīgi pievienota.', 'success')
            return redirect(url_for('view_locations'))
        else:
            flash('Neizdevās iegūt koordinātes adresei.', 'error')
    return render_template('add_location.html', form=form)

@app.route('/upload_locations', methods=['GET', 'POST'])
def upload_locations():
    form = UploadLocationsForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            try:
                file_content = file.read()
                if isinstance(file_content, bytes):
                    file_content = file_content.decode('utf-8-sig')
                file_content = file_content.strip()
                if not file_content:
                    flash('Fails ir tukšs.', 'error')
                    return redirect(request.url)
                data = json.loads(file_content)
                if not isinstance(data, list):
                    flash('Nekorekts datu formāts: tika gaidīts lokāciju saraksts.', 'error')
                    return redirect(request.url)
                for item in data:
                    address = item.get('address')
                    demand = item.get('demand', 0)
                    ready_time = item.get('ready_time', 0)
                    due_time = item.get('due_time', 1440)
                    service_time = item.get('service_time', 0)
                    if not address:
                        flash('Nekorekti dati failā: nav norādīta adrese.', 'error')
                        continue
                    latitude, longitude = get_coordinates(address)
                    if latitude is not None and longitude is not None:
                        location = Location(
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                            demand=demand,
                            ready_time=ready_time,
                            due_time=due_time,
                            service_time=service_time
                        )
                        db.session.add(location)
                    else:
                        flash(f"Neizdevās iegūt koordinātes adresei: {address}.", 'error')
                db.session.commit()
                flash('Lokācijas veiksmīgi augšupielādētas.', 'success')
                return redirect(url_for('view_locations'))
            except json.JSONDecodeError as e:
                flash(f'Kļūda, augšupielādējot lokācijas: nekorekts JSON. {e}', 'error')
                return redirect(request.url)
            except Exception as e:
                flash(f'Kļūda, augšupielādējot lokācijas: {e}', 'error')
                return redirect(request.url)
        else:
            flash('Fails nav izvēlēts.', 'error')
    return render_template('upload_locations.html', form=form)

@app.route('/view_locations')
def view_locations():
    locations = Location.query.all()
    return render_template('view_locations.html', locations=locations)

@app.route('/generate_optimized_routes', methods=['GET'])
def generate_optimized_routes():
    locations = Location.query.all()
    if not locations:
        flash('Nav pieejamu lokāciju optimizācijai.', 'error')
        return redirect(url_for('index'))
    vehicle_capacity = 100
    optimized_routes = solomon_algorithm(locations, vehicle_capacity)
    if not optimized_routes:
        flash('Neizdevās ģenerēt maršrutus ar pašreizējiem datiem.', 'error')
        return redirect(url_for('view_locations'))
    routes_data = []
    for idx, route in enumerate(optimized_routes):
        print(f"Maršruts {idx+1}: {[loc.address for loc in route]}")
        route_data = []
        for location in route:
            route_data.append({
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address
            })
        routes_data.append(route_data)
    return render_template('optimized_routes.html', routes=routes_data)
