import random
import string
from datetime import datetime

def generate_order_number():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.digits, k=4))
    return f'APX-{timestamp}-{random_str}'

def generate_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
