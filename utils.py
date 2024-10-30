import requests
from flask import flash
import math

def get_coordinates(address):
    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': address, 'format': 'json', 'limit': 1}
        )
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            flash(f'Neizdevās iegūt koordinātes adresei: {address}', 'error')
            return None, None
    except Exception as e:
        flash(f'Kļūda, iegūstot koordinātes: {e}', 'error')
        return None, None

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def solomon_algorithm(locations, vehicle_capacity):
    if not locations:
        return []
    routes = []
    unvisited = locations.copy()
    while unvisited:
        route = []
        capacity_remaining = vehicle_capacity
        current_time = 0
        current_location = unvisited[0]
        route.append(current_location)
        capacity_remaining -= current_location.demand
        unvisited.remove(current_location)
        while True:
            feasible_locations = []
            for loc in unvisited:
                distance = calculate_distance(
                    current_location.latitude, current_location.longitude,
                    loc.latitude, loc.longitude
                )
                arrival_time = current_time + distance
                if (loc.demand <= capacity_remaining and
                    arrival_time >= loc.ready_time and
                    arrival_time <= loc.due_time):
                    feasible_locations.append((loc, distance))
            if not feasible_locations:
                break
            feasible_locations.sort(key=lambda x: x[1])
            next_location, distance = feasible_locations[0]
            route.append(next_location)
            capacity_remaining -= next_location.demand
            current_time += distance + next_location.service_time
            current_location = next_location
            unvisited.remove(next_location)
        routes.append(route)
    return routes
