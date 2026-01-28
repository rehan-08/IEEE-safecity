let map;
let mapLayers = {};
let currentData = {};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    loadData();
    updateTime();
    setInterval(loadData, 30000); // Refresh every 30 seconds
    setInterval(updateTime, 1000);
});

// Initialize Leaflet Map
function initMap() {
    map = L.map('map').setView([19.0760, 72.8777], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// Load data from API
async function loadData() {
    try {
        const response = await fetch('/api/data');
        currentData = await response.json();
        
        updateDashboard();
        updateMap();
        updateLastUpdate();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Update dashboard with data
function updateDashboard() {
    // Update stats
    document.getElementById('total-crimes').textContent = 
        currentData.stats?.total_crimes || 0;
    document.getElementById('hotspot-count').textContent = 
        currentData.hotspots?.length || 0;
    document.getElementById('live-alerts').textContent = 
        currentData.stats?.live_alerts || 0;
    
    // Update predictions
    const predictionsContainer = document.getElementById('predictions-container');
    if (currentData.predictions) {
        predictionsContainer.innerHTML = currentData.predictions.map(pred => `
            <div class="prediction-item">
                <div>${pred.area}</div>
                <div class="risk-info">
                    ${pred.level}
                    <div class="risk-bar">
                        <div class="risk-fill" style="width: ${pred.risk_score * 100}%"></div>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    // Update patrols
    updatePatrolsDisplay();
    
    // Update alerts
    const alertsContainer = document.getElementById('alerts-container');
    if (currentData.live_crimes) {
        alertsContainer.innerHTML = currentData.live_crimes.map(crime => `
            <div class="alert-item">
                <div>
                    <strong>${crime.crime_type}</strong><br>
                    ${crime.area} • ${crime.timestamp}
                </div>
                <div>${crime.status}</div>
            </div>
        `).join('');
    }
}

// Update patrols display
function updatePatrolsDisplay() {
    const patrolsContainer = document.getElementById('patrols-container');
    const activePatrols = document.getElementById('active-patrols');
    
    if (currentData.patrols) {
        patrolsContainer.innerHTML = currentData.patrols.map(patrol => `
            <div class="patrol-item">
                <div><strong>Patrol ${patrol.id}</strong></div>
                <div>Hotspots: ${patrol.hotspots?.length || 0}</div>
                <div>Status: ${patrol.status}</div>
            </div>
        `).join('');
        
        activePatrols.textContent = currentData.patrols.length;
    }
}

// Update map with layers
function updateMap() {
    // Clear existing layers
    Object.values(mapLayers).forEach(layer => {
        if (layer) map.removeLayer(layer);
    });
    
    // Add hotspots
    if (currentData.hotspots) {
        const hotspotsLayer = L.layerGroup();
        currentData.hotspots.forEach(hotspot => {
            L.circle([hotspot.lat, hotspot.lon], {
                radius: hotspot.radius * 100000,
                color: hotspot.severity === 'High' ? '#FF3B30' : 
                       hotspot.severity === 'Medium' ? '#FF9500' : '#34C759',
                fillOpacity: 0.3
            }).addTo(hotspotsLayer)
            .bindPopup(`<b>${hotspot.severity} Risk</b><br>
                       Crimes: ${hotspot.crime_count}`);
        });
        hotspotsLayer.addTo(map);
        mapLayers.hotspots = hotspotsLayer;
    }
    
    // Add police stations
    if (currentData.police_stations) {
        const stationsLayer = L.layerGroup();
        currentData.police_stations.forEach(station => {
            L.marker([station.lat, station.lon])
                .addTo(stationsLayer)
                .bindPopup(`<b>${station.name}</b>`);
        });
        stationsLayer.addTo(map);
        mapLayers.stations = stationsLayer;
    }
    
    // Add live crimes
    if (currentData.live_crimes) {
        const crimesLayer = L.layerGroup();
        currentData.live_crimes.forEach(crime => {
            L.circleMarker([crime.lat, crime.lon], {
                radius: 8,
                color: '#FF3B30',
                fillColor: '#FF3B30',
                fillOpacity: 0.8
            }).addTo(crimesLayer)
            .bindPopup(`<b>${crime.crime_type}</b><br>
                       ${crime.area}<br>
                       ${crime.timestamp}`);
        });
        crimesLayer.addTo(map);
        mapLayers.crimes = crimesLayer;
    }
}

// Map control functions
function showHeatmap() {
    // Add heatmap layer
    if (currentData.live_crimes) {
        const heatPoints = currentData.live_crimes.map(crime => [crime.lat, crime.lon, 1]);
        if (mapLayers.heatmap) map.removeLayer(mapLayers.heatmap);
        
        mapLayers.heatmap = L.heatLayer(heatPoints, {
            radius: 25,
            blur: 15,
            maxZoom: 17
        }).addTo(map);
    }
}

function showHotspots() {
    // Ensure hotspots are visible
    if (mapLayers.hotspots) {
        map.removeLayer(mapLayers.hotspots);
        mapLayers.hotspots.addTo(map);
    }
}

function showPatrols() {
    // Show patrol routes (simplified)
    if (currentData.hotspots) {
        const patrolLayer = L.layerGroup();
        currentData.hotspots.forEach((hotspot, index) => {
            if (index % 2 === 0) { // Simple pattern for demo
                L.polyline([
                    [hotspot.lat + 0.005, hotspot.lon + 0.005],
                    [hotspot.lat, hotspot.lon],
                    [hotspot.lat - 0.005, hotspot.lon - 0.005]
                ], {color: '#0047AB', weight: 3}).addTo(patrolLayer);
            }
        });
        
        if (mapLayers.patrols) map.removeLayer(mapLayers.patrols);
        mapLayers.patrols = patrolLayer.addTo(map);
    }
}

// Update patrol count
async function updatePatrols() {
    const count = document.getElementById('patrol-input').value;
    const response = await fetch(`/api/data?patrols=${count}`);
    currentData = await response.json();
    updateDashboard();
    updateMap();
}

// Utility functions
function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = 
        now.toLocaleTimeString('en-IN', {hour12: false});
}

function updateLastUpdate() {
    const now = new Date();
    document.getElementById('last-update').textContent = 
        `Last updated: ${now.toLocaleTimeString('en-IN', {hour12: false})}`;
}