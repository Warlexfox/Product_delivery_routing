# TODO
# 1. pirms funkcija jebko atgriež, izņemt vias piegādes atsevišķā sarakstā, kur viņi būtu sagrupēti kopā pēc vadītājiem, tad apvienot un izlabot kārtas numurus 
# 2. salabot lai strādātu "gaidāmais ierašanās laiks"
# 3. uztaisīt loģiku, lai nepārslogotu vadītājus, piemēram visi vadītāji var strādāt ne ilgāk kā 8 stundas
# 4. Visi vadītāji uzsāk savu maiņu plsk 9:00, viņu maiņa beidzas ne vēlāk kā pēc plsk 18:00, NEņemt vērā to, ka šoferim ir jāatgriežas uz depo
# 5. Ja pietrūkst vadītāju, lai piegādātu kādu paciņu, tad pie vadītāja ielikt null un pie gaidāmā piegādes laika ierakstīt "cant deliver this package" un attribūts deliverable ir false

from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import random
import googlemaps

AVERAGE_SPEED_KMH = 70  # Average driving speed in km/h

# Aprēķina braukšanas laiku
def calculate_travel_time(distance_meters: float) -> timedelta:
    """Calculate travel time given the distance in meters and average speed."""
    distance_km = distance_meters / 1000  # Convert from meters to kilometers
    travel_hours = distance_km / AVERAGE_SPEED_KMH
    return timedelta(hours=travel_hours)

# Aprēķina attālumu
def calculate_distance(origin: str, destination: str) -> float:
    """Calculate driving distance using Google Maps API"""
    gmaps = googlemaps.Client(key="AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY")
    try:
        result = gmaps.distance_matrix(origin, destination, mode='driving')
        if result['rows'] and result['rows'][0]['elements']:
            element = result['rows'][0]['elements'][0]
            if 'distance' in element and element['status'] == 'OK':
                return element['distance']['value']
        print(f"Unexpected API response: {result}")
        return float('inf')
    except Exception as e:
        print(f"Error during API call: {e}")
        return float('inf')
        
# Izveido laika rādītāju
def parse_timeframe(timeframe: str) -> Tuple[datetime, datetime]:
    """Parse timeframe string into start and end datetime objects"""
    start, end = timeframe.split('-')
    return datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')

# Heiristiskā vērtība veiksmīgu piegāžu skaitīšanai
def evaluate_route(route: List[Dict]) -> float:
    """Evaluate the efficiency of a route based on successful deliveries."""
    success_count = sum(1 for delivery in route if delivery["deliverable"])
    return success_count

def optimize_route(drivers: List[Dict], deliveries: List[Dict], iterations: int = 10) -> List[Dict]:
    """
    Optimizē piegādes maršrutu, izmantojot randomizētu ievades pasūtīšanu un novērtēšanu.
    Iterāciju skaits nosakas cik reizes algoritms veiks pārbaudi, mainot ievada datu secību pēc nejaušības principa.
    Iterāciju skaitu var mainīt, pašlaik tas ir 10.
    Vairāk iterācijas nozīmē lielāku gaidīšanas laiku, bet palielina iespēju iegūt labāku rezultātu.
    """
    best_route = []
    best_score = -1

    # Iterēt pēc nejaušības principa
    for i in range(iterations):
        shuffled_deliveries = deliveries.copy()
        
        if i == 0: # Pirmajā iterācijā izmanto sākotnējo secību.
            shuffled_deliveries = deliveries.copy()
        if i == 1: # Otrajā iterācijā izmanto sākotnējo secību, kas ir sakārtota pēc laika augošā secībā.
            shuffled_deliveries.sort(key=lambda x: parse_timeframe(x['timeframe'])[0])
        else: # Pārējās iterācijās izmanto nejaušo secību, kas ir sakārtota pēc laika augošā secībā.
            random.shuffle(shuffled_deliveries)
            shuffled_deliveries.sort(key=lambda x: parse_timeframe(x['timeframe'])[0])
        
        current_route = optimize_single_route(drivers, shuffled_deliveries)
        current_score = evaluate_route(current_route)

    # Atjaunināt labāko maršrutu, ja ir labāks rezultāts
        if current_score > best_score:
            best_score = current_score
            best_route = current_route

    # Atgriež labāko maršrutu
    return best_route

def optimize_single_route(drivers: List[Dict], deliveries: List[Dict]) -> List[Dict]:
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

    deliveries.sort(key=lambda x: x['timeframe_start']) # Sākotnēji sakārto piegādes pēc laika.

    for driver in drivers:
        driver['total_working_time'] = timedelta()  # Inicializē kopējo darba laiku.

    optimized_route = []

    stop_time = timedelta(minutes=15)  # 15 minūtes starp piegādēm.
    max_working_time = timedelta(hours=8)  # Maksimālais darba laiks (8 stundas).
    shift_start = datetime.strptime("09:00", "%H:%M") # Darba sākuma laiks.
    shift_end = datetime.strptime("18:00", "%H:%M") # Darba beigu laiks.

    for delivery in deliveries:
        best_driver = None
        best_distance = float('inf')
        best_arrival_time = None

        for driver in drivers:
            travel_distance = calculate_distance(driver['current_location'], delivery['full_address'])
            travel_time = calculate_travel_time(travel_distance)

            arrival_time = max(
                delivery['timeframe_start'],
                shift_start + driver['total_working_time'] + travel_time + stop_time
            )

            projected_working_time = driver['total_working_time'] + travel_time + stop_time

            if (
                projected_working_time <= max_working_time and
                arrival_time <= delivery['timeframe_end'] and
                delivery['timeframe_start'] >= shift_start and
                delivery['timeframe_end'] <= shift_end and
                travel_distance < best_distance
            ):
                best_driver = driver
                best_distance = travel_distance
                best_arrival_time = arrival_time

         # Ja nav pieejams neviens šoferis, tad piegādi nevar veikt.
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
                "driver_id": None,
                "order": len(optimized_route) + 1,
                "location_id": delivery['id'],
                'estimated_arrival': "cant deliver this package",
                "deliverable": False
            })
            continue

        best_driver['current_location'] = delivery['full_address'] # Atjaunina šoferu darba laiku un atrašanās vietu
        best_driver['total_working_time'] = best_arrival_time - shift_start + stop_time # Atjaunina šoferu kopējo darba laiku

        # Pievieno piegādi maršrutam
        optimized_route.append({
            "country": delivery['country'],
            "city": delivery['city'],
            "address": delivery['address'],
            "latitude": delivery.get('latitude'),
            "longitude": delivery.get('longitude'),
            "timeframe": delivery['timeframe'],
            "timeframe_start": delivery['timeframe_start'],
            "timeframe_end": delivery['timeframe_end'],
            "driver_id": best_driver["driver_id"],
            "location_id": delivery['id'],
            "order": len(optimized_route) + 1,
            'estimated_arrival': best_arrival_time,
            "deliverable": True
        })

    # Grupē piegādes pēc šoferiem,
    grouped_deliveries = {}
    for route in optimized_route:
        driver_id = driver['driver_id'] if driver else "unassigned"
        if driver_id not in grouped_deliveries:
            grouped_deliveries[driver_id] = []
        grouped_deliveries[driver_id].append(route)

    # Sakārto šoferus pēc to ID augošā secībā.
    sorted_driver_ids = sorted(grouped_deliveries.keys(), key=lambda x: int(x) if x != "unassigned" else float('inf'))

    # Apvieno grupas un atjauno secības numurus
    merged_routes = []
    sequence_number = 1
    for driver_id in sorted_driver_ids:
        routes = grouped_deliveries[driver_id]
        sorted_routes = sorted(routes, key=lambda x: x['timeframe_start'])
        for route in sorted_routes:
            route['order'] = sequence_number
            merged_routes.append(route)
            sequence_number += 1

    optimized_route = merged_routes
    return optimized_route

def main():
    # Test data
    drivers = [
        {'driver_id': '1001', 'first_name': 'Artjoms', 'last_name': 'Šefanovskis', 'phone_number': '12345678', 'current_location': "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 1},
        {'driver_id': '1002', 'first_name': 'Niklāvs', 'last_name': 'Zebinskis', 'phone_number': '87654321', 'current_location': "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 2},
        {'driver_id': '1003', 'first_name': 'Sergejs', 'last_name': 'Zembkovskis', 'phone_number': '22222222', 'current_location': "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004", 'priority': 3}
    ]

    deliveries = [
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Brīvības iela 10', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Daugavgrīvas iela 15', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Tērbatas iela 33', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Kr.Valdemāra iela 12', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Ģertrūdes iela 23', 'timeframe': '13:00-14:00'},
        {'country': 'Latvia', 'city': 'Riga', 'address': 'Maskavas iela 260', 'timeframe': '14:00-15:00'},
        {'country': 'Latvia', 'city': 'Liepaja', 'address': 'Ganību iela 21', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Liepaja', 'address': 'Zivju iela 12', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Daugavpils', 'address': 'Rīgas iela 10', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Daugavpils', 'address': 'Cietokšņa iela 1', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Ventspils', 'address': 'Lielais prospekts 35', 'timeframe': '14:00-15:00'},
        {'country': 'Latvia', 'city': 'Ventspils', 'address': 'Tirgus iela 5', 'timeframe': '15:00-16:00'},
        {'country': 'Latvia', 'city': 'Valmiera', 'address': 'Rīgas iela 20', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Valmiera', 'address': 'Bastiona iela 8', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Sigulda', 'address': 'Pils iela 16', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Sigulda', 'address': 'Dārza iela 9', 'timeframe': '13:00-14:00'},
        {'country': 'Latvia', 'city': 'Jelgava', 'address': 'Raiņa iela 7', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Jelgava', 'address': 'Lielā iela 15', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Ogre', 'address': 'Brīvības iela 2', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Ogre', 'address': 'Tīnūžu iela 14', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Cēsis', 'address': 'Rīgas iela 18', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Cēsis', 'address': 'Vienības laukums 1', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Jēkabpils', 'address': 'Madonas iela 5', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Jēkabpils', 'address': 'Kurzemes iela 9', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Saldus', 'address': 'Rīgas iela 2', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Saldus', 'address': 'Kalna iela 7', 'timeframe': '13:00-14:00'},
        {'country': 'Latvia', 'city': 'Dobele', 'address': 'Bērzes iela 8', 'timeframe': '14:00-15:00'},
        {'country': 'Latvia', 'city': 'Dobele', 'address': 'Tirgoņu iela 10', 'timeframe': '15:00-16:00'},
        {'country': 'Latvia', 'city': 'Rēzekne', 'address': 'Atbrīvošanas aleja 93', 'timeframe': '09:00-10:00'},
        {'country': 'Latvia', 'city': 'Rēzekne', 'address': 'Latgales iela 15', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Kuldīga', 'address': 'Baznīcas iela 9', 'timeframe': '11:00-12:00'},
        {'country': 'Latvia', 'city': 'Kuldīga', 'address': 'Kalna iela 5', 'timeframe': '12:00-13:00'},
        {'country': 'Latvia', 'city': 'Talsi', 'address': 'Kroņu iela 4', 'timeframe': '10:00-11:00'},
        {'country': 'Latvia', 'city': 'Talsi', 'address': 'Saules iela 12', 'timeframe': '11:00-12:00'}
    ]

    optimized_route = optimize_route(drivers, deliveries, iterations=10)

    
    # Izprintē optimizēto maršrutu
    print("Optimized Delivery Route:\n")
    for i, assignment in enumerate(optimized_route, 1):  # Rekursīvā funkcija, kas izprintētē maršrutu
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
        if driver:
            print(f"Driver: {driver['first_name']} {driver['last_name']} (ID: {driver['driver_id']})")
        else:
            print("Driver: Not assigned")
        if isinstance(estimated_arrival, datetime):
            print(f"Estimated Arrival: {estimated_arrival.strftime('%H:%M')}")
        else:
            print(f"Estimated Arrival: {estimated_arrival}")
        print("---")

if __name__ == "__main__":
    main()
