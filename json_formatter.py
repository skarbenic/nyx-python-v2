import json
import os
from datetime import datetime 
import pytz

def log_to_json(log_data, log_file='log.json'):
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(pytz.utc).astimezone(utc_plus_7)
    formatted_time = current_time.strftime('%d-%m-%Y, %H:%M:%S')
    
    log_entry = {
        'timestamp': formatted_time,
        'log': log_data
    }
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            data = json.load(file)
            data.append(log_entry)
    else:
        data = [log_entry]
    
    with open(log_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f'Logged data: {log_entry}')

