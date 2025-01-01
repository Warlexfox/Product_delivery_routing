from flask import flash
import requests
from app import app, db
from models import Drivers, Location, OptimizedRoute, Route, User
from route_optimizer import optimize_route

def get_coordinates(country, city, address):
    full_address = f"{address}, {city}, {country}"
    try:
        headers = {'User-Agent': 'YourAppName/1.0 (your_email@example.com)'}
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': full_address, 'format': 'json', 'limit': 1},
            headers=headers
        )
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            flash(f'Failed to get coordinates for address: {full_address}', 'error')
            return None, None
    except Exception as e:
        flash(f'Error getting coordinates: {e}', 'error')
        return None, None

def run_optimization(route_id, user_id):
    """
    Clears the old optimized routes for the given route,
    fetches the updated list of locations and drivers,
    calls the algorithm, and saves results in the OptimizedRoute table.
    """
    # Clear old data
    OptimizedRoute.query.filter_by(route_id=route_id).delete()
    db.session.commit()

    # Fetch deliveries (locations) for the route
    deliveries = Location.query.filter_by(route_id=route_id).all()

    # Fetch drivers for the user
    drivers = Drivers.query.filter_by(user_id=user_id).all()

    # Prepare data for the optimizer
    delivery_data = []
    for loc in deliveries:
        delivery_data.append({
            "id": loc.id,
            "country": loc.country,
            "city": loc.city,
            "address": loc.address,
            "timeframe": loc.timeframe,
        })

    driver_data = []
    for d in drivers:
        driver_data.append({
            "driver_id": d.id,
            "first_name": d.name,
            "last_name": d.surname,
            "priority": d.priority,
            "current_location": d.depot_address,
        })

    # Optimize
    optimized_list = optimize_route(driver_data, delivery_data)

    # Save results
    for assignment in optimized_list:
        new_entry = OptimizedRoute(
            route_id=route_id,
            location_id=assignment["location_id"],
            driver_id=assignment["driver_id"],
            order=assignment["order"],
            estimated_arrival=(
                assignment["estimated_arrival"].strftime('%H:%M')
                if assignment["deliverable"] and assignment["estimated_arrival"] != "cant deliver this package"
                else "cant deliver this package"
            ),
            deliverable=assignment["deliverable"]
        )
        db.session.add(new_entry)

    db.session.commit()
