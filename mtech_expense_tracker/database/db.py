import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "expenses.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            semester TEXT NOT NULL,
            paid_by TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS paid_by (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    default_categories = [
        "Registration Fees", "Admission Fees", "Tuition Fees",
        "Exam Fees", "Hostel Fees", "Books", "Travel", "Other"
    ]
    default_paid_by = ["Self", "Jayanti Mama", "Mother", "Other"]

    for cat in default_categories:
        cur.execute("INSERT OR IGNORE INTO categories (category_name) VALUES (?)", (cat,))
    for person in default_paid_by:
        cur.execute("INSERT OR IGNORE INTO paid_by (name) VALUES (?)", (person,))

    conn.commit()
    conn.close()


# ── Expense CRUD ──────────────────────────────────────────────────────────────

def add_expense(date, semester, paid_by, category, description, amount):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (date, semester, paid_by, category, description, amount) VALUES (?,?,?,?,?,?)",
        (date, semester, paid_by, category, description, amount)
    )
    conn.commit()
    conn.close()


def get_all_expenses(semester=None, paid_by=None, search=None):
    conn = get_connection()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if semester and semester != "All":
        query += " AND semester = ?"
        params.append(semester)
    if paid_by and paid_by != "All":
        query += " AND paid_by = ?"
        params.append(paid_by)
    if search:
        query += " AND (description LIKE ? OR category LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    query += " ORDER BY date DESC, id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_expense_by_id(expense_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id=?", (expense_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_expense(expense_id, date, semester, paid_by, category, description, amount):
    conn = get_connection()
    conn.execute(
        "UPDATE expenses SET date=?, semester=?, paid_by=?, category=?, description=?, amount=? WHERE id=?",
        (date, semester, paid_by, category, description, amount, expense_id)
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


# ── Aggregates ────────────────────────────────────────────────────────────────

def get_summary():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY paid_by, semester, description", conn)
    conn.close()
    return df


def get_total():
    conn = get_connection()
    row = conn.execute("SELECT COALESCE(SUM(amount),0) as total FROM expenses").fetchone()
    conn.close()
    return row["total"]


def get_semester_totals():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT semester, COALESCE(SUM(amount),0) as total FROM expenses GROUP BY semester ORDER BY semester",
        conn
    )
    conn.close()
    return df


def get_paid_by_totals():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT paid_by, COALESCE(SUM(amount),0) as total FROM expenses GROUP BY paid_by ORDER BY total DESC",
        conn
    )
    conn.close()
    return df


def get_category_totals():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT category, COALESCE(SUM(amount),0) as total FROM expenses GROUP BY category ORDER BY total DESC",
        conn
    )
    conn.close()
    return df


# ── Settings ──────────────────────────────────────────────────────────────────

def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT category_name FROM categories ORDER BY category_name").fetchall()
    conn.close()
    return [r["category_name"] for r in rows]


def add_category(name):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO categories (category_name) VALUES (?)", (name,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def delete_category(name):
    conn = get_connection()
    conn.execute("DELETE FROM categories WHERE category_name=?", (name,))
    conn.commit()
    conn.close()


def get_paid_by_names():
    conn = get_connection()
    rows = conn.execute("SELECT name FROM paid_by ORDER BY name").fetchall()
    conn.close()
    return [r["name"] for r in rows]


def add_paid_by(name):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO paid_by (name) VALUES (?)", (name,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def delete_paid_by(name):
    conn = get_connection()
    conn.execute("DELETE FROM paid_by WHERE name=?", (name,))
    conn.commit()
    conn.close()
