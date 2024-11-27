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
        # Sort deliveries by timeframe_start and priority
        deliveries.sort(key=lambda x: (x.timeframe_start, -x.priority))
        optimized_route = []
        current_location = self.depot_address

        # Define working hours (e.g., 08:00 to 18:00)
        working_start_time = datetime.strptime("08:00", "%H:%M").time()
        working_end_time = datetime.strptime("18:00", "%H:%M").time()
        stop_time = timedelta(minutes=15)  # Assume 15 minutes per delivery

        # Set initial current_time to the later of the working start time or the first delivery's start time
        current_time = max(
            datetime.combine(deliveries[0].timeframe_start.date(), working_start_time),
            deliveries[0].timeframe_start
        )

        while deliveries:
            best_next_delivery = None
            best_distance = float('inf')
            best_index = -1

            for i, delivery in enumerate(deliveries):
                # Calculate travel distance and time
                travel_distance = self.calculate_distance(current_location, delivery.full_address)
                travel_time = timedelta(seconds=(travel_distance / 50000) * 3600)  # Speed: 50km/h
                arrival_time = current_time + travel_time

                # Add debug log to show the current state
                print(f"Checking delivery: {delivery.full_address}")
                print(f"Arrival Time: {arrival_time.strftime('%H:%M')}, Timeframe: {delivery.timeframe_start.strftime('%H:%M')} - {delivery.timeframe_end.strftime('%H:%M')}")
                print(f"Travel Time: {travel_time}, Stop Time: {stop_time}")

                # Ensure the arrival time is within working hours
                if arrival_time.time() > working_end_time:
                    print(f"Arrival exceeds working hours for {delivery.full_address}.")
                    continue  # Skip if beyond working hours

                # Check if this delivery can be reached within its time window
                if delivery.timeframe_start <= arrival_time <= delivery.timeframe_end:
                    # Prioritize closer deliveries
                    if travel_distance < best_distance:
                        best_distance = travel_distance
                        best_next_delivery = delivery
                        best_index = i

            if best_next_delivery:
                # Update route, location, and current time
                optimized_route.append(best_next_delivery)
                current_location = best_next_delivery.full_address
                current_time += travel_time + stop_time  # Add travel time and stop time

                # Remove the completed delivery
                deliveries.pop(best_index)

                # Check if current time exceeds working hours
                if current_time.time() > working_end_time:
                    print("End of working day. Returning to depot.")
                    current_time = datetime.combine(current_time.date() + timedelta(days=1), working_start_time)
                    current_location = self.depot_address  # Reset to depot
            else:
                # If no valid delivery can be found, exit the loop
                print("No valid next delivery found within time windows.")
                break

        return optimized_route





def main():
    # Example usage
    api_key = "AIzaSyBMIUvpEMX0yupxfDxyhjM3qQM0eSTwXHY"
    depot_address = "Lucavsalas iela 3, Zemgales priekšpilsēta, Rīga, LV-1004"
    optimizer = RouteOptimizer(api_key, depot_address)  # Pass both arguments
    
    deliveries = [
        Delivery("Latvia", "Riga", "Brīvības iela 100", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Tērbatas iela 50", 1, "09:00-10:00"),
        Delivery("Latvia", "Riga", "Krišjāņa Valdemāra iela 75", 1, "09:00-10:00")
    ]
    
    optimized_route = optimizer.optimize_route(deliveries)
    
    for i, delivery in enumerate(optimized_route, 1):
        print(f"Stop {i}:")
        print(f"Address: {delivery.full_address}")
        print(f"Time window: {delivery.timeframe_start.strftime('%H:%M')}-{delivery.timeframe_end.strftime('%H:%M')}")
        print(f"Priority: {delivery.priority}")
        print("---")

if __name__ == "__main__":
    main()