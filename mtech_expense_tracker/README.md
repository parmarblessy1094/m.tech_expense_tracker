# 🎓 M.Tech Expense Tracker

A production-ready Expense Management System built with Python & Streamlit.

## 📁 Project Structure

```
mtech_expense_tracker/
├── app.py                  ← Main entry point (run this)
├── requirements.txt        ← Python dependencies
├── seed_data.py            ← Load sample data for demo
├── database/
│   ├── __init__.py
│   └── db.py               ← All SQLite DB operations
├── pages/
│   ├── __init__.py
│   ├── dashboard.py        ← Dashboard with KPIs and charts
│   ├── add_expense.py      ← Add new expense form
│   ├── edit_expense.py     ← Edit/Delete expenses table
│   ├── summary.py          ← Payer+semester breakdown
│   ├── reports.py          ← Excel & PDF report generation
│   ├── printable.py        ← Printable HTML report
│   └── settings.py         ← Manage categories and payers
└── assets/
    ├── reports/            ← (auto-created for temp files)
    └── expenses.db         ← SQLite database (auto-created)
```

---

## 🚀 Setup & Run

### 1. Create Virtual Environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Load Sample Data

```bash
python seed_data.py
```

This loads 24 sample expenses across all 4 semesters so you can explore the app immediately.

### 4. Run the Application

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🌐 Deploying to Streamlit Community Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repo, branch, and set **Main file path** = `app.py`
5. Click **Deploy**

> ⚠️ The SQLite database (`assets/expenses.db`) resets when the container restarts on Streamlit Cloud. For persistent cloud storage, consider switching to PostgreSQL (Supabase free tier) or a hosted SQLite service.

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t mtech-tracker .
docker run -p 8501:8501 mtech-tracker
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 Dashboard | KPI cards, pie chart, bar charts, timeline, recent transactions |
| ➕ Add Expense | Date, semester, paid-by, category, description, amount with validation |
| ✏️ Edit/Delete | Searchable table with inline edit and delete confirmation |
| 📋 Summary | Grouped by payer → semester → expense with subtotals |
| 📁 Reports | Excel (.xlsx) and PDF (A4 professional) download |
| 🖨️ Print | Browser-print ready HTML report in iframe preview |
| ⚙️ Settings | Add/remove expense categories and paid-by names |

---

## 🎨 Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **SQLite** — Local database (zero config)
- **Pandas** — Data processing
- **Plotly** — Interactive charts
- **OpenPyXL** — Excel generation
- **ReportLab** — PDF generation

---

## 📝 License

Free to use for personal and educational purposes.
