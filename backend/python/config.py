# ============================================================
# config.py  –  Database & App Configuration
# ============================================================
import os

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Ganesh@9642'
DB_NAME = 'library_management'
SECRET_KEY       = os.getenv('SECRET_KEY', 'lms-secret-key-change-in-production')
FINE_PER_DAY     = 2.00   # ₹ per overdue day
LOAN_DAYS        = 14     # default loan period
JWT_EXPIRY_HOURS = 8
