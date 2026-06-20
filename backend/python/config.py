# ============================================================
# config.py  –  Database & App Configuration
# ============================================================
import os

DB_HOST = 'sql5.freesqldatabase.com'
DB_USER = 'sql5831052'
DB_PASSWORD = 'iJRRdBAter'
DB_NAME = 'sql5831052'
SECRET_KEY       = os.getenv('SECRET_KEY', 'lms-secret-key-change-in-production')
FINE_PER_DAY     = 2.00   # ₹ per overdue day
LOAN_DAYS        = 14     # default loan period
JWT_EXPIRY_HOURS = 8
