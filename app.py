from flask import Flask, render_template, jsonify, request
import pandas as pd
from data import generate_crime_data, get_live_crimes, get_police_stations
from model import CrimePredictor
from datetime import datetime

app = Flask(__name__)

# Initialize
crime_data = generate_crime_data(500)
predictor = CrimePredictor()
hotspots = predictor.detect_hotspots(crime_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Get all data in one endpoint"""
    current_hour = datetime.now().hour
    
    # Get predictions for all areas
    predictions = []
    for area in ['Dadar', 'Andheri', 'Bandra', 'Kurla']:
        predictions.append(predictor.predict_risk(area, current_hour))
    
    # Get patrol routes
    num_patrols = request.args.get('patrols', 3, type=int)
    patrols = predictor.optimize_patrols(hotspots, num_patrols)
    
    response = {
        'hotspots': hotspots,
        'predictions': predictions,
        'patrols': patrols,
        'live_crimes': get_live_crimes(),
        'police_stations': get_police_stations(),
        'stats': {
            'total_crimes': len(crime_data),
            'high_risk_zones': len([h for h in hotspots if h['severity'] == 'High']),
            'live_alerts': len(get_live_crimes()),
            'prediction_accuracy': 87
        }
    }
    
    return jsonify(response)

@app.route('/api/update')
def update_data():
    """Update with new data"""
    new_crime = get_live_crimes()
    return jsonify({
        'new_crimes': new_crime,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

if __name__ == '__main__':
    print("🚀 SafeCity Mumbai Server Starting...")
    print(f"📊 Generated {len(crime_data)} crime records")
    print(f"🔥 Detected {len(hotspots)} hotspots")
    print("🌐 Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)