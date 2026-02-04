"""
Resource exchange: deterministic, realistic data (no random).
"""

def get_hospital_network():
    """Get list of hospitals in the network."""
    return [
        {'id': 1, 'name': 'HealFlow Central Hospital', 'location': 'Downtown', 'distance': '0 km', 'status': 'Active', 'is_current': True},
        {'id': 2, 'name': 'City General Hospital', 'location': 'North District', 'distance': '3.5 km', 'status': 'Active', 'is_current': False},
        {'id': 3, 'name': 'MetroCare Medical Center', 'location': 'East Side', 'distance': '5.2 km', 'status': 'Active', 'is_current': False},
        {'id': 4, 'name': 'LifeLine Hospital', 'location': 'West End', 'distance': '7.8 km', 'status': 'Active', 'is_current': False},
    ]


def get_available_resources():
    """Get resources available for sharing (fixed realistic data)."""
    return [
        {'id': 1, 'hospital_name': 'City General Hospital', 'resource_type': 'ICU Beds', 'quantity': 2, 'availability': 'Immediate', 'distance': '3.5 km', 'contact': '+1-555-0102'},
        {'id': 2, 'hospital_name': 'MetroCare Medical Center', 'resource_type': 'Ventilators', 'quantity': 3, 'availability': 'Within 2 hours', 'distance': '5.2 km', 'contact': '+1-555-0103'},
        {'id': 3, 'hospital_name': 'LifeLine Hospital', 'resource_type': 'Blood Units (O+)', 'quantity': 5, 'availability': 'Immediate', 'distance': '7.8 km', 'contact': '+1-555-0104'},
        {'id': 4, 'hospital_name': 'City General Hospital', 'resource_type': 'Surgical Team', 'quantity': 1, 'availability': 'Within 1 hour', 'distance': '3.5 km', 'contact': '+1-555-0102'},
    ]


def get_my_shareable_resources():
    """Get resources current hospital can share (deterministic)."""
    return [
        {'resource_type': 'General Beds', 'available': 10, 'total': 40, 'status': 'Available to share'},
        {'resource_type': 'ICU Beds', 'available': 2, 'total': 10, 'status': 'Limited availability'},
        {'resource_type': 'Ventilators', 'available': 4, 'total': 15, 'status': 'Available to share'},
        {'resource_type': 'Blood Bank (A+)', 'available': 14, 'total': 50, 'status': 'Available to share'},
    ]


def get_resource_requests():
    """Get pending resource requests (fixed)."""
    return [
        {'id': 1, 'from_hospital': 'MetroCare Medical Center', 'resource': 'ICU Bed', 'quantity': 1, 'urgency': 'High', 'reason': 'Critical patient transfer', 'time': '15 mins ago'},
        {'id': 2, 'from_hospital': 'LifeLine Hospital', 'resource': 'Blood Units (B+)', 'quantity': 3, 'urgency': 'Medium', 'reason': 'Emergency surgery', 'time': '1 hour ago'},
    ]
