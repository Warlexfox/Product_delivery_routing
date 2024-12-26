# Primitīvs maršruta organizētāja algoritms, strādā pats un spēj izveidot loģisku sarakstu balstoties uz laikiem un attālumiem
# Spēj strādāt ar vairākiem šoferiem
# Izmantoju google maps api, debug printi dod papildinformāciju par braukšanas laiku
# Bez klasēm!!!
# TODO: Vajag inputu iegūt no datubāzēm.

from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import googlemaps

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
            'timeframe_end': parse_timeframe(delivery['timeframe'])[1],
            'full_address': f"{delivery['address']}, {delivery['city']}, {delivery['country']}"
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

            # Update driver location to the delivery address
            best_driver['current_location'] = delivery['full_address']

    return optimized_route

def main():
    """Main function to run the route optimization"""
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY"
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004"

    # Test data
    drivers = [
        {'driver_id': '1', 'first_name': 'John', 'last_name': 'Doe', 'phone_number': '12345678', 'current_location': None},
        {'driver_id': '2', 'first_name': 'Jane', 'last_name': 'Smith', 'phone_number': '87654321', 'current_location': None}
    ]

    deliveries = [
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Brivibas iela 1', 'priority': 1, 'timeframe': '09:00-12:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Daugavgrivas iela 2', 'priority': 2, 'timeframe': '10:00-14:00'}
    ]

    # Optimize the route
    optimized_route = optimize_route(api_key, depot_address, drivers, deliveries)

    # Output the optimized route
    for assignment in optimized_route:
        delivery = assignment['delivery']
        driver = assignment['driver']
        print(f"Driver {driver['first_name']} {driver['last_name']} assigned to deliver to {delivery['full_address']}.")

if __name__ == "__main__":
    main()
