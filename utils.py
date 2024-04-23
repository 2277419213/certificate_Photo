import time
import random

def generate_unique_id():
    timestamp = int(time.time())
    random_part = random.randint(1000, 9999)
    unique_id = f"{timestamp}_{random_part}"
    return unique_id
