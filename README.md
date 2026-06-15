# IT Asset Management System

A professional Flask web application for tracking IT equipment such as laptops, monitors, phones, and other company devices.

This project is designed for an IT support, help desk, systems administrator, or IT asset management portfolio.

## Features

- Asset inventory dashboard
- Add, edit, view, and delete assets
- Track asset tag, serial number, device type, brand, model, status, department, and location
- Check out assets to employees
- Check in returned assets
- Assignment and update history log
- Dashboard summary cards for total, available, assigned, maintenance, and retired assets
- Sample data route for demo use
- Bootstrap styling
- SQLite database for easy local setup

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- Bootstrap 5
- CSS

## Why This Project Is Strong for Your Resume

This project shows that you understand real IT department workflows, including:

- Asset lifecycle tracking
- Device assignment
- Inventory documentation
- Hardware accountability
- Status reporting
- Support operations

It connects directly to IT technician, help desk, asset management, and systems administration roles.

## How to Run the Project

### 1. Clone or download the project

```bash
cd asset_management_system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
python app.py
```

### 6. Open in browser

Go to:

```text
http://127.0.0.1:5000
```

### 7. Load sample data

Click **Load Sample Data** in the navbar, or visit:

```text
http://127.0.0.1:5000/seed
```

## Suggested GitHub README Screenshot Ideas

Add screenshots of:

- Dashboard
- Add asset form
- Asset detail page
- Check-out/check-in form
- Assignment history log

## Resume Bullet Points

You can add this to your resume:

- Built a Flask-based IT asset management system to track equipment inventory, device assignments, check-in/check-out history, and asset status reporting.
- Designed relational database models using SQLAlchemy to manage assets and audit logs for IT equipment lifecycle tracking.
- Created a Bootstrap dashboard with inventory metrics for available, assigned, maintenance, and retired assets.

## Future Improvements

- User login and admin roles
- Barcode or QR code generation
- CSV export
- Search and filtering
- Email alerts for overdue returns
- Cloud deployment on AWS EC2 or Render
- PostgreSQL database support
