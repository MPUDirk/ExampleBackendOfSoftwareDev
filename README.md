#  The Backend Of Order Management System(OMS)

The back-end provides APIs for login, employee management, goods management and order placement systems.

## Folder Description

```
backend/
├─backend/
│   ├─settings.py       # Global Project Configuration
│   ├─urls.py           # Main routing configuration
│   └─wsgi.py           # WSGI Deployment Configuration
├─OMS/                  # Core Order Management Module
│   |─migrations/       # Database migration file
│   ├─views.py          # View Layer (Current File)
│   ├─models.py         # Data Model (Good/Order/OrderGood)
│   ├─forms.py          # Form Definition (such as OrderFrom)
│   └─urls.py           # Route Configuration (not shown but should exist)
├─omsAuth/              # Authentication Module
│   |─migrations/       # Migration of User-related databases
│   ├─models.py         # User Model (Presumed to include the Customer Model)
│   └─views.py          # Certification-related Views (not shown)
└─manage.py             # Django Project Management Script (Key Entry)

```

## Project Technology

Django

PyMySQL
