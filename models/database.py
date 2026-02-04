"""
Hospital database: uses fixed seed for reproducible, realistic data.
When real data is available, replace init_db() with CSV/API load and keep get_* as-is.
"""
import sqlite3
from datetime import datetime, timedelta

DATABASE = '/tmp/hospital.db'

# Fixed seed-like values for reproducible data (no random)
DEPARTMENTS_FIXED = [
    ('Emergency', 30, 24),
    ('Cardiology', 25, 18),
    ('Orthopedics', 20, 14),
    ('Pediatrics', 35, 26),
    ('General Medicine', 40, 31),
]

PATIENT_NAMES = [
    'John Doe', 'Jane Smith', 'Michael Brown', 'Emily Davis', 'Robert Wilson',
    'Sarah Johnson', 'David Lee', 'Lisa Anderson', 'James Taylor', 'Maria Garcia',
]


def _deterministic_index(seed, i, mod):
    """Deterministic 'random' for reproducibility."""
    return (seed * 31 + i) % mod


def init_db():
    """Initialize the database with realistic, reproducible data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS patients')
    cursor.execute('DROP TABLE IF EXISTS departments')
    cursor.execute('DROP TABLE IF EXISTS beds')
    cursor.execute('DROP TABLE IF EXISTS staff')

    cursor.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_beds INTEGER,
            occupied_beds INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            admission_time TIMESTAMP,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE beds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            bed_number TEXT NOT NULL,
            status TEXT,
            patient_id INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT,
            shift TEXT
        )
    ''')

    cursor.executemany(
        'INSERT INTO departments (name, total_beds, occupied_beds) VALUES (?, ?, ?)',
        DEPARTMENTS_FIXED
    )

    dept_names = [d[0] for d in DEPARTMENTS_FIXED]
    now = datetime.now()
    for i in range(50):
        dept_idx = _deterministic_index(42, i, len(dept_names))
        dept = dept_names[dept_idx]
        name_idx = _deterministic_index(7, i, len(PATIENT_NAMES))
        name = PATIENT_NAMES[name_idx]
        hours_ago = 6 + (i * 17) % 42
        admission = now - timedelta(hours=hours_ago)
        status_idx = _deterministic_index(3, i, 3)
        status = ['Admitted', 'Under Treatment', 'Recovery'][status_idx]
        cursor.execute(
            'INSERT INTO patients (name, department, admission_time, status) VALUES (?, ?, ?, ?)',
            (name, dept, admission, status)
        )

    for dept_name, total, occupied in DEPARTMENTS_FIXED:
        for i in range(1, total + 1):
            bed_status = 'Occupied' if i <= occupied else 'Available'
            patient_id = (i + _deterministic_index(11, ord(dept_name[0]), 50)) % 51 if bed_status == 'Occupied' else None
            if patient_id == 0:
                patient_id = 1
            cursor.execute(
                'INSERT INTO beds (department, bed_number, status, patient_id) VALUES (?, ?, ?, ?)',
                (dept_name, f'{dept_name[:3].upper()}-{i:02d}', bed_status, patient_id)
            )

    staff_roles = ['Doctor', 'Nurse', 'Technician']
    staff_shifts = ['Morning', 'Evening', 'Night']
    for dept_name, _, _ in DEPARTMENTS_FIXED:
        n_staff = 6 + (hash(dept_name) % 3)
        for i in range(n_staff):
            role = staff_roles[_deterministic_index(5, i, 3)]
            shift = staff_shifts[_deterministic_index(13, i, 3)]
            cursor.execute(
                'INSERT INTO staff (name, department, role, shift) VALUES (?, ?, ?, ?)',
                (f'Staff-{100 + hash(dept_name) % 900 + i}', dept_name, role, shift)
            )

    conn.commit()
    conn.close()


def get_patient_data():
    """Get patient count by department."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM patients GROUP BY department")
    data = cursor.fetchall()
    conn.close()
    return data


def get_department_data():
    """Get all department information."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, total_beds, occupied_beds FROM departments")
    data = cursor.fetchall()
    conn.close()
    return data


def get_bed_allocation():
    """Get bed allocation details."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT department,
               COUNT(*) as total_beds,
               SUM(CASE WHEN status = 'Occupied' THEN 1 ELSE 0 END) as occupied_beds
        FROM beds
        GROUP BY department
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_total_patients_today():
    """Get total patients admitted today."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(admission_time) = ?", (today,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_staff_count():
    """Get staff count by department."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM staff GROUP BY department")
    data = cursor.fetchall()
    conn.close()
    return data
