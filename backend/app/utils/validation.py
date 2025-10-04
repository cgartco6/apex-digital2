import re
from datetime import datetime

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 8

def validate_phone(phone):
    # South African phone number validation
    pattern = r'^(\+27|0)[6-8][0-9]{8}$'
    return re.match(pattern, phone.replace(' ', '')) is not None

def validate_price(price):
    try:
        return float(price) > 0
    except (ValueError, TypeError):
        return False

def validate_date(date_string):
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except (ValueError, TypeError):
        return False
