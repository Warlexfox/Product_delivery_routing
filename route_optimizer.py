# TODO
# 1. pirms funkcija jebko atgriež, izņemt vias piegādes atsevišķā sarakstā, kur viņi būtu sagrupēti kopā pēc vadītājiem, tad apvienot un izlabot kārtas numurus 
# 2. salabot lai strādātu "gaidāmais ierašanās laiks"
# 3. uztaisīt loģiku, lai nepārslogotu vadītājus, piemēram visi vadītāji var strādāt ne ilgāk kā 8 stundas
# 4. Visi vadītāji uzsāk savu maiņu plsk 9:00, viņu maiņa beidzas ne vēlāk kā pēc plsk 18:00, NEņemt vērā to, ka šoferim ir jāatgriežas uz depo
# 5. Ja pietrūkst vadītāju, lai piegādātu kādu paciņu, tad pie vadītāja ielikt null un pie gaidāmā piegādes laika ierakstīt "cant deliver this package" un attribūts deliverable ir false

from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import googlemaps

AVERAGE_SPEED_KMH = 70 # Vidējais braukšanas ātrums km/h

def calculate_travel_time(distance_meters: float) -> timedelta: # Aprēķina braukšanas laiku
    """Calculate travel time given the distance in meters and average speed."""
    distance_km = distance_meters / 1000  # Pārvērš no metriem uz kilometriem
    travel_hours = distance_km / AVERAGE_SPEED_KMH
    return timedelta(hours=travel_hours)

def calculate_distance(origin: str, destination: str) -> float: # Aprēķina attālumu
    """Calculate driving distance using Google Maps API"""
    # print(f"Calculating distance from '{origin}' to '{destination}'")
    gmaps = googlemaps.Client(key="AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY") # google maps api
    try: # Pārbauda vai ir kļūda
        result = gmaps.distance_matrix(origin, destination, mode='driving')
        if 'origin_addresses' in result and not result['origin_addresses']:
            raise ValueError(f"Invalid origin address: {origin}")
        if result['rows'] and result['rows'][0]['elements']:
            element = result['rows'][0]['elements'][0]
            if 'distance' in element: # Pārbauda vai ir attālums
                return element['distance']['value']
        print(f"Unexpected API response: {result}") 
        return float('inf')
    except Exception as e: # Ja ir kļūda, tad atgriež bezgalību
        print(f"Error during API call: {e}")
        return float('inf')

def parse_timeframe(timeframe: str) -> Tuple[datetime, datetime]: # Izveido laika rādītāju
    """Parse timeframe string into start and end datetime objects"""
    start, end = timeframe.split('-')
    return datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')

def optimize_route(drivers: List[Dict], deliveries: List[Dict]) -> List[Dict]: # Optimizē maršrutu
    """
    Optimize delivery route based on driver priorities and timeframes, 
    while ensuring no driver works more than 8 hours and handling cases
    where no drivers are available.
    """
    deliveries = [ 
        {
            **delivery,
            'timeframe_start': parse_timeframe(delivery['timeframe'])[0],
            'timeframe_end': parse_timeframe(delivery['timeframe'])[1],
            'full_address': f"{delivery['address']}, {delivery['city']}, {delivery['country']}"
        }
        for delivery in deliveries
    ]

    # Sortē piegādes pēc to sākuma laika (sāk ar agrākajām piegādēm)
    deliveries.sort(key=lambda x: x['timeframe_start'])

    # Sortē šoferus pēc prioritātes (augošā secībā)
    for driver in drivers:
        driver['total_working_time'] = timedelta()  # Initialize working time

    optimized_route = []
    stop_time = timedelta(minutes=15)  # Pavada 15 minūtes piegādes laikā
    max_working_time = timedelta(hours=8)  # Maksimālais darba laiks
    shift_start = datetime.strptime("09:00", "%H:%M")
    shift_end = datetime.strptime("18:00", "%H:%M")

    for delivery in deliveries:
        best_driver = None
        best_distance = float('inf')

        for driver in drivers:
            # Aprēķina attālumu no vadītāja līdz piegādes adresei
            travel_distance = calculate_distance(driver['current_location'], delivery['full_address'])
            travel_time = calculate_travel_time(travel_distance)

            # Paredzamais laiks, ieskaitot apstāšanās laiku
            projected_working_time = driver['total_working_time'] + travel_time + stop_time

            # Izvēlas tikai tos šoferus, kuriem darba laiks nepārsniedz limitu un ir maiņas ietvaros
            if (
                projected_working_time <= max_working_time and
                delivery['timeframe_start'] >= shift_start and
                delivery['timeframe_end'] <= shift_end and
                travel_distance < best_distance
            ):
                best_driver = driver
                best_distance = travel_distance

        # Ja visi šoferi pārsniedz darba laiku vai nav pieejami, piešķir "neizpildāms"
        if not best_driver:
            optimized_route.append({
                "country": delivery['country'],
                "city": delivery['city'],
                "address": delivery['address'],
                "latitude": delivery.get('latitude'),
                "longitude": delivery.get('longitude'),
                "timeframe": delivery['timeframe'],
                "timeframe_start": delivery['timeframe_start'],
                "timeframe_end": delivery['timeframe_end'],
                "driver": None,
                "order": len(optimized_route) + 1,
                'estimated_arrival': "cant deliver this package",
                "deliverable": False
            })
            continue

        # Aprēķina ceļojuma attālumu un braukšanas laiku
        travel_distance = calculate_distance(best_driver['current_location'], delivery['full_address'])
        travel_time = calculate_travel_time(travel_distance)

        # Aprēķina ierašanās laiku
        arrival_time = delivery['timeframe_start'] - travel_time
        if arrival_time < delivery['timeframe_start']:
            estimated_arrival = delivery['timeframe_start']
        else:
            estimated_arrival = arrival_time

        # Atjauno vadītāja atrašanās vietu un darba laiku
        best_driver['current_location'] = delivery['full_address']
        best_driver['total_working_time'] += travel_time + stop_time

        # Pievieno piegādi uz optimizēto maršrutu
        optimized_route.append({
            "country": delivery['country'],
            "city": delivery['city'],
            "address": delivery['address'],
            "latitude": delivery.get('latitude'),
            "longitude": delivery.get('longitude'),
            "timeframe": delivery['timeframe'],
            "timeframe_start": delivery['timeframe_start'],
            "timeframe_end": delivery['timeframe_end'],
            "driver": best_driver,
            "order": len(optimized_route) + 1,
            'estimated_arrival': estimated_arrival,
            "deliverable": True
        })

    # Grupē piegādes pēc šoferiem
    grouped_deliveries = {}
    for route in optimized_route:
        driver = route['driver']
        driver_id = driver['driver_id'] if driver else "unassigned"
        if driver_id not in grouped_deliveries:
            grouped_deliveries[driver_id] = []
        grouped_deliveries[driver_id].append(route)

    # Apvieno grupas un atjauno secības numurus
    merged_routes = []
    sequence_number = 1
    for driver_id, routes in grouped_deliveries.items():
        for route in routes:
            route['order'] = sequence_number
            merged_routes.append(route)
            sequence_number += 1

    optimized_route = merged_routes
    return optimized_route

def main():
    # Test data
    drivers = [
        {'driver_id': '1001', 'first_name': 'Artjoms', 'last_name': 'Šefanovskis', 'phone_number': '12345678', 'current_location':"Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 1},
        {'driver_id': '1002', 'first_name': 'Niklāvs', 'last_name': 'Zebinskis', 'phone_number': '87654321', 'current_location':"Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 2},
        {'driver_id': '1003', 'first_name': 'Sergejs', 'last_name': 'Zembkovskis', 'phone_number': '22222222', 'current_location':"Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 3}
    ]

    deliveries = [
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Brivibas iela 1', 'timeframe': '09:00-12:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Daugavgrivas iela 2', 'timeframe': '10:00-14:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Tērbatas iela 50', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Krišjāņa Valdemāra iela 75', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Liepaja', 'address': 'Rīgas iela 1', 'timeframe': '15:00-20:00'},
        {'country': 'Latvia', 'city': 'Sigulda', 'address': 'Rīgas iela 1', 'timeframe': '16:00-18:00'}
    ]

    # Optimizē maršrutu
    optimized_route = optimize_route(drivers, deliveries)
    
    # Izprintē optimizēto maršrutu
    print("Optimized Delivery Route:\n")
    for i, assignment in enumerate(optimized_route, 1): # Rekursīvā funkcija, kas izprintētē maršrutu
        country = assignment['country']
        city = assignment['city']
        address = assignment['address']
        timeframe_start = assignment['timeframe_start']
        timeframe_end = assignment['timeframe_end']
        driver = assignment['driver']
        estimated_arrival = assignment['estimated_arrival']

        print("*****")
        print(f"Stop {i}:")
        print(f"Address: {country}, {city}, {address}")
        print(f"Time window: {timeframe_start.strftime('%H:%M')} - {timeframe_end.strftime('%H:%M')}")
        print(f"Driver: {driver['first_name']} {driver['last_name']} (ID: {driver['driver_id']})")
        print(f"Estimated Arrival: {estimated_arrival.strftime('%H:%M')}")
        print("---")

if __name__ == "__main__":
    main()
