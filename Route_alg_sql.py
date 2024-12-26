## "python.defaultInterpreterPath": "C:\\Users\\Janis Zageris\\AppData\\Local\\Microsoft\\WindowsApps\\python3.8.exe"

# Primitīvs maršruta organizētāja algoritms, strādā pats un spēj izveidot loģisku sarakstu balstoties uz laikiem un attālumiem
# Spēj strādāt ar vairākiem šoferiem
# Izmantoju google maps api, debug printi dod papildinformāciju par braukšanas laiku
# TODO: Vajag inputu iegūt no datubāzēm.

from datetime import datetime, timedelta
from typing import List, Tuple
import googlemaps
from models import Driver, Endpoint, SortedEndpoint, db, app

# Define the Driver and Delivery classes for internal use
class Driver:
    def __init__(self, driver_id: str, first_name: str, last_name: str, phone_number: str, current_location: str = None):
        self.driver_id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.current_location = current_location  # Initialize with current location or None for depot

    def update_location(self, new_location: str):
        self.current_location = new_location


class Delivery:
    def __init__(self, country: str, city: str, address: str, priority: int, timeframe: str):
        self.country = country
        self.city = city
        self.address = address
        self.priority = priority
        self.timeframe_start, self.timeframe_end = self._parse_timeframe(timeframe)
        self.full_address = f"{address}, {city}, {country}"

    def _parse_timeframe(self, timeframe: str) -> Tuple[datetime, datetime]:
        start, end = timeframe.split('-')
        return datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')


class RouteOptimizer:
    def __init__(self, api_key: str, depot_address: str, drivers: List[Driver]):
        self.gmaps = googlemaps.Client(key=api_key)
        self.depot_address = depot_address
        self.drivers = drivers  # List of available drivers

    def calculate_distance(self, origin: str, destination: str) -> float:
        print(f"Calculating distance from '{origin}' to '{destination}'")  # Debugging
        try:
            result = self.gmaps.distance_matrix(origin, destination, mode='driving')
            if 'origin_addresses' in result and not result['origin_addresses']:
                raise ValueError(f"Invalid origin address: {origin}")
            if result['rows'] and result['rows'][0]['elements']:
                element = result['rows'][0]['elements'][0]
                if 'distance' in element:
                    return element['distance']['value']
            print(f"Unexpected API response: {result}")
            return float('inf')  # Default high value
        except Exception as e:
            print(f"Error during API call: {e}")
            return float('inf')

    def optimize_route(self, deliveries: List[Delivery]) -> List[Tuple[Delivery, Driver]]:
        # Sort deliveries primarily by priority (highest first) and secondarily by their start time
        deliveries.sort(key=lambda x: (-x.priority, x.timeframe_start))
        optimized_route = []
        stop_time = timedelta(minutes=15)  # Assume 15 minutes per delivery
        current_time = max(deliveries[0].timeframe_start, datetime.now())

        for delivery in deliveries:
            best_driver = None
            best_distance = float('inf')

            # Compare distances for each driver
            for driver in self.drivers:
                # Use the driver's current location (if any) or the depot if the driver is not deployed yet
                driver_location = driver.current_location or self.depot_address

                # Calculate distance from driver to delivery address
                travel_distance = self.calculate_distance(driver_location, delivery.full_address)

                if travel_distance < best_distance:
                    best_distance = travel_distance
                    best_driver = driver

            if best_driver:
                # Assign the best driver to the delivery
                optimized_route.append((delivery, best_driver))
                # Update driver's location to the delivery address
                best_driver.update_location(delivery.full_address)

                # Add the delivery time and stop time to the current time
                current_time += timedelta(seconds=(best_distance / 70000) * 3600) + stop_time  # Assuming 70km/h speed

        return optimized_route


# Fetch data from the database
def fetch_data():
    with app.app_context():
        # Fetch drivers from the database
        drivers = Driver.query.all()
        driver_objects = [
            Driver(
                driver_id=str(driver.id),
                first_name=driver.name,
                last_name=driver.surname,
                phone_number=driver.phone_number,
                current_location=driver.depot_address
            )
            for driver in drivers
        ]

        # Fetch endpoints from the database
        deliveries = Endpoint.query.all()
        delivery_objects = [
            Delivery(
                country=endpoint.country,
                city=endpoint.city,
                address=endpoint.address,
                priority=endpoint.priority,
                timeframe=endpoint.delivery_time
            )
            for endpoint in deliveries
        ]

        return driver_objects, delivery_objects


# Save sorted endpoints back to the database
def save_sorted_endpoints(optimized_route, route_id):
    with app.app_context():
        for i, (delivery, driver) in enumerate(optimized_route, 1):
            sorted_endpoint = SortedEndpoint(
                route_id=route_id,
                consecutive_number=i,
                full_address=delivery.full_address,
                delivery_time=f"{delivery.timeframe_start.strftime('%H:%M')} - {delivery.timeframe_end.strftime('%H:%M')}",
                driver_id=driver.driver_id
            )
            db.session.add(sorted_endpoint)
        db.session.commit()


def main():
    # API Key and Depot Address
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004"

    # Example route ID (this can be dynamic in future implementations)
    route_id = 1

    # Fetch data from the database
    drivers, deliveries = fetch_data()

    # Optimize the route
    optimizer = RouteOptimizer(api_key, depot_address, drivers)
    optimized_route = optimizer.optimize_route(deliveries)

    # Save the optimized route back to the database
    save_sorted_endpoints(optimized_route, route_id)


if __name__ == "__main__":
    main()