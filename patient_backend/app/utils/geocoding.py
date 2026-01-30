import requests
import time

def geocode_address(address):
    """
    Geocode an address using Nominatim (OpenStreetMap).
    Returns (lat, lng) or (None, None).
    """
    if not address:
        return None, None
        
    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {
        'User-Agent': 'NationalHealthcareApp/1.0 (contact@example.com)' 
    }
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    
    try:
        # Nominatim requires 1s delay/throttling mostly, but for occasional use 
        # inside our app it's fine. If bulk, add sleep.
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
        
    return None, None
