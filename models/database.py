"""
Hospital database: uses fixed seed for reproducible, realistic data.
Serverless-safe (Vercel) and localhost-safe.
"""

import os
import sqlite3
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# Environment detection (RELIABLE)
# -----------------------------------------------------------------------------

IS_VERCEL = bool(os.environ.get("VERCEL_ENV") or os.environ.get("NOW_REGION"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DB_PATH = "/tmp/hospital.db" if IS_VERCEL else os.path.join(BASE_DIR, "hospital.db")

# Ensure directory exists (safe even if already exists)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# -----------------------------------------------------------------------------
# Fixed deterministic data
# -----------------------------------------------------------------------------

DEPARTMENTS_FIXED = [
    ("Emergency", 30, 24),
    ("Cardiology", 25, 18),
    ("Orthopedics", 20, 14),
    ("Pediatrics", 35, 26),
    ("General Medicine", 40, 31),
]

PATIENT_NAMES = [
    "John Doe", "Jane Smith", "Michael Brown", "Emily Davis", "Robert Wilson",
    "Sarah Johnson", "David Lee", "Lisa Anderson", "James Taylor", "Maria Garcia",
]

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def _deterministic_index(seed, i, mod):
    return (seed * 31 + i) % mod


def _connect():
    return sqlite3.connect(DB_PATH)


def ensure_db():
    """
    Ensure DB exists and is initialized.
    CRITICAL for Vercel serverless cold starts.
    """
    if not os.path.exists(DB_PATH):
        init_db()

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

def init_db():
    conn = _connect()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("DROP TABLE IF EXISTS departments")
    cursor.execute("DROP TABLE IF EXISTS beds")
    cursor.execute("DROP TABLE IF EXISTS staff")

    cursor.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_beds INTEGER,
            occupied_beds INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            admission_time TIMESTAMP,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE beds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            bed_number TEXT NOT NULL,
            status TEXT,
            patient_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT,
            shift TEXT
        )
    """)

    cursor.executemany(
        "INSERT INTO departments (name, total_beds, occupied_beds) VALUES (?, ?, ?)",
        DEPARTMENTS_FIXED,
    )

    dept_names = [d[0] for d in DEPARTMENTS_FIXED]
    now = datetime.now()

    for i in range(50):
        dept = dept_names[_deterministic_index(42, i, len(dept_names))]
        name = PATIENT_NAMES[_deterministic_index(7, i, len(PATIENT_NAMES))]
        admission = now - timedelta(hours=(6 + (i * 17) % 42))
        status = ["Admitted", "Under Treatment", "Recovery"][_deterministic_index(3, i, 3)]

        cursor.execute(
            "INSERT INTO patients (name, department, admission_time, status) VALUES (?, ?, ?, ?)",
            (name, dept, admission, status),
        )

    for dept_name, total, occupied in DEPARTMENTS_FIXED:
        for i in range(1, total + 1):
            bed_status = "Occupied" if i <= occupied else "Available"
            patient_id = i if bed_status == "Occupied" else None

            cursor.execute(
                "INSERT INTO beds (department, bed_number, status, patient_id) VALUES (?, ?, ?, ?)",
                (dept_name, f"{dept_name[:3].upper()}-{i:02d}", bed_status, patient_id),
            )

    staff_roles = ["Doctor", "Nurse", "Technician"]
    staff_shifts = ["Morning", "Evening", "Night"]

    for dept_name, _, _ in DEPARTMENTS_FIXED:
        for i in range(6):
            cursor.execute(
                "INSERT INTO staff (name, department, role, shift) VALUES (?, ?, ?, ?)",
                (
                    f"Staff-{dept_name[:3]}-{i}",
                    dept_name,
                    staff_roles[_deterministic_index(5, i, 3)],
                    staff_shifts[_deterministic_index(13, i, 3)],
                ),
            )

    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------
# Query Functions (ALL serverless-safe)
# -----------------------------------------------------------------------------

def get_patient_data():
    ensure_db()
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM patients GROUP BY department")
    data = cursor.fetchall()
    conn.close()
    return data


def get_department_data():
    ensure_db()
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, total_beds, occupied_beds FROM departments")
    data = cursor.fetchall()
    conn.close()
    return data


def get_bed_allocation():
    ensure_db()
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT department,
               COUNT(*) AS total_beds,
               SUM(CASE WHEN status = 'Occupied' THEN 1 ELSE 0 END)
        FROM beds
        GROUP BY department
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_total_patients_today():
    ensure_db()
    conn = _connect()
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute(
        "SELECT COUNT(*) FROM patients WHERE DATE(admission_time) = ?", (today,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_staff_count():
    ensure_db()
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM staff GROUP BY department")
    data = cursor.fetchall()
    conn.close()
    return data
# -----------------------------------------------------------------------------
# 🚨 EMERGENCY DEMO MODE (Vercel-safe)
# -----------------------------------------------------------------------------

if DEMO_MODE:

    def get_bed_allocation():
        return [
            ("Emergency", 30, 24),
            ("Cardiology", 25, 18),
            ("Orthopedics", 20, 14),
            ("Pediatrics", 35, 26),
            ("General Medicine", 40, 31),
        ]

    def get_patient_data():
        return [
            ("Emergency", 42),
            ("Cardiology", 31),
            ("Orthopedics", 28),
            ("Pediatrics", 36),
            ("General Medicine", 49),
        ]

    def get_department_data():
        return [
            ("Emergency", 30, 24),
            ("Cardiology", 25, 18),
            ("Orthopedics", 20, 14),
            ("Pediatrics", 35, 26),
            ("General Medicine", 40, 31),
        ]

    def get_total_patients_today():
        return 186

    def get_staff_count():
        return [
            ("Emergency", 18),
            ("Cardiology", 14),
            ("Orthopedics", 12),
            ("Pediatrics", 16),
            ("General Medicine", 20),
        ]
