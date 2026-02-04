"""
Patient inflow prediction using deterministic, realistic patterns.
Uses day-of-week and department-specific base rates (no random values).
Replace with ML model trained on real OPD/hospital data when available.
"""
from datetime import datetime, timedelta

# Base daily patient counts per department (typical mid-size hospital)
# Source: realistic ranges from public health / OPD benchmarks
DEPARTMENT_BASE_RATES = {
    'Emergency': 45,
    'Cardiology': 28,
    'Orthopedics': 22,
    'Pediatrics': 38,
    'General Medicine': 52,
}

# Day-of-week multiplier (1.0 = average). Weekdays higher, weekend lower.
DAY_OF_WEEK_MULTIPLIER = {
    0: 0.85,   # Monday
    1: 1.05,   # Tuesday
    2: 1.02,   # Wednesday
    3: 1.00,   # Thursday
    4: 1.08,   # Friday
    5: 0.75,   # Saturday
    6: 0.72,   # Sunday
}


def predict_patient_inflow(department):
    """
    Predict patient inflow for next 7 days using day-of-week and department base rates.
    Deterministic and reproducible (no random).
    """
    base = DEPARTMENT_BASE_RATES.get(department, 35)
    predictions = []
    today = datetime.now()
    for i in range(7):
        d = today + timedelta(days=i)
        mult = DAY_OF_WEEK_MULTIPLIER.get(d.weekday(), 1.0)
        value = max(5, int(base * mult))
        predictions.append(value)
    return predictions


def get_all_departments_prediction():
    """Get predictions for all departments (deterministic)."""
    departments = list(DEPARTMENT_BASE_RATES.keys())
    predictions = {}
    for dept in departments:
        predictions[dept] = predict_patient_inflow(dept)
    return predictions


def get_prediction_dates():
    """Generate dates for next 7 days."""
    dates = []
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
    return dates
