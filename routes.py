import random
from app import app, db
from flask import render_template, redirect, url_for, request, flash, session
from models import OptimizedRoute, User, Location, Route, Drivers
from forms import (
    LoginForm, RegisterForm, LocationForm, UploadLocationsForm,
    RenameRouteForm, EditDriverPriorityForm, DriverForm, UploadDriversForm
)
from utils import get_coordinates, run_optimization
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import csv
from io import StringIO
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        user = User.query.get(user_id)
        if not user:
            session.clear()
            flash('Session expired. Please log in again.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_current_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return {'current_user': user}
    return {'current_user': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('This email is not registered. Please register', 'error')
            return render_template('login.html', form=form)
        if user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Successful login', 'success')
            return redirect(url_for('index'))
        else:
            flash('Wrong password', 'error')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('This email has already been registered', 'error')
            return render_template('register.html', form=form)
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/view_routes')
@login_required
def view_routes():
    routes = Route.query.filter_by(user_id=session['user_id']).all()
    return render_template('view-routes.html', routes=routes)

@app.route('/create_route')
@login_required
def create_route():
    user_id = session['user_id']
    route_count = Route.query.filter_by(user_id=user_id).count()
    route_name = f'Route #{route_count + 1}'
    route = Route(
        name=route_name,
        user_id=user_id
    )
    db.session.add(route)
    db.session.commit()
    flash('A new route has been created', 'success')
    return redirect(url_for('view_routes'))

@app.route('/delete_route/<int:route_id>')
@login_required
def delete_route(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    
    # Clear optimized routes for this route
    OptimizedRoute.query.filter_by(route_id=route_id).delete()
    db.session.commit()

    # Now delete the route
    db.session.delete(route)
    db.session.commit()
    flash('The route has been deleted', 'success')
    return redirect(url_for('view_routes'))

@app.route('/view_route/<int:route_id>')
@login_required
def view_route(route_id):
    route = Route.query.get_or_404(route_id)
    
    # Query optimized routes for the current route ID, ordered by `order`
    optimized_routes = (
        OptimizedRoute.query
        .filter_by(route_id=route_id)
        .order_by(OptimizedRoute.order)
        .all()
    )
    return render_template(
        "view-one-route.html",
        route=route,
        optimized_routes=optimized_routes
    )

@app.route('/rename_route/<int:route_id>', methods=['GET', 'POST'])
@login_required
def rename_route(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    form = RenameRouteForm()
    if form.validate_on_submit():
        route.name = form.name.data
        db.session.commit()
        flash('The route name has been successfully changed', 'success')
        return redirect(url_for('view_route', route_id=route_id))
    elif request.method == 'GET':
        form.name.data = route.name
    return render_template('rename-route.html', route=route, form=form)

@app.route('/add_location/<int:route_id>', methods=['GET', 'POST'])
@login_required
def add_location(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    form = LocationForm()
    upload_form = UploadLocationsForm()

    if form.submit_location.data and form.validate_on_submit():
        country = form.country.data
        city = form.city.data
        address = form.address.data
        timeframe = form.timeframe.data

        latitude, longitude = get_coordinates(country, city, address)
        if latitude is None or longitude is None:
            return redirect(url_for('add_location', route_id=route_id))

        # Insert into locations
        location = Location(
            country=country,
            city=city,
            address=address,
            latitude=latitude,
            longitude=longitude,
            timeframe=timeframe,
            route_id=route_id
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully', 'success')

        # Re-run optimization
        run_optimization(route_id, session['user_id'])

        return redirect(url_for('view_route', route_id=route_id))
    elif upload_form.submit_upload.data and upload_form.validate_on_submit():
        file = upload_form.file.data
        filename = secure_filename(file.filename)
        if filename.endswith('.json') or filename.endswith('.csv'):
            try:
                data = []
                if filename.endswith('.json'):
                    data = json.load(file)
                else:
                    csv_reader = csv.DictReader(StringIO(file.read().decode('utf-8')))
                    for row in csv_reader:
                        data.append(row)

                for item in data:
                    country = item.get('country', '')
                    city = item.get('city', '')
                    address = item.get('address')
                    timeframe = item.get('timeframe', '')
                    latitude, longitude = get_coordinates(country, city, address)
                    if latitude is None or longitude is None:
                        continue
                    loc = Location(
                        country=country,
                        city=city,
                        address=address,
                        latitude=latitude,
                        longitude=longitude,
                        timeframe=timeframe,
                        route_id=route_id
                    )
                    db.session.add(loc)

                db.session.commit()
                flash('Locations loaded successfully', 'success')

                # Re-run optimization
                run_optimization(route_id, session['user_id'])

            except Exception as e:
                flash(f'Error processing file: {e}', 'error')
        else:
            flash('Invalid file format. Only JSON or CSV files are accepted', 'error')
        return redirect(url_for('view_route', route_id=route_id))
    return render_template('add-location.html', route=route, form=form, upload_form=upload_form)

@app.route('/delete_location/<int:location_id>')
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    if location.route.user_id != session['user_id']:
        flash('You do not have permission to delete this location', 'error')
        return redirect(url_for('view_routes'))
    route_id = location.route_id

    db.session.delete(location)
    db.session.commit()
    flash('Location has been removed', 'success')

    # Re-run optimization
    run_optimization(route_id, session['user_id'])

    return redirect(url_for('view_route', route_id=route_id))

@app.route('/view_route_map/<int:route_id>')
@login_required
def view_route_map(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    optimized_routes = (
        OptimizedRoute.query
        .filter_by(route_id=route_id, deliverable=True)
        .order_by(OptimizedRoute.driver_id, OptimizedRoute.order)
        .all()
    )
    
    driver_colors = {}
    locations_data = []
    grouped_routes = {}

    for opt in optimized_routes:
        driver = opt.driver
        driver_id = driver.id if driver else None

        if driver_id not in grouped_routes:
            grouped_routes[driver_id] = {'driver': driver, 'locations': []}

        grouped_routes[driver_id]['locations'].append({
            'latitude': opt.location.latitude,
            'longitude': opt.location.longitude,
            'address': opt.location.address,
            'order': len(grouped_routes[driver_id]['locations']) + 1,
            'depot': driver.depot_address if driver else None,
        })

    import random
    for driver_id, data in grouped_routes.items():
        if driver_id not in driver_colors:
            driver_colors[driver_id] = f"#{''.join([format(i, '02x') for i in (random.randint(0, 255) for _ in range(3))])}"

        for loc in data['locations']:
            loc['driver'] = f"{data['driver'].name} {data['driver'].surname}" if data['driver'] else "No Driver"
            loc['color'] = driver_colors.get(driver_id, '#007BFF') 
            locations_data.append(loc)

    locations_json = json.dumps(locations_data, ensure_ascii=False)
    return render_template('view-route-map.html', route=route, locations_json=locations_json)

@app.route('/export_route/<int:route_id>')
@login_required
def export_route(route_id):
    """
    Exports data from the OptimizedRoute table
    so the user can see the result of the algorithm.
    """
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    optimized_locations = (
        OptimizedRoute.query
        .filter_by(route_id=route_id)
        .order_by(OptimizedRoute.order)
        .all()
    )
    data = []
    for opt in optimized_locations:
        loc = opt.location
        driver_str = (
            f"{opt.driver.name} {opt.driver.surname} [Priority={opt.driver.priority}]"
            if opt.driver else
            "No Driver"
        )
        data.append({
            'address': loc.address,
            'coordinates': f'{loc.latitude}, {loc.longitude}',
            'timeframe': loc.timeframe,
            'driver': driver_str,
            'estimated_arrival': opt.estimated_arrival,
            'deliverable': opt.deliverable
        })

    response = app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename=optimized_route_{route_id}.json'}
    )
    return response

@app.route('/export_locations/<int:route_id>')
@login_required
def export_locations(route_id):
    """
    Exports data from the Location table (raw locations),
    without the optimization details.
    """
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    locations = route.locations
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['address', 'coordinates', 'timeframe'])
    for loc in locations:
        writer.writerow([
            loc.address,
            f'{loc.latitude}, {loc.longitude}',
            loc.timeframe
        ])
    output = si.getvalue()
    response = app.response_class(
        response=output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename=locations_{route_id}.csv'}
    )
    return response

@app.route('/view_drivers')
@login_required
def view_drivers():
    user_id = session['user_id']
    drivers = Drivers.query.filter_by(user_id=user_id).all()
    return render_template('view-drivers.html', drivers=drivers)

@app.route('/edit_driver_priority/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def edit_driver_priority(driver_id):
    user_id = session['user_id']
    driver = Drivers.query.filter_by(id=driver_id, user_id=user_id).first_or_404()
    form = EditDriverPriorityForm()
    if form.validate_on_submit():
        driver.priority = form.priority.data
        db.session.commit()
        flash('Driver priority updated successfully', 'success')
        return redirect(url_for('view_drivers'))
    elif request.method == 'GET':
        form.priority.data = driver.priority
    return render_template('edit-driver-priority.html', form=form, driver=driver)

@app.route('/add_driver', methods=['GET', 'POST'])
@login_required
def add_driver():
    user_id = session['user_id']
    driver_form = DriverForm()
    upload_form = UploadDriversForm()

    if driver_form.submit_driver.data and driver_form.validate_on_submit():
        new_driver = Drivers(
            name=driver_form.name.data,
            surname=driver_form.surname.data,
            tel_num=driver_form.tel_num.data,
            depot_address=driver_form.depot_address.data,
            priority=driver_form.priority.data,
            user_id=user_id
        )
        db.session.add(new_driver)
        db.session.commit()
        flash('Driver added successfully', 'success')
        return redirect(url_for('view_drivers'))

    elif upload_form.submit_upload_drivers.data and upload_form.validate_on_submit():
        file = upload_form.file.data
        filename = secure_filename(file.filename)
        if filename.endswith('.json') or filename.endswith('.csv'):
            try:
                data = []
                if filename.endswith('.json'):
                    data = json.load(file)
                else:
                    csv_reader = csv.DictReader(StringIO(file.read().decode('utf-8')))
                    for row in csv_reader:
                        data.append(row)

                for item in data:
                    name = item.get('name')
                    surname = item.get('surname')
                    tel_num = item.get('tel_num', 0)
                    depot_address = item.get('depot_address', '')
                    priority = item.get('priority', 1)

                    if not name or not surname or not depot_address:
                        continue

                    new_drv = Drivers(
                        name=name,
                        surname=surname,
                        tel_num=int(tel_num),
                        depot_address=depot_address,
                        priority=int(priority),
                        user_id=user_id
                    )
                    db.session.add(new_drv)

                db.session.commit()
                flash('Drivers uploaded successfully', 'success')
            except Exception as e:
                flash(f'Error processing file: {e}', 'error')
        else:
            flash('Invalid file format. Only JSON or CSV files are accepted', 'error')

        return redirect(url_for('view_drivers'))

    return render_template('add-driver.html', driver_form=driver_form, upload_form=upload_form)

@app.route('/delete_driver/<int:driver_id>')
@login_required
def delete_driver(driver_id):
    user_id = session['user_id']
    driver = Drivers.query.filter_by(id=driver_id, user_id=user_id).first_or_404()
    
    db.session.delete(driver)
    db.session.commit()
    
    flash('Driver has been removed', 'success')
    return redirect(url_for('view_drivers'))
