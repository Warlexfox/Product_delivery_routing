from app import app, db
from flask import render_template, redirect, url_for, request, flash, session
from models import OptimizedRoute, User, Location, Route, Drivers
from forms import LoginForm, RegisterForm, LocationForm, UploadLocationsForm, RenameRouteForm, EditDriverPriorityForm
from utils import get_coordinates
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
        priority = form.priority.data
        timeframe = form.timeframe.data

        latitude, longitude = get_coordinates(country, city, address)
        if latitude is None or longitude is None:
            return redirect(url_for('add_location', route_id=route_id))
        location = Location(
            country=country,
            city=city,
            address=address,
            latitude=latitude,
            longitude=longitude,
            priority=int(priority),
            timeframe=timeframe,
            route_id=route_id
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully', 'success')
        return redirect(url_for('view_route', route_id=route_id))
    elif upload_form.submit_upload.data and upload_form.validate_on_submit():
        file = upload_form.file.data
        filename = secure_filename(file.filename)
        if filename.endswith('.json') or filename.endswith('.csv'):
            try:
                if filename.endswith('.json'):
                    data = json.load(file)
                else:
                    data = []
                    csv_reader = csv.DictReader(StringIO(file.read().decode('utf-8')))
                    for row in csv_reader:
                        data.append(row)
                for item in data:
                    country = item.get('country', '')
                    city = item.get('city', '')
                    address = item.get('address')
                    priority = item.get('priority', '1')
                    timeframe = item.get('timeframe', '')
                    latitude, longitude = get_coordinates(country, city, address)
                    if latitude is None or longitude is None:
                        continue
                    location = Location(
                        country=country,
                        city=city,
                        address=address,
                        latitude=latitude,
                        longitude=longitude,
                        priority=int(priority),
                        timeframe=timeframe,
                        route_id=route_id
                    )
                    db.session.add(location)
                db.session.commit()
                flash('Locations loaded successfully', 'success')
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
    return redirect(url_for('view_route', route_id=route_id))

@app.route('/view_route_map/<int:route_id>')
@login_required
def view_route_map(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    locations = route.locations
    locations_data = [{
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'address': loc.address
    } for loc in locations]
    locations_json = json.dumps(locations_data, ensure_ascii=False)
    return render_template('view-route-map.html', route=route, locations_json=locations_json)

@app.route('/export_route/<int:route_id>')
@login_required
def export_route(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    locations = route.locations
    data = [{
        'address': loc.address,
        'coordinates': f'{loc.latitude}, {loc.longitude}',
        'priority': loc.priority,
        'timeframe': loc.timeframe
    } for loc in locations]
    response = app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename=route_{route_id}.json'}
    )
    return response

@app.route('/export_locations/<int:route_id>')
@login_required
def export_locations(route_id):
    route = Route.query.filter_by(id=route_id, user_id=session['user_id']).first_or_404()
    locations = route.locations
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['address', 'coordinates', 'priority', 'timeframe'])
    for loc in locations:
        writer.writerow([
            loc.address,
            f'{loc.latitude}, {loc.longitude}',
            loc.priority,
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
    # Show only drivers for the current user
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
