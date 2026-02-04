from flask import Flask, render_template, jsonify, request
import os
from models.database import init_db, get_patient_data, get_department_data, get_bed_allocation, get_total_patients_today, get_staff_count
from models.inflow_model import predict_patient_inflow, get_all_departments_prediction, get_prediction_dates
from models.queue_model import mmc_queue_simulation, calculate_probability_no_wait
from models.surge_predictor import predict_surge_events, get_surge_statistics, get_weather_impact
from models.resource_exchange import get_hospital_network, get_available_resources, get_my_shareable_resources, get_resource_requests
from models.supply_chain import get_supply_inventory, get_supply_predictions, get_supply_statistics, get_usage_trend

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

if not os.path.exists('/tmp/hospital.db'):
    init_db()

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/prediction')
def prediction():
    """Patient flow prediction page"""
    return render_template('prediction.html')

@app.route('/queue')
def queue():
    """Queue simulation page"""
    return render_template('queue.html')

@app.route('/allocation')
def allocation():
    """Bed and staff allocation page"""
    return render_template('allocation.html')

@app.route('/overview')
def overview():
    """System overview page"""
    return render_template('overview.html')

@app.route('/surge-predictor')
def surge_predictor():
    """Emergency Surge Predictor page"""
    return render_template('surge_predictor.html')

@app.route('/resource-exchange')
def resource_exchange():
    """Resource Exchange Network page"""
    return render_template('resource_exchange.html')

@app.route('/supply-chain')
def supply_chain():
    """Supply Chain Assistant page"""
    return render_template('supply_chain.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for patient flow prediction"""
    data = request.get_json()
    department = data.get('department', 'Emergency')
    
    predictions = predict_patient_inflow(department)
    dates = get_prediction_dates()
    
    return jsonify({
        'department': department,
        'dates': dates,
        'predictions': predictions
    })

@app.route('/api/predict/all', methods=['GET'])
def api_predict_all():
    """Get predictions for all departments"""
    predictions = get_all_departments_prediction()
    dates = get_prediction_dates()
    
    return jsonify({
        'dates': dates,
        'predictions': predictions
    })

@app.route('/api/queue/simulate', methods=['POST'])
def api_queue_simulate():
    """API endpoint for queue simulation"""
    data = request.get_json()
    
    arrival_rate = float(data.get('arrival_rate', 20))
    service_rate = float(data.get('service_rate', 5))
    servers = int(data.get('servers', 3))
    
    results = mmc_queue_simulation(arrival_rate, service_rate, servers)
    prob_no_wait = calculate_probability_no_wait(arrival_rate, service_rate, servers)
    
    results['prob_no_wait'] = prob_no_wait
    
    return jsonify(results)

@app.route('/api/beds/allocate', methods=['POST'])
def api_allocate_beds():
    """API endpoint for bed allocation optimization"""
    bed_data = get_bed_allocation()
    
    recommendations = []
    for dept, total, occupied in bed_data:
        utilization = (occupied / total) * 100 if total > 0 else 0
        
        if utilization > 85:
            recommendation = f"Add 5-10 beds (Critical: {utilization:.1f}% occupancy)"
        elif utilization > 70:
            recommendation = f"Consider adding 3-5 beds ({utilization:.1f}% occupancy)"
        elif utilization < 40:
            recommendation = f"Optimize usage or reallocate ({utilization:.1f}% occupancy)"
        else:
            recommendation = f"Optimal ({utilization:.1f}% occupancy)"
        
        recommendations.append({
            'department': dept,
            'total_beds': total,
            'occupied_beds': occupied,
            'available_beds': total - occupied,
            'utilization': round(utilization, 1),
            'recommendation': recommendation
        })
    
    return jsonify(recommendations)

@app.route('/api/overview/stats', methods=['GET'])
def api_overview_stats():
    """API endpoint for overview statistics (derived from real DB data)."""
    bed_data = get_bed_allocation()
    total_beds = sum([total for _, total, _ in bed_data])
    occupied_beds = sum([occupied for _, _, occupied in bed_data])
    bed_occupancy = (occupied_beds / total_beds * 100) if total_beds > 0 else 0

    total_patients = get_total_patients_today()
    # Deterministic: wait time estimate from occupancy (higher occupancy -> longer wait)
    avg_wait_time = int(12 + (bed_occupancy / 100) * 28)
    avg_wait_time = max(10, min(45, avg_wait_time))
    # Staff efficiency from bed utilization (realistic band)
    staff_efficiency = int(78 + (1 - bed_occupancy / 100) * 14)
    staff_efficiency = max(72, min(95, staff_efficiency))

    patient_distribution = []
    for dept, count in get_patient_data():
        patient_distribution.append({'department': dept, 'count': count})

    return jsonify({
        'total_patients': total_patients,
        'avg_wait_time': avg_wait_time,
        'bed_occupancy': round(bed_occupancy, 1),
        'staff_efficiency': staff_efficiency,
        'patient_distribution': patient_distribution
    })

@app.route('/api/departments', methods=['GET'])
def api_departments():
    """Get all departments"""
    dept_data = get_department_data()
    departments = []
    
    for name, total_beds, occupied_beds in dept_data:
        departments.append({
            'name': name,
            'total_beds': total_beds,
            'occupied_beds': occupied_beds,
            'available_beds': total_beds - occupied_beds
        })
    
    return jsonify(departments)

@app.route('/api/surge/events', methods=['GET'])
def api_surge_events():
    """Get surge prediction events"""
    events = predict_surge_events()
    return jsonify(events)

@app.route('/api/surge/stats', methods=['GET'])
def api_surge_stats():
    """Get surge statistics"""
    stats = get_surge_statistics()
    weather = get_weather_impact()
    stats['weather'] = weather
    return jsonify(stats)

@app.route('/api/resources/network', methods=['GET'])
def api_resource_network():
    """Get hospital network"""
    hospitals = get_hospital_network()
    return jsonify(hospitals)

@app.route('/api/resources/available', methods=['GET'])
def api_resources_available():
    """Get available resources from other hospitals"""
    resources = get_available_resources()
    return jsonify(resources)

@app.route('/api/resources/mine', methods=['GET'])
def api_my_resources():
    """Get my shareable resources"""
    resources = get_my_shareable_resources()
    return jsonify(resources)

@app.route('/api/resources/requests', methods=['GET'])
def api_resource_requests():
    """Get resource requests"""
    requests = get_resource_requests()
    return jsonify(requests)

@app.route('/api/supply/inventory', methods=['GET'])
def api_supply_inventory():
    """Get supply inventory"""
    supplies = get_supply_inventory()
    return jsonify(supplies)

@app.route('/api/supply/predictions', methods=['GET'])
def api_supply_predictions():
    """Get supply shortage predictions"""
    predictions = get_supply_predictions()
    return jsonify(predictions)

@app.route('/api/supply/stats', methods=['GET'])
def api_supply_stats():
    """Get supply statistics"""
    stats = get_supply_statistics()
    return jsonify(stats)

@app.route('/api/supply/trend', methods=['GET'])
def api_supply_trend():
    """Get usage trend"""
    trend = get_usage_trend()
    return jsonify(trend)

@app.route('/api/patient-data', methods=['GET'])
def api_patient_data():
    """Get patient data"""
    data = get_patient_data()
    return jsonify(data)

@app.route('/api/department-data', methods=['GET'])
def api_department_data():
    """Get department data"""
    data = get_department_data()
    return jsonify(data)

@app.route('/api/bed-allocation', methods=['GET'])
def api_bed_allocation():
    """Get bed allocation data"""
    data = get_bed_allocation()
    return jsonify(data)

@app.route('/api/total-patients-today', methods=['GET'])
def api_total_patients_today():
    """Get total patients today"""
    data = get_total_patients_today()
    return jsonify(data)

@app.route('/api/staff-count', methods=['GET'])
def api_staff_count():
    """Get staff count"""
    data = get_staff_count()
    return jsonify(data)

@app.route('/api/predict-inflow', methods=['POST'])
def api_predict_inflow():
    """Predict patient inflow"""
    data = request.get_json()
    department = data.get('department')
    date = data.get('date')
    prediction = predict_patient_inflow(department, date)
    return jsonify({'prediction': prediction})

@app.route('/api/predict-all-departments', methods=['GET'])
def api_predict_all_departments():
    """Get predictions for all departments"""
    predictions = get_all_departments_prediction()
    return jsonify(predictions)

@app.route('/api/prediction-dates', methods=['GET'])
def api_prediction_dates():
    """Get prediction dates"""
    dates = get_prediction_dates()
    return jsonify(dates)

@app.route('/api/queue-simulation', methods=['POST'])
def api_queue_simulation():
    """Run queue simulation"""
    data = request.get_json()
    arrival_rate = data.get('arrival_rate')
    service_rate = data.get('service_rate')
    servers = data.get('servers')
    result = mmc_queue_simulation(arrival_rate, service_rate, servers)
    return jsonify(result)

@app.route('/api/queue-probability', methods=['POST'])
def api_queue_probability():
    """Calculate probability of no wait"""
    data = request.get_json()
    arrival_rate = data.get('arrival_rate')
    service_rate = data.get('service_rate')
    servers = data.get('servers')
    probability = calculate_probability_no_wait(arrival_rate, service_rate, servers)
    return jsonify({'probability': probability})

@app.route('/api/surge-events', methods=['GET'])
def api_surge_events():
    """Get surge event predictions"""
    events = predict_surge_events()
    return jsonify(events)

@app.route('/api/surge-stats', methods=['GET'])
def api_surge_stats():
    """Get surge statistics"""
    stats = get_surge_statistics()
    return jsonify(stats)

@app.route('/api/weather-impact', methods=['GET'])
def api_weather_impact():
    """Get weather impact on surge"""
    impact = get_weather_impact()
    return jsonify(impact)

@app.route('/api/hospital-network', methods=['GET'])
def api_hospital_network():
    """Get hospital network"""
    network = get_hospital_network()
    return jsonify(network)

@app.route('/api/resources/available', methods=['GET'])
def api_available_resources():
    """Get available resources"""
    resources = get_available_resources()
    return jsonify(resources)

@app.route('/api/resources/mine', methods=['GET'])
def api_my_resources():
    """Get my shareable resources"""
    resources = get_my_shareable_resources()
    return jsonify(resources)

@app.route('/api/resources/requests', methods=['GET'])
def api_resource_requests():
    """Get resource requests"""
    requests = get_resource_requests()
    return jsonify(requests)

@app.route('/api/supply/inventory', methods=['GET'])
def api_supply_inventory():
    """Get supply inventory"""
    supplies = get_supply_inventory()
    return jsonify(supplies)

@app.route('/api/supply/predictions', methods=['GET'])
def api_supply_predictions():
    """Get supply shortage predictions"""
    predictions = get_supply_predictions()
    return jsonify(predictions)

@app.route('/api/supply/stats', methods=['GET'])
def api_supply_stats():
    """Get supply statistics"""
    stats = get_supply_statistics()
    return jsonify(stats)

@app.route('/api/supply/trend', methods=['GET'])
def api_supply_trend():
    """Get usage trend"""
    trend = get_usage_trend()
    return jsonify(trend)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)