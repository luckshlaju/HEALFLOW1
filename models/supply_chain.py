"""
Supply chain: deterministic, realistic inventory and trends (no random).
"""
from datetime import datetime, timedelta


def get_supply_inventory():
    """Current medical supply inventory (fixed realistic data)."""
    return [
        {'id': 1, 'name': 'PPE Kits (N95 Masks)', 'current_stock': 380, 'min_required': 1000, 'daily_usage': 95, 'days_remaining': 4, 'status': 'Critical', 'auto_order': True, 'supplier': 'MedSupply Co.'},
        {'id': 2, 'name': 'Surgical Gloves', 'current_stock': 2500, 'min_required': 2000, 'daily_usage': 250, 'days_remaining': 10, 'status': 'Good', 'auto_order': False, 'supplier': 'HealthCare Supplies Inc.'},
        {'id': 3, 'name': 'IV Fluids (Saline)', 'current_stock': 220, 'min_required': 500, 'daily_usage': 48, 'days_remaining': 5, 'status': 'Low', 'auto_order': True, 'supplier': 'Pharma Direct'},
        {'id': 4, 'name': 'Antibiotics (Amoxicillin)', 'current_stock': 620, 'min_required': 400, 'daily_usage': 38, 'days_remaining': 12, 'status': 'Good', 'auto_order': False, 'supplier': 'MediPharm Ltd.'},
        {'id': 5, 'name': 'Oxygen Cylinders', 'current_stock': 22, 'min_required': 50, 'daily_usage': 10, 'days_remaining': 2, 'status': 'Critical', 'auto_order': True, 'supplier': 'OxygenTech'},
        {'id': 6, 'name': 'Syringes (Disposable)', 'current_stock': 6200, 'min_required': 3000, 'daily_usage': 480, 'days_remaining': 12, 'status': 'Good', 'auto_order': False, 'supplier': 'MedSupply Co.'},
    ]


def get_supply_predictions():
    """Supply shortage predictions (deterministic from today)."""
    today = datetime.now()
    return [
        {'item': 'PPE Kits (N95 Masks)', 'shortage_date': (today + timedelta(days=4)).strftime('%Y-%m-%d'), 'severity': 'High', 'recommended_order': '2000 units', 'estimated_cost': '$3,500'},
        {'item': 'Oxygen Cylinders', 'shortage_date': (today + timedelta(days=3)).strftime('%Y-%m-%d'), 'severity': 'Critical', 'recommended_order': '50 cylinders', 'estimated_cost': '$15,000'},
        {'item': 'IV Fluids (Saline)', 'shortage_date': (today + timedelta(days=5)).strftime('%Y-%m-%d'), 'severity': 'Medium', 'recommended_order': '500 units', 'estimated_cost': '$2,000'},
    ]


def get_supply_statistics():
    """Supply chain statistics (fixed)."""
    return {
        'total_items': 6,
        'critical_items': 2,
        'auto_orders_pending': 4,
        'monthly_spend': '$52,400',
        'wastage_reduction': '15%',
    }


def get_usage_trend():
    """7-day usage trend (deterministic pattern)."""
    today = datetime.now()
    # Realistic weekly pattern: mid-week peak
    base_ppe = [92, 98, 105, 102, 96, 88, 90]
    base_iv = [44, 48, 52, 50, 46, 42, 44]
    base_oxygen = [9, 10, 11, 10, 9, 8, 9]
    days = []
    for i in range(7):
        d = today - timedelta(days=6 - i)
        days.append({
            'date': d.strftime('%a'),
            'ppe': base_ppe[i],
            'iv_fluids': base_iv[i],
            'oxygen': base_oxygen[i],
        })
    return days
