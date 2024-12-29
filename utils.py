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
    # Notīra esošos optimizētos maršrutus
    OptimizedRoute.query.filter_by(route_id=route_id).delete()
    db.session.commit()

    # Iegūst piegādes datus no datubāzes konkrētajam maršrutam
    deliveries = Location.query.filter_by(route_id=route_id).all()

    # Iegūst vadītājus, kas ir saistīti ar konkrēto lietotāju
    drivers = Drivers.query.filter_by(user_id=user_id).all()

    # Sagatavo datus optimizācijas funkcijai
    delivery_data = [
        {
            "country": loc.country,
            "city": loc.city,
            "address": loc.address,
            "timeframe": loc.timeframe,
        }
        for loc in deliveries
    ]

    driver_data = [
        {
            "driver_id": driver.id,
            "first_name": driver.name,
            "last_name": driver.surname,
            "priority": driver.priority,
            "current_location": driver.depot_address,
        }
        for driver in drivers
    ]

    # Izsauc optimizācijas funkciju
    optimized_route = optimize_route(driver_data, delivery_data)

    # Saglabā optimizēto maršrutu datubāzē
    for index, assignment in enumerate(optimized_route, start=1):
        new_entry = OptimizedRoute(
            route_id=route_id,
            country=assignment['delivery']['country'],
            city=assignment['delivery']['city'],
            address=assignment['delivery']['address'],
            latitude=assignment['delivery'].get('latitude'),
            longitude=assignment['delivery'].get('longitude'),
            timeframe=assignment['delivery']['timeframe'],
            driver_id=assignment['driver']['driver_id'],
            order=index,
        )
        db.session.add(new_entry)
    db.session.commit()

# TODO DELET THIS
if __name__ == "__main__":
    with app.app_context():
    # Retrieve the first existing user
        user = User.query.first()
        if not user:
            print("No user found in the database. Please ensure there is at least one user.")
            exit()

        # Retrieve the first route associated with the user
        route = Route.query.filter_by(user_id=user.id).first()
        if not route:
            print(f"No route found for user {user.id}. Please ensure the user has at least one route.")
            exit()

        # Print details for debugging
        print(f"Using existing user: {user.id} - {user.email}")
        print(f"Using existing route: {route.id} - {route.name}")

        # Check if there are locations for this route
        locations = Location.query.filter_by(route_id=route.id).all()
        if not locations:
            print(f"No locations found for route {route.id}. Please ensure the route has associated locations.")
            exit()

        print(f"Found {len(locations)} locations for route {route.id}.")

        # Run the optimization function
        print(f"Running optimization for route_id={route.id} and user_id={user.id}")
        run_optimization(route.id, user.id)
        optimizedRout = OptimizedRoute.query.filter_by(route_id=route.id).all()
        for i in optimizedRout:
            print(i)

        print("Optimization completed successfully.")