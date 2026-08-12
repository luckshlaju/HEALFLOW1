# 🏥 HealFlow

### AI-Based Hospital Flow Optimization & Decision Support System

HealFlow is a hospital operations optimization platform designed to help administrators **predict patient demand, analyze queues, optimize resource utilization, and anticipate operational surges** through a centralized dashboard.

The system combines **patient inflow forecasting, queuing theory, resource allocation, surge prediction, and supply monitoring** to provide a unified view of hospital operations and support faster, data-driven administrative decisions.

> **HealFlow – Predict. Optimize. Care.**

---

## 🎯 Project Objective

Hospitals frequently face unpredictable patient inflow, long waiting times, uneven resource utilization, staff shortages, bed constraints, and supply issues.

HealFlow addresses these operational challenges by providing a centralized decision-support platform that can:

- Predict upcoming patient inflow
- Simulate patient queues and waiting times
- Monitor bed and staff utilization
- Recommend resource allocation
- Identify potential emergency surges
- Monitor hospital supply levels
- Enable resource sharing across hospitals
- Present operational insights through an administrative dashboard

The goal is to help hospital administrators **anticipate operational pressure instead of reacting to it after it occurs**.

---

## ✨ Key Features

### 📈 Patient Inflow Prediction

Forecasts expected patient arrivals for the upcoming days based on:

- Day of the week
- Department
- Historical/deterministic patterns

The forecasting layer is modular and can be replaced with a trained machine learning model when real hospital datasets become available.

### 🚶 Queue & Waiting-Time Simulation

Uses **M/M/c queuing theory** to simulate patient flow through hospital departments.

The system considers:

- Arrival rate
- Service rate
- Number of available servers
- Resource utilization
- Expected waiting time
- Queue length

This allows administrators to experiment with different staffing and capacity scenarios.

### 🛏️ Bed & Staff Optimization

Provides department-level visibility into:

- Bed occupancy
- Available capacity
- Resource utilization
- Staff requirements
- Allocation recommendations

This helps identify departments approaching capacity and areas where resources may be reallocated.

### 🚨 Emergency Surge Prediction

Models potential increases in patient demand using factors such as:

- Special events
- Weather conditions
- Department-specific demand
- Surge scenarios

The feature is intended to help administrators prepare resources before demand increases.

### 🔄 Hospital Resource Exchange

Provides a conceptual framework for sharing available resources across hospitals within a network.

Potential resources include:

- Beds
- Staff
- Medical supplies
- Other operational resources

This can help reduce situations where one facility is overloaded while another has unused capacity.

### 📦 Supply Chain Monitoring

Tracks hospital inventory and provides insights into:

- Current stock levels
- Usage trends
- Potential shortages
- Supply requirements

This enables administrators to identify supply risks before they become operational problems.

### 📊 Administrative Dashboard

A centralized dashboard provides an overview of hospital operations through:

- KPI cards
- Forecast charts
- Queue analytics
- Bed utilization
- Staff/resource information
- Surge indicators
- Supply information
- Department-level insights

The dashboard is designed for hospital administrators rather than patients.

---

## 🧠 System Architecture

HealFlow follows a modular architecture:

```text
                    ┌─────────────────────┐
                    │   Admin Dashboard   │
                    │ HTML / CSS / JS     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Flask API       │
                    │  Application Layer  │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │ Patient Inflow │   │ Queue Simulator│   │ Resource Engine│
 │   Prediction   │   │    M/M/c       │   │ Beds & Staff   │
 └────────────────┘   └────────────────┘   └────────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Operational Modules │
                    │ Surge & Supply Data │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ SQLite / Prototype  │
                    │       Data          │
                    └─────────────────────┘
````

The architecture is intentionally modular so that prototype components can later be replaced with production-grade services and real hospital data sources.

---

## 🛠️ Technologies Used

| Technology                  | Purpose                                 |
| --------------------------- | --------------------------------------- |
| **Python**                  | Backend logic and analytical models     |
| **Flask**                   | Web application and REST API            |
| **Machine Learning**        | Patient inflow prediction architecture  |
| **Queuing Theory**          | M/M/c queue and waiting-time simulation |
| **SQLite**                  | Prototype data storage                  |
| **HTML / CSS / JavaScript** | Administrative dashboard                |
| **Plotly**                  | Interactive data visualization          |
| **Chart.js**                | Dashboard charts                        |
| **Git / GitHub**            | Version control                         |
| **Vercel**                  | Web deployment                          |

---

## 📁 Repository Structure

```text
HealFlow/
│
├── app.py                    # Local application entry point
│
├── api/
│   └── app.py                # Flask application and API routes
│
├── models/
│   ├── database.py           # Database operations
│   ├── inflow.py             # Patient inflow prediction
│   ├── queue.py              # Queue simulation
│   ├── surge.py              # Emergency surge prediction
│   ├── supply.py             # Supply chain analytics
│   └── resources.py          # Bed/staff/resource management
│
├── static/
│   ├── css/                  # Dashboard styles
│   └── js/                   # Frontend logic and charts
│
├── templates/
│   ├── base.html
│   ├── layout_dashboard.html
│   ├── partials/
│   └── pages/
│
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel configuration
├── README.md
└── .gitignore
```

---

## 🔄 How HealFlow Works

The system follows a simple operational workflow:

```text
Hospital Data
     │
     ▼
Patient Demand Analysis
     │
     ▼
Inflow Prediction
     │
     ▼
Queue Simulation
     │
     ▼
Resource Analysis
     │
     ├── Beds
     ├── Doctors
     ├── Nurses
     └── Supplies
     │
     ▼
Surge Detection
     │
     ▼
Administrative Recommendations
     │
     ▼
Dashboard Visualization
```

This allows different operational factors to be considered together rather than analyzing patient flow, staffing, beds, and supplies independently.

---

## 📊 Current Prototype Capabilities

The current prototype includes:

* 7-day patient inflow forecasting
* Department-based demand analysis
* M/M/c queue simulation
* Arrival and service-rate configuration
* Waiting-time estimation
* Queue utilization analysis
* Department-wise bed utilization
* Staff/resource recommendations
* Emergency surge scenarios
* Event and weather-based surge factors
* Hospital resource exchange concept
* Supply inventory monitoring
* Shortage prediction
* Usage trend visualization
* Administrative dashboard
* Responsive dashboard interface
* Modular Flask API
* SQLite-based prototype data layer

The prototype currently uses **deterministic/simulated data** for demonstration rather than live hospital data.

---

## 🚀 Running HealFlow Locally

### 1. Clone the repository

```bash
git clone https://github.com/luckshlaju/HealFlow.git
cd HealFlow
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
python app.py
```

Alternatively:

```bash
python api/app.py
```

### 6. Open the application

```text
http://localhost:5000
```

---

## ☁️ Deployment

HealFlow is structured to support cloud deployment and is currently configured for **Vercel**.

The application separates the frontend presentation layer from the Flask API and analytical modules, making it easier to migrate individual components to scalable cloud services in future versions.

---

## 🔮 Future Enhancements

The prototype can be extended into a production-grade hospital decision-support platform through:

### Real Hospital Data

* Integration with hospital databases
* EHR/EMR integration
* OPD and emergency department data
* Real-time patient arrival streams
* Historical patient datasets

### Advanced Machine Learning

* Time-series forecasting
* Department-specific demand models
* Seasonal demand prediction
* Anomaly detection
* Predictive emergency surge models
* Model retraining using historical hospital data

### Intelligent Workforce Management

* Dynamic doctor scheduling
* Nurse scheduling
* Shift optimization
* Workload balancing
* Skill-based staff allocation

### Advanced Patient Flow

* Emergency prioritization
* Fast-track queue management
* Appointment optimization
* Dynamic queue routing
* Bottleneck detection

### Multi-Hospital Intelligence

* Hospital network analytics
* Cross-hospital resource allocation
* Bed availability sharing
* Supply redistribution
* Regional demand forecasting

### Real-Time Operations

* Live hospital dashboards
* Automated alerts
* Staff notifications
* Capacity threshold warnings
* Supply shortage alerts

---

## ⚠️ Prototype Disclaimer

HealFlow is a **prototype and decision-support concept** intended for demonstration and research purposes.

The current system uses simulated/deterministic data and should **not be used for real clinical decisions, patient diagnosis, treatment decisions, emergency prioritization, or resource allocation in a real hospital environment**.

A production deployment would require validated clinical models, real-world datasets, security controls, privacy protection, regulatory compliance, extensive testing, and validation by qualified healthcare professionals.

---

## 🌍 Potential Impact

If developed with validated real-world hospital data, HealFlow could help organizations:

* Reduce patient waiting times
* Identify operational bottlenecks
* Improve bed utilization
* Balance staff workloads
* Anticipate patient surges
* Reduce resource wastage
* Detect potential supply shortages
* Improve hospital-wide operational visibility
* Support faster administrative decision-making

The long-term vision is to transform hospital operations from a **reactive workflow into a predictive and optimization-driven system**.

---

## 👨‍💻 Author

**Luckshvadhan B**

Information Technology Student

---

## 🏷️ Project Tagline

**HealFlow – Predict. Optimize. Care.**

```
```
