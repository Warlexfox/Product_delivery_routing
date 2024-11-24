from flask import flash
import requests

def get_coordinates(country, city, address):
    full_address = f"{address}, {city}, {country}"
    try:
        headers = {'User-Agent': 'YourAppName/1.0 (your_email@example.com)'}
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': full_address, 'format': 'json', 'limit': 1},
            headers=headers
        )
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            flash(f'Failed to get coordinates for address: {full_address}', 'error')
            return None, None
    except Exception as e:
        flash(f'Error getting coordinates: {e}', 'error')
        return None, None
