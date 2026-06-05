"""
seed_data.py — Populates the database with sample M.Tech expenses for demo/testing.
Run: python seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database.db import init_db, add_expense

SAMPLE_EXPENSES = [
    # Sem 1
    ("2023-07-15", "Sem 1", "Jayanti Mama", "Registration Fees", "Adit Registration Fees",    1000),
    ("2023-07-20", "Sem 1", "Jayanti Mama", "Registration Fees", "CVM Registration Fees",    20000),
    ("2023-08-01", "Sem 1", "Jayanti Mama", "Tuition Fees",      "College Tuition Fees",     58275),
    ("2023-08-05", "Sem 1", "Self",          "Hostel Fees",       "Hostel Deposit",            5000),
    ("2023-08-10", "Sem 1", "Father",        "Books",             "Semester 1 Books",          3200),
    ("2023-09-01", "Sem 1", "Self",          "Travel",            "Ahmedabad to College",      1800),
    ("2023-10-15", "Sem 1", "Mother",        "Exam Fees",         "Mid Semester Exam Fees",    2500),

    # Sem 2
    ("2024-01-10", "Sem 2", "Jayanti Mama",  "Tuition Fees",      "Sem 2 Tuition Fees",       55000),
    ("2024-01-15", "Sem 2", "Father",        "Hostel Fees",       "Sem 2 Hostel Charges",     18000),
    ("2024-02-05", "Sem 2", "Self",          "Books",             "Reference Books Sem 2",     4500),
    ("2024-02-20", "Sem 2", "Self",          "Exam Fees",         "University Exam Fees",      3000),
    ("2024-03-10", "Sem 2", "Mother",        "Travel",            "Travel Home During Break",  2200),
    ("2024-03-25", "Sem 2", "Jayanti Mama",  "Other",             "Lab Equipment Charges",     8000),

    # Sem 3
    ("2024-07-12", "Sem 3", "Father",        "Tuition Fees",      "Sem 3 Tuition Fees",       55000),
    ("2024-07-20", "Sem 3", "Father",        "Hostel Fees",       "Sem 3 Hostel",             18000),
    ("2024-08-10", "Sem 3", "Self",          "Books",             "Project Reference Books",   2800),
    ("2024-09-01", "Sem 3", "Jayanti Mama",  "Exam Fees",         "Theory Exam Fees Sem 3",   3500),
    ("2024-10-15", "Sem 3", "Self",          "Travel",            "Conference Travel",         5000),

    # Sem 4
    ("2025-01-08", "Sem 4", "Father",        "Tuition Fees",      "Final Sem Tuition",        55000),
    ("2025-01-15", "Sem 4", "Father",        "Exam Fees",         "Final Thesis Exam",         5000),
    ("2025-02-01", "Sem 4", "Self",          "Other",             "Thesis Printing & Binding", 3500),
    ("2025-03-01", "Sem 4", "Jayanti Mama",  "Other",             "Convocation Fees",         12000),
    ("2025-03-15", "Sem 4", "Self",          "Travel",            "Final Semester Travel",     2000),
]

if __name__ == "__main__":
    init_db()
    for exp in SAMPLE_EXPENSES:
        add_expense(*exp)
    print(f"✅ Seeded {len(SAMPLE_EXPENSES)} expenses successfully!")
