# HealFlow – AI-Based Hospital Flow Optimization System


---

## Project Objective

To design and develop an AI-driven hospital flow optimization system that predicts patient inflow, simulates hospital queues, and optimizes critical resources such as doctors, nurses, and beds. The system aims to reduce patient waiting time, improve staff efficiency, and enable data-driven decision-making through a real-time administrative dashboard.

## Technologies Used

- **Python** – Backend logic and models  
- **Flask** – Web application and REST API  
- **Machine learning** – Patient inflow prediction (deterministic patterns; ready for ML model swap)  
- **Queuing theory (M/M/c)** – Queue and waiting-time simulation  
- **HTML, CSS, JavaScript** – Admin dashboard  
- **Plotly & Chart.js** – Data visualization  
- **Git & GitHub** – Version control  

## Architecture Overview

HealFlow uses a modular structure:

- **Backend:** Flask API for predictions, queue simulation, bed allocation, surge and supply data  
- **Frontend:** Admin dashboard with shared layout, sidebar navigation, and responsive UI  
- **Data layer:** SQLite for departments, patients, beds, staff; deterministic datasets for prototype  
- **Deployment:** Web app (e.g. Vercel); structure supports future cloud and mobile use  

## Repository Structure

```
├── app.py              # Flask app and API routes
├── models/             # Data and logic (database, inflow, queue, surge, supply, resources)
├── static/             # CSS and JS
├── templates/          # HTML (base, layout_dashboard, partials, page templates)
├── requirements.txt
├── README.md
└── .gitignore
```

## Current Scope (Prototype)

- **Patient inflow prediction** – Day-of-week and department-based forecasts (next 7 days)  
- **Queue simulation (M/M/c)** – Configurable arrival/service rates and servers; utilization and wait times  
- **Bed & staff allocation** – Department-wise bed utilization and recommendations  
- **Emergency surge predictor** – Event-based surge and weather impact  
- **Resource exchange** – Hospital network and shareable resources  
- **Supply chain** – Inventory, shortage predictions, usage trends  
- **Real-time dashboard** – Overview, charts with fixed heights, deterministic data  
- **Prototype disclaimer** – Shown in UI where applicable  

## How to Run Locally

1. Clone the repository and go to the project folder:
   ```bash
   git clone https://github.com/luckshlaju/HealFlow.git
   cd HealFlow
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open **http://localhost:5000** in your browser.

## Future Enhancements

- Integration with live hospital databases and EHR/OPD systems  
- ML-based inflow models trained on real historical data  
- Dynamic doctor and nurse scheduling  
- Emergency prioritization and fast-track queues  
- Multi-hospital analytics and mobile alerts for staff  
- Full-scale deployment as a hospital decision support system  

## Impact

- Reduced patient waiting time in OPD and emergency units  
- Better utilization of doctors, nurses, and beds  
- Improved planning through predictive analytics  
- Clearer, data-driven decisions for hospital administrators  

## Authors

 **Luckshvadhan B** 

 **Harikishanth R**

 **Mohamed Mubashir**

 **Mohamed Ashiq Omar**

 **Naveen Raj** 

 (Information Technology Students)

**Team CheatCode** – HackElite DNS'26

---

*HealFlow – Predict. Optimize. Care.*
