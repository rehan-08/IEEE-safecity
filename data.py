import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Mumbai area coordinates (simplified)
MUMBAI_AREAS = {
    'Dadar': {'lat': 19.0176, 'lon': 72.8422, 'crime_rate': 0.8},
    'Andheri': {'lat': 19.1136, 'lon': 72.8697, 'crime_rate': 0.9},
    'Bandra': {'lat': 19.0544, 'lon': 72.8404, 'crime_rate': 0.6},
    'Colaba': {'lat': 18.9066, 'lon': 72.8146, 'crime_rate': 0.7},
    'Borivali': {'lat': 19.2307, 'lon': 72.8567, 'crime_rate': 0.5},
    'Kurla': {'lat': 19.0728, 'lon': 72.8826, 'crime_rate': 0.85},
    'Vashi': {'lat': 19.0820, 'lon': 73.0100, 'crime_rate': 0.4},
}

CRIME_TYPES = ['Theft', 'Assault', 'Burglary', 'Robbery', 'Vandalism']

def generate_crime_data(n=1000):
    """Generate synthetic crime dataset"""
    data = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(n):
        area_name = random.choice(list(MUMBAI_AREAS.keys()))
        area = MUMBAI_AREAS[area_name]
        
        # Add time-based patterns
        crime_date = start_date + timedelta(days=random.randint(0, 90))
        hour = random.randint(0, 23)
        
        # Night crimes are more likely
        night_multiplier = 1.8 if 20 <= hour <= 23 or 0 <= hour <= 4 else 1.0
        weekend_multiplier = 1.5 if crime_date.weekday() >= 5 else 1.0
        
        # Generate crime if probability passes
        if random.random() < area['crime_rate'] * night_multiplier * weekend_multiplier * 0.5:
            data.append({
                'id': i,
                'date': crime_date.strftime('%Y-%m-%d'),
                'time': f'{hour:02d}:{random.randint(0,59):02d}',
                'crime_type': random.choice(CRIME_TYPES),
                'latitude': area['lat'] + random.uniform(-0.01, 0.01),
                'longitude': area['lon'] + random.uniform(-0.01, 0.01),
                'area': area_name,
                'severity': random.choice(['Low', 'Medium', 'High'])
            })
    
    return pd.DataFrame(data)

def get_live_crimes():
    """Generate real-time crime data"""
    live_data = []
    for _ in range(random.randint(0, 10)):
        area_name = random.choice(list(MUMBAI_AREAS.keys()))
        area = MUMBAI_AREAS[area_name]
        
        live_data.append({
            'id': random.randint(1000, 9999),
            'timestamp': datetime.now().strftime('%H:%M'),
            'crime_type': random.choice(CRIME_TYPES),
            'lat': area['lat'] + random.uniform(-0.005, 0.005),
            'lon': area['lon'] + random.uniform(-0.005, 0.005),
            'area': area_name,
            'status': 'Just Reported'
        })
    
    return live_data

def get_police_stations():
    """Police station locations"""
    return [
        {'name': 'Colaba PS', 'lat': 18.9066, 'lon': 72.8146},
        {'name': 'Dadar PS', 'lat': 19.0176, 'lon': 72.8422},
        {'name': 'Andheri PS', 'lat': 19.1136, 'lon': 72.8697},
        {'name': 'Bandra PS', 'lat': 19.0544, 'lon': 72.8404},
        {'name': 'Vashi PS', 'lat': 19.0820, 'lon': 73.0100},
    ]