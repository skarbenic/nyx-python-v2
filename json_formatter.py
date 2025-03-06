import json
import os
from datetime import datetime 
import pytz

def log_to_json(log_data, log_file='log.json'):
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(pytz.utc).astimezone(utc_plus_7)
    formatted_time = current_time.strftime('%d-%m-%Y, %H:%M:%S.%f')[:-3]
    
    log_entry = {
        'message_received': formatted_time,
        'log': log_data
    }
    
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        try:
            with open(log_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except (json.JSONDecodeError, ValueError):
            data = []
    else:
        data = []
    data.append(log_entry)
    
    with open(log_file, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'Logged data: {log_entry}')

