import sys
import os

# Ensure project root is on Python path (Vercel fix)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, jsonify, request



from models.database import (
    init_db,
    get_patient_data,
    get_department_data,
    get_bed_allocation,
    get_total_patients_today,
    get_staff_count,
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

BASE_DIR = os.path.dirname(__file__)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../templates"),
    static_folder=os.path.join(BASE_DIR, "../static"),
)

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret")

# Initialize DB safely (Vercel-safe: init_db is no-op when FORCE_DEMO)
if not os.path.exists("/tmp/hospital.db"):
    init_db()

@app.route("/health")
def health():
    return "OK", 200

# -------------------- PAGES --------------------

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

# -------------------- API --------------------

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    dept = data.get("department", "Emergency")
    return jsonify({
        "department": dept,
        "dates": get_prediction_dates(),
        "predictions": predict_patient_inflow(dept),
    })

@app.route("/api/predict/all")
def api_predict_all():
    return jsonify({
        "dates": get_prediction_dates(),
        "predictions": get_all_departments_prediction(),
    })

@app.route("/api/queue/simulate", methods=["POST"])
def api_queue_sim():
    data = request.get_json()
    ar = float(data.get("arrival_rate", 20))
    sr = float(data.get("service_rate", 5))
    s = int(data.get("servers", 3))
    result = mmc_queue_simulation(ar, sr, s)
    result["prob_no_wait"] = calculate_probability_no_wait(ar, sr, s)
    return jsonify(result)

@app.route("/api/beds/allocate")
def api_beds_allocate():
    output = []
    for dept, total, occupied in get_bed_allocation():
        util = (occupied / total) * 100 if total else 0
        output.append({
            "department": dept,
            "total_beds": total,
            "occupied_beds": occupied,
            "available_beds": total - occupied,
            "utilization": round(util, 1),
        })
    return jsonify(output)

@app.route("/api/overview/stats")
def api_overview():
    beds = get_bed_allocation()
    total = sum(t for _, t, _ in beds)
    occ = sum(o for _, _, o in beds)
    occupancy = (occ / total * 100) if total else 0

    return jsonify({
        "total_patients": get_total_patients_today(),
        "bed_occupancy": round(occupancy, 1),
        "staff_efficiency": max(70, min(95, int(90 - occupancy / 5))),
        "patient_distribution": [
            {"department": d, "count": c} for d, c in get_patient_data()
        ],
    })

@app.route("/api/surge/events")
def api_surge_events():
    return jsonify(predict_surge_events())

@app.route("/api/surge/stats")
def api_surge_stats():
    stats = get_surge_statistics()
    stats["weather"] = get_weather_impact()
    return jsonify(stats)
