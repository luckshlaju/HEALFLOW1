from flask import Flask, render_template, jsonify, request
import os
import traceback

from models.database import (
    init_db,
    get_patient_data,
    get_department_data,
    get_bed_allocation,
    get_total_patients_today,
)

from models.inflow_model import (
    predict_patient_inflow,
    get_all_departments_prediction,
    get_prediction_dates,
)

from models.queue_model import (
    mmc_queue_simulation,
    calculate_probability_no_wait,
)

from models.surge_predictor import (
    predict_surge_events,
    get_surge_statistics,
    get_weather_impact,
)

from models.resource_exchange import (
    get_hospital_network,
    get_available_resources,
    get_my_shareable_resources,
    get_resource_requests,
)

from models.supply_chain import (
    get_supply_inventory,
    get_supply_predictions,
    get_supply_statistics,
    get_usage_trend,
)

# -----------------------------------------------------------------------------
# Flask App Setup
# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# -----------------------------------------------------------------------------
# Database Initialization (safe for local + Vercel)
# -----------------------------------------------------------------------------

DB_PATH = "/tmp/hospital.db" if os.environ.get("VERCEL") else "hospital.db"

if not os.path.exists(DB_PATH):
    try:
        init_db()
    except Exception as e:
        print("DB init failed:", e)

# -----------------------------------------------------------------------------
# Page Routes
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


@app.route("/queue")
def queue():
    return render_template("queue.html")


@app.route("/allocation")
def allocation():
    return render_template("allocation.html")


@app.route("/overview")
def overview():
    return render_template("overview.html")


@app.route("/surge-predictor")
def surge_predictor():
    return render_template("surge_predictor.html")


@app.route("/resource-exchange")
def resource_exchange():
    return render_template("resource_exchange.html")


@app.route("/supply-chain")
def supply_chain():
    return render_template("supply_chain.html")

# -----------------------------------------------------------------------------
# API Routes
# -----------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True)
    department = data.get("department", "Emergency")

    return jsonify({
        "department": department,
        "dates": get_prediction_dates(),
        "predictions": predict_patient_inflow(department),
    })


@app.route("/api/predict/all", methods=["GET"])
def api_predict_all():
    return jsonify({
        "dates": get_prediction_dates(),
        "predictions": get_all_departments_prediction(),
    })


@app.route("/api/queue/simulate", methods=["POST"])
def api_queue_simulate():
    data = request.get_json(force=True)

    arrival_rate = float(data.get("arrival_rate", 20))
    service_rate = float(data.get("service_rate", 5))
    servers = int(data.get("servers", 3))

    results = mmc_queue_simulation(arrival_rate, service_rate, servers)
    results["prob_no_wait"] = calculate_probability_no_wait(
        arrival_rate, service_rate, servers
    )

    return jsonify(results)

# -----------------------------------------------------------------------------
# ✅ FIXED: Bed Allocation API (NO MORE 500 / JSON ERRORS)
# -----------------------------------------------------------------------------

@app.route("/api/beds/allocate", methods=["POST"])
def api_allocate_beds():
    try:
        bed_data = get_bed_allocation()

        if not bed_data:
            return jsonify({
                "error": "No bed data found in database",
                "recommendations": []
            })

        recommendations = []

        for row in bed_data:
            if len(row) != 3:
                return jsonify({
                    "error": "Invalid bed data format",
                    "row": row
                }), 500

            dept, total, occupied = row
            utilization = (occupied / total) * 100 if total > 0 else 0

            if utilization > 85:
                rec = f"Add 5–10 beds (Critical: {utilization:.1f}%)"
            elif utilization > 70:
                rec = f"Consider adding 3–5 beds ({utilization:.1f}%)"
            elif utilization < 40:
                rec = f"Reallocate beds ({utilization:.1f}%)"
            else:
                rec = f"Optimal ({utilization:.1f}%)"

            recommendations.append({
                "department": dept,
                "total_beds": total,
                "occupied_beds": occupied,
                "available_beds": total - occupied,
                "utilization": round(utilization, 1),
                "recommendation": rec,
            })

        return jsonify(recommendations)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "error": "Bed allocation failed",
            "details": str(e)
        }), 500

# -----------------------------------------------------------------------------
# Overview API
# -----------------------------------------------------------------------------

@app.route("/api/overview/stats", methods=["GET"])
def api_overview_stats():
    bed_data = get_bed_allocation() or []

    total_beds = sum(total for _, total, _ in bed_data) if bed_data else 0
    occupied_beds = sum(occ for _, _, occ in bed_data) if bed_data else 0
    bed_occupancy = (occupied_beds / total_beds * 100) if total_beds else 0

    avg_wait_time = int(12 + (bed_occupancy / 100) * 28)
    avg_wait_time = max(10, min(45, avg_wait_time))

    staff_efficiency = int(78 + (1 - bed_occupancy / 100) * 14)
    staff_efficiency = max(72, min(95, staff_efficiency))

    patient_distribution = [
        {"department": dept, "count": count}
        for dept, count in get_patient_data()
    ]

    return jsonify({
        "total_patients": get_total_patients_today(),
        "avg_wait_time": avg_wait_time,
        "bed_occupancy": round(bed_occupancy, 1),
        "staff_efficiency": staff_efficiency,
        "patient_distribution": patient_distribution,
    })

# -----------------------------------------------------------------------------
# Surge APIs (endpoint-safe for Vercel)
# -----------------------------------------------------------------------------

@app.route(
    "/api/surge/events",
    methods=["GET"],
    endpoint="api_surge_events_v1"
)
def api_surge_events():
    return jsonify(predict_surge_events())


@app.route(
    "/api/surge/stats",
    methods=["GET"],
    endpoint="api_surge_stats_v1"
)
def api_surge_stats():
    stats = get_surge_statistics()
    stats["weather"] = get_weather_impact()
    return jsonify(stats)

# -----------------------------------------------------------------------------
# Resource Exchange APIs
# -----------------------------------------------------------------------------

@app.route("/api/resources/network", methods=["GET"])
def api_resource_network():
    return jsonify(get_hospital_network())


@app.route("/api/resources/available", methods=["GET"])
def api_resources_available():
    return jsonify(get_available_resources())


@app.route("/api/resources/mine", methods=["GET"])
def api_my_resources():
    return jsonify(get_my_shareable_resources())


@app.route("/api/resources/requests", methods=["GET"])
def api_resource_requests():
    return jsonify(get_resource_requests())

# -----------------------------------------------------------------------------
# Supply Chain APIs
# -----------------------------------------------------------------------------

@app.route("/api/supply/inventory", methods=["GET"])
def api_supply_inventory():
    return jsonify(get_supply_inventory())


@app.route("/api/supply/predictions", methods=["GET"])
def api_supply_predictions():
    return jsonify(get_supply_predictions())


@app.route("/api/supply/stats", methods=["GET"])
def api_supply_stats():
    return jsonify(get_supply_statistics())


@app.route("/api/supply/trend", methods=["GET"])
def api_supply_trend():
    return jsonify(get_usage_trend())

# -----------------------------------------------------------------------------
# Local Development Entry
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
