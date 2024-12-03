# Primitīvs maršruta organizētāja algoritms, strādā pats un spēj izveidot loģisku sarakstu balstoties uz laikiem un attālumiem
# Pagaidām strādā tikai ar vienu šoferi
# Izmantoju google maps api, debug printi dod papildinformāciju par braukšanas laiku

from datetime import datetime
from datetime import timedelta
from typing import List, Tuple
import googlemaps

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
    def __init__(self, api_key: str, depot_address: str):
        self.gmaps = googlemaps.Client(key=api_key)
        self.depot_address = depot_address
        
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

    
    def optimize_route(self, deliveries: List[Delivery]) -> List[Delivery]:
        # Sort deliveries primarily by priority (highest first) and secondarily by their start time
        deliveries.sort(key=lambda x: (-x.priority, x.timeframe_start))
        optimized_route = []
        current_location = self.depot_address

        stop_time = timedelta(minutes=15)  # Assume 15 minutes per delivery

        # Start time is the earliest of the first delivery's timeframe start or the workday start
        current_time = max(deliveries[0].timeframe_start, datetime.now())

        while deliveries:
            best_next_delivery = None
            best_distance = float('inf')
            best_index = -1

            for i, delivery in enumerate(deliveries):
                # Calculate travel distance and time
                travel_distance = self.calculate_distance(current_location, delivery.full_address)
                travel_time = timedelta(seconds=(travel_distance / 50000) * 3600)  # Speed: 50km/h
                arrival_time = current_time + travel_time

                # Debug logs
                print(f"Checking delivery: {delivery.full_address}")
                print(f"Arrival Time: {arrival_time.strftime('%H:%M')}, Timeframe: {delivery.timeframe_start.strftime('%H:%M')} - {delivery.timeframe_end.strftime('%H:%M')}")
                print(f"Travel Time: {travel_time}, Stop Time: {stop_time}")

                # Prioritize deliveries based on the smallest travel distance and the least deviation from the target time window
                if travel_distance < best_distance:
                    best_distance = travel_distance
                    best_next_delivery = delivery
                    best_index = i

            if best_next_delivery:
                # Add delivery to route
                optimized_route.append(best_next_delivery)
                current_location = best_next_delivery.full_address
                current_time += travel_time + stop_time  # Add travel time and stop time

                # Remove processed delivery from list
                deliveries.pop(best_index)
            else:
                print("No valid next delivery found.")
                break

        return optimized_route





def main():
    # Piemērs
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY" # Mans google maps API key, lūdzu neaiztikt
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004" # Noliktavas/sākumadrese
    optimizer = RouteOptimizer(api_key, depot_address) # Ievada informāciju optimizātorā

    # Piegādāšanas vieta, prioritāte un piegādājamies laiks
    deliveries = [
        Delivery("Latvia", "Riga", "Brīvības iela 100", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Tērbatas iela 50", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Krišjāņa Valdemāra iela 75", 1, "09:00-10:00"),
        Delivery("Latvia", "Liepaja", "Rīgas iela 1", 1, "19:00-20:00"),
        Delivery("Latvia", "Sigula", "Rīgas iela 1", 1, "16:00-18:00")
    ]
    
    optimized_route = optimizer.optimize_route(deliveries)

    # Sarakstu printētājs
    for i, delivery in enumerate(optimized_route, 1):
        print(f"Stop {i}:")
        print(f"Address: {delivery.full_address}")
        print(f"Time window: {delivery.timeframe_start.strftime('%H:%M')}-{delivery.timeframe_end.strftime('%H:%M')}")
        print(f"Priority: {delivery.priority}")
        print("---")

if __name__ == "__main__":
    main()
