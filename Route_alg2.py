# Primitīvs maršruta organizētāja algoritms, strādā pats un spēj izveidot loģisku sarakstu balstoties uz laikiem un attālumiem
# Spēj strādāt ar vairākiem šoferiem
# Izmantoju google maps api, debug printi dod papildinformāciju par braukšanas laiku
# Bez klasēm!!!
# TODO: Vajag inputu iegūt no datubāzēm.

from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import googlemaps

AVERAGE_SPEED_KMH = 70 # Vidējais braukšanas ātrums km/h

def calculate_travel_time(distance_meters: float) -> timedelta:
    """Calculate travel time given the distance in meters and average speed."""
    distance_km = distance_meters / 1000  # No metriem uz kilometriem
    travel_hours = distance_km / AVERAGE_SPEED_KMH
    return timedelta(hours=travel_hours)

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

def optimize_route(api_key: str, depot_address: str, drivers: List[Dict], deliveries: List[Dict]) -> List[Dict]:
    """
    Optimize delivery route based on driver priorities and timeframes.

    :param api_key: Google Maps API Key
    :param depot_address: Address of the depot
    :param drivers: List of drivers with current location and priority
    :param deliveries: List of deliveries with timeframes
    :return: Optimized route as a list of assignments
    """
    # Prepare deliveries by parsing timeframe and adding a full address
    deliveries = [
        {
            **delivery,
            'timeframe_start': parse_timeframe(delivery['timeframe'])[0],
            'timeframe_end': parse_timeframe(delivery['timeframe'])[1],
            'full_address': f"{delivery['address']}, {delivery['city']}, {delivery['country']}"
        }
        for delivery in deliveries
    ]

    # Sort deliveries by their start time (earliest deliveries first)
    deliveries.sort(key=lambda x: x['timeframe_start'])

    # Sort drivers by their priority (lowest number has highest priority)
    drivers.sort(key=lambda x: x['priority'])

    optimized_route = []
    stop_time = timedelta(minutes=15)  # 15 minūtes katrā piegādes punktā

    for delivery in deliveries:
        best_driver = None
        best_distance = float('inf')

        # Assign drivers based on priority
        for driver in drivers:
            driver_location = driver['current_location'] or depot_address

            # Calculate distance from driver to delivery address
            travel_distance = calculate_distance(api_key, driver_location, delivery['full_address'])

            if travel_distance < best_distance:
                best_distance = travel_distance
                best_driver = driver

        if best_driver:
            # Assign the best driver to the delivery
            optimized_route.append({
                'delivery': delivery,
                'driver': best_driver
            })

            # Update driver's location to the delivery address
            best_driver['current_location'] = delivery['full_address']

    return optimized_route

def main():
    """Main function to run the route optimization"""
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY"
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004"

    # Test data
    drivers = [
        {'driver_id': '1001', 'first_name': 'Artjoms', 'last_name': 'Šefanovskis', 'phone_number': '12345678', 'current_location': None, 'priority': 1},
        {'driver_id': '1002', 'first_name': 'Niklāvs', 'last_name': 'Zebinskis', 'phone_number': '87654321', 'current_location': None, 'priority': 2},
        {'driver_id': '1003', 'first_name': 'Sergejs', 'last_name': 'Zembkovskis', 'phone_number': '22222222', 'current_location': None, 'priority': 3}
    ]

    deliveries = [
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Brivibas iela 1', 'timeframe': '09:00-12:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Daugavgrivas iela 2', 'timeframe': '10:00-14:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Tērbatas iela 50', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Krišjāņa Valdemāra iela 75', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Liepaja', 'address': 'Rīgas iela 1', 'timeframe': '19:00-20:00'},
        {'country': 'Latvia', 'city': 'Sigulda', 'address': 'Rīgas iela 1', 'timeframe': '16:00-18:00'}
    ]

    # Optimize the route
    optimized_route = optimize_route(api_key, depot_address, drivers, deliveries)

    # Print the optimized route
    print("Optimized Delivery Route:\n")
    for i, assignment in enumerate(optimized_route, 1):
        delivery = assignment['delivery']
        driver = assignment['driver']
        driver_location = driver['current_location'] or depot_address

        # Calculate the travel distance and estimated arrival time
        travel_distance = calculate_distance(api_key, driver_location, delivery['full_address'])
        travel_time = calculate_travel_time(travel_distance)

        # Estimated arrival time
        estimated_arrival = delivery['timeframe_start'] - travel_time

        print(f"Stop {i}:")
        print(f"Address: {delivery['full_address']}")
        print(f"Time window: {delivery['timeframe_start'].strftime('%H:%M')} - {delivery['timeframe_end'].strftime('%H:%M')}")
        print(f"Driver: {driver['first_name']} {driver['last_name']} (ID: {driver['driver_id']})")
        print(f"Estimated Arrival: {estimated_arrival.strftime('%H:%M')}")
        print("---")

if __name__ == "__main__":
    main()
