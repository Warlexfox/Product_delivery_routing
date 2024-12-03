# Primitīvs maršruta organizētāja algoritms, strādā pats un spēj izveidot loģisku sarakstu balstoties uz laikiem un attālumiem
# Spēj strādāt ar vairākiem šoferiem
# Izmantoju google maps api, debug printi dod papildinformāciju par braukšanas laiku
# TODO: Vajag inputu iegūt no datubāzēm.

from datetime import datetime, timedelta
from typing import List, Tuple
import googlemaps

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
            best_driver_index = -1

            # Compare distances for each driver
            for i, driver in enumerate(self.drivers):
                # Use the driver's current location (if any) or the depot if the driver is not deployed yet
                driver_location = driver.current_location or self.depot_address
                
                # Calculate distance from driver to delivery address
                travel_distance = self.calculate_distance(driver_location, delivery.full_address)
                
                if travel_distance < best_distance:
                    best_distance = travel_distance
                    best_driver = driver
                    best_driver_index = i
            
            if best_driver:
                # Assign the best driver to the delivery
                optimized_route.append((delivery, best_driver))
                # Update driver's location to the delivery address
                best_driver.update_location(delivery.full_address)

                # Add the delivery time and stop time to the current time
                current_time += timedelta(seconds=(best_distance / 70000) * 3600) + stop_time  # Assuming 70km/h speed

        return optimized_route



def main():
    # Piemērs
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY" # Mans google maps API key, lūdzu neaiztikt
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004" # Noliktavas/sākumadrese

    # Piegādes šoferi (ID, vārds, uzvārds, tel. nr., depot_address)
    drivers = [
        Driver("1001", "Artjoms", "Šefanovskis", "22222222", depot_address),
        Driver("1002", "Niklāvs", "Zebinskis", "22222223", depot_address)
    ]
    
    # Piegādāšanas vieta, prioritāte un piegādājamies laiks
    deliveries = [
        Delivery("Latvia", "Riga", "Brīvības iela 100", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Tērbatas iela 50", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Krišjāņa Valdemāra iela 75", 1, "09:00-10:00"),
        Delivery("Latvia", "Liepaja", "Rīgas iela 1", 1, "19:00-20:00"),
        Delivery("Latvia", "Sigula", "Rīgas iela 1", 1, "16:00-18:00")
    ]
    
    optimizer = RouteOptimizer(api_key, depot_address, drivers)
    optimized_route = optimizer.optimize_route(deliveries)

    # Sarakstu printētājs
    for i, (delivery, drivers) in enumerate(optimized_route, 1):
        print(f"Stop {i}:")
        print(f"Address: {delivery.full_address}")
        print(f"Time window: {delivery.timeframe_start.strftime('%H:%M')} - {delivery.timeframe_end.strftime('%H:%M')}")
        print(f"Priority: {delivery.priority}")
        print(f"Driver: (ID: {drivers.driver_id})")
        print("---")

if __name__ == "__main__":
    main()
