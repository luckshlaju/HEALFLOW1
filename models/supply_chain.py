"""
Supply chain: deterministic, realistic inventory and trends (Vercel-safe).
No filesystem, no DB, no randomness.
"""

from datetime import datetime, timedelta


def get_supply_inventory():
    """Current medical supply inventory."""
    return [
        {
            "id": 1,
            "name": "PPE Kits (N95 Masks)",
            "currentStock": 380,
            "minRequired": 1000,
            "dailyUsage": 95,
            "daysRemaining": 4,
            "status": "Critical",
            "autoOrder": True,
            "supplier": "MedSupply Co.",
        },
        {
            "id": 2,
            "name": "Surgical Gloves",
            "currentStock": 2500,
            "minRequired": 2000,
            "dailyUsage": 250,
            "daysRemaining": 10,
            "status": "Good",
            "autoOrder": False,
            "supplier": "HealthCare Supplies Inc.",
        },
        {
            "id": 3,
            "name": "IV Fluids (Saline)",
            "currentStock": 220,
            "minRequired": 500,
            "dailyUsage": 48,
            "daysRemaining": 5,
            "status": "Low",
            "autoOrder": True,
            "supplier": "Pharma Direct",
        },
        {
            "id": 4,
            "name": "Antibiotics (Amoxicillin)",
            "currentStock": 620,
            "minRequired": 400,
            "dailyUsage": 38,
            "daysRemaining": 12,
            "status": "Good",
            "autoOrder": False,
            "supplier": "MediPharm Ltd.",
        },
        {
            "id": 5,
            "name": "Oxygen Cylinders",
            "currentStock": 22,
            "minRequired": 50,
            "dailyUsage": 10,
            "daysRemaining": 2,
            "status": "Critical",
            "autoOrder": True,
            "supplier": "OxygenTech",
        },
        {
            "id": 6,
            "name": "Syringes (Disposable)",
            "currentStock": 6200,
            "minRequired": 3000,
            "dailyUsage": 480,
            "daysRemaining": 12,
            "status": "Good",
            "autoOrder": False,
            "supplier": "MedSupply Co.",
        },
    ]


def get_supply_predictions():
    """Supply shortage predictions."""
    today = datetime.now()
    return [
        {
            "item": "PPE Kits (N95 Masks)",
            "shortageDate": (today + timedelta(days=4)).strftime("%Y-%m-%d"),
            "severity": "High",
            "recommendedOrder": "2000 units",
            "estimatedCost": 3500,
        },
        {
            "item": "Oxygen Cylinders",
            "shortageDate": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
            "severity": "Critical",
            "recommendedOrder": "50 cylinders",
            "estimatedCost": 15000,
        },
        {
            "item": "IV Fluids (Saline)",
            "shortageDate": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "severity": "Medium",
            "recommendedOrder": "500 units",
            "estimatedCost": 2000,
        },
    ]


def get_supply_statistics():
    """Top summary cards."""
    return {
        "totalItems": 6,
        "criticalItems": 2,
        "autoOrdersPending": 4,
        "monthlySpend": 52400,
        "wastageReduction": 15,
    }


def get_usage_trend():
    """7-day usage trend (frontend-chart friendly)."""
    today = datetime.now()

    base_ppe = [92, 98, 105, 102, 96, 88, 90]
    base_iv = [44, 48, 52, 50, 46, 42, 44]
    base_oxygen = [9, 10, 11, 10, 9, 8, 9]

    trend = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        trend.append({
            "date": day.strftime("%a"),
            "ppe": base_ppe[i],
            "ivFluids": base_iv[i],
            "oxygen": base_oxygen[i],
        })

    return trend
