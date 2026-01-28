import numpy as np
from sklearn.cluster import DBSCAN
from datetime import datetime

class CrimePredictor:
    def __init__(self):
        self.hotspots = []
        
    def detect_hotspots(self, crime_data):
        """Find crime hotspots using clustering"""
        if len(crime_data) == 0:
            return []
            
        coords = np.array([[row['latitude'], row['longitude']] for _, row in crime_data.iterrows()])
        
        # DBSCAN clustering
        clustering = DBSCAN(eps=0.01, min_samples=3).fit(coords)
        
        hotspots = []
        for label in set(clustering.labels_):
            if label != -1:  # Ignore noise
                cluster_points = coords[clustering.labels_ == label]
                center = cluster_points.mean(axis=0)
                
                hotspots.append({
                    'lat': float(center[0]),
                    'lon': float(center[1]),
                    'radius': 0.002 * len(cluster_points),
                    'crime_count': int(len(cluster_points)),
                    'severity': 'High' if len(cluster_points) > 10 else 'Medium'
                })
        
        self.hotspots = hotspots
        return hotspots
    
    def predict_risk(self, area_name, current_hour):
        """Predict crime risk for area"""
        risk_map = {
            'Dadar': {'base': 0.7, 'night_boost': 0.3},
            'Andheri': {'base': 0.8, 'night_boost': 0.4},
            'Kurla': {'base': 0.75, 'night_boost': 0.35},
            'Bandra': {'base': 0.6, 'night_boost': 0.25},
            'default': {'base': 0.5, 'night_boost': 0.2}
        }
        
        area = risk_map.get(area_name, risk_map['default'])
        risk = area['base']
        
        # Night time increases risk
        if 20 <= current_hour <= 23 or 0 <= current_hour <= 4:
            risk += area['night_boost']
        
        # Add some randomness
        risk += np.random.uniform(-0.1, 0.1)
        risk = min(max(risk, 0), 1)
        
        return {
            'area': area_name,
            'risk_score': round(risk, 2),
            'level': 'High' if risk > 0.7 else 'Medium' if risk > 0.4 else 'Low'
        }
    
    def optimize_patrols(self, hotspots, num_patrols=3):
        """Generate patrol routes"""
        if not hotspots:
            return []
            
        # Sort by crime count
        sorted_hotspots = sorted(hotspots, key=lambda x: x['crime_count'], reverse=True)
        
        # Simple patrol assignment
        patrols = []
        for i in range(min(num_patrols, len(sorted_hotspots))):
            patrols.append({
                'id': i + 1,
                'hotspots': [sorted_hotspots[i]],
                'route': [sorted_hotspots[i]],
                'status': 'Active'
            })
        
        return patrols