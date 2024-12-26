from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import googlemaps
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Drivers, Location, Route, db

def calculate_distance(api_key: str, origin: str, destination: str) -> float:
    """Calculate driving distance using Google Maps API"""
    print(f"Calculating distance from '{origin}' to '{destination}'")
    gmaps = googlemaps.Client(key=api_key)
    try:
        result = gmaps.distance_matrix(origin, destination, mode='driving')
        if 'origin_addresses' in result and not result['origin_addresses']:
            raise ValueError(f"Invalid origin address: {origin}")
        if result['rows'] and result['rows'][0]['elements']:
            element = result['rows'][0]['elements'][0]
            if 'distance' in element:
                return element['distance']['value']
        print(f"Unexpected API response: {result}")
        return float('inf')
    except Exception as e:
        print(f"Error during API call: {e}")
        return float('inf')

def parse_timeframe(timeframe: str) -> Tuple[datetime, datetime]:
    """Parse timeframe string into start and end datetime objects"""
    start, end = timeframe.split('-')
    return datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')

def fetch_data_from_db(route_id: int):
    """Fetch drivers and locations from the database"""
    drivers = Drivers.query.all()
    driver_data = [
        {
            'driver_id': driver.id,
            'first_name': driver.name,
            'last_name': driver.surname,
            'phone_number': driver.tel_num,
            'current_location': driver.depot_address
        }
        for driver in drivers
    ]

    locations = Location.query.filter_by(route_id=route_id).all()
    delivery_data = [
        {
            'id': location.id,
            'address': location.address,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'priority': location.priority,
            'timeframe': location.timeframe,
            'route_id': location.route_id
        }
        for location in locations
    ]

    return driver_data, delivery_data

def save_optimized_route_to_db(optimized_route: List[Dict], route_id: int):
    """Save the optimized route back to the database"""
    for i, assignment in enumerate(optimized_route, 1):
        delivery = assignment['delivery']
        driver = assignment['driver']
        location = Location.query.get(delivery['id'])
        location.driver_id = driver['driver_id']
        db.session.add(location)
    db.session.commit()

def optimize_route(api_key: str, depot_address: str, drivers: List[Dict], deliveries: List[Dict]) -> List[Dict]:
    """
    Optimize delivery route based on priorities and timeframes.

    :param api_key: Google Maps API Key
    :param depot_address: Address of the depot
    :param drivers: List of drivers with current location
    :param deliveries: List of deliveries with priorities and timeframes
    :return: Optimized route as a list of assignments
    """
    # Prepare deliveries by parsing timeframe and adding a full address
    deliveries = [
        {
            **delivery,
            'timeframe_start': parse_timeframe(delivery['timeframe'])[0],
            'timeframe_end': parse_timeframe(delivery['timeframe'])[1]
        }
        for delivery in deliveries
    ]

    # Sort deliveries primarily by priority (highest first) and secondarily by their start time
    deliveries.sort(key=lambda x: (-x['priority'], x['timeframe_start']))

    optimized_route = []
    stop_time = timedelta(minutes=15)  # 15 minutes per delivery

    for delivery in deliveries:
        best_driver = None
        best_distance = float('inf')

        # Compare distances for each driver
        for driver in drivers:
            driver_location = driver['current_location'] or depot_address

            # Calculate distance from driver to delivery address
            travel_distance = calculate_distance(api_key, driver_location, delivery['address'])

            if travel_distance < best_distance:
                best_distance = travel_distance
                best_driver = driver

        if best_driver:
            # Assign the best driver to the delivery
            optimized_route.append({
                'delivery': delivery,
                'driver': best_driver
            })

            # Update driver location to the delivery address
            best_driver['current_location'] = delivery['address']

    return optimized_route

def main():
    """Main function to run the route optimization"""
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY"
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004"

    # Test route ID, PĀRMAINĪT!!!
    route_id = 1

    with db.session.app.app_context():
        # Fetch data from the database
        drivers, deliveries = fetch_data_from_db(route_id)

        # Optimize the route
        optimized_route = optimize_route(api_key, depot_address, drivers, deliveries)

        # Save the optimized route back to the database
        save_optimized_route_to_db(optimized_route, route_id)

if __name__ == "__main__":
    main()
