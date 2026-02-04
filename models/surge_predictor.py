"""
Emergency surge predictor: deterministic, realistic data (no random).
In production, integrate with weather APIs and event calendars.
"""
from datetime import datetime


def predict_surge_events():
    """Surge events with fixed, realistic predicted cases."""
    return [
        {'id': 1, 'type': 'Marathon Event', 'location': 'City Center', 'predicted_cases': 20, 'case_types': 'Dehydration, Heat Stroke, Minor Injuries', 'time_to_event': '2 hours', 'severity': 'Medium', 'departments_affected': ['Emergency', 'Orthopedics'], 'recommendation': 'Deploy 2 additional doctors, stock IV fluids'},
        {'id': 2, 'type': 'Heavy Rain Alert', 'location': 'Highway Area', 'predicted_cases': 11, 'case_types': 'Accident Trauma, Fractures', 'time_to_event': '4 hours', 'severity': 'Low', 'departments_affected': ['Emergency', 'Orthopedics'], 'recommendation': 'Prepare trauma bay, alert surgical team'},
        {'id': 3, 'type': 'Flu Season Peak', 'location': 'Citywide', 'predicted_cases': 42, 'case_types': 'Respiratory Issues, Fever', 'time_to_event': 'Today', 'severity': 'High', 'departments_affected': ['General Medicine', 'Pediatrics'], 'recommendation': 'Increase bed capacity, stock antivirals'},
        {'id': 4, 'type': 'Food Festival', 'location': 'Downtown', 'predicted_cases': 14, 'case_types': 'Food Poisoning, Allergic Reactions', 'time_to_event': '6 hours', 'severity': 'Medium', 'departments_affected': ['Emergency'], 'recommendation': 'Stock anti-allergy meds, prepare GI treatment'},
    ]


def get_surge_statistics():
    """Surge statistics (deterministic)."""
    return {
        'total_predicted_cases': 87,
        'high_risk_events': 2,
        'departments_on_alert': ['Emergency', 'Orthopedics', 'General Medicine'],
        'preparation_score': 84,
    }


def get_weather_impact():
    """Weather impact: deterministic by day of week (for demo)."""
    weekday = datetime.now().weekday()
    # Rotate condition by weekday so it's stable per day
    conditions = ['Clear', 'Rainy', 'Hot & Humid', 'Clear', 'Stormy', 'Clear', 'Rainy']
    condition = conditions[weekday]
    impact_map = {
        'Rainy': {'cases': '+15%', 'types': 'Accidents, Fractures'},
        'Hot & Humid': {'cases': '+25%', 'types': 'Heat stroke, Dehydration'},
        'Clear': {'cases': 'Normal', 'types': 'Regular cases'},
        'Stormy': {'cases': '+30%', 'types': 'Trauma, Electric injuries'},
    }
    return {
        'condition': condition,
        'impact': impact_map[condition],
    }
