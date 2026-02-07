import os
import json
import pandas as pd
from src.config import DATA_DIR
from src.db import get_engine

# --- EXTRACTION FUNCTIONS ---

def extract_aggregated_transaction():
    path = os.path.join(DATA_DIR, 'aggregated/transaction/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['transactionData']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'transaction_type': i['name'],
                            'transaction_count': i['paymentInstruments'][0]['count'],
                            'transaction_amount': i['paymentInstruments'][0]['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_aggregated_user():
    path = os.path.join(DATA_DIR, 'aggregated/user/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    data_list.append({
                        'state': state.replace('-', ' ').title(),
                        'year': int(year),
                        'quarter': int(file.strip('.json')),
                        'registered_users': data['data']['aggregated']['registeredUsers'],
                        'app_opens': data['data']['aggregated']['appOpens']
                    })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_aggregated_insurance():
    path = os.path.join(DATA_DIR, 'aggregated/insurance/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['transactionData']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'insurance_type': i['name'],
                            'insurance_count': i['paymentInstruments'][0]['count'],
                            'insurance_amount': i['paymentInstruments'][0]['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_aggregated_user_device():
    path = os.path.join(DATA_DIR, 'aggregated/user/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    if data['data']['usersByDevice']:
                        for i in data['data']['usersByDevice']:
                            data_list.append({
                                'state': state.replace('-', ' ').title(),
                                'year': int(year),
                                'quarter': int(file.strip('.json')),
                                'brand': i['brand'],
                                'count': i['count'],
                                'percentage': i['percentage']
                            })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_map_transaction():
    path = os.path.join(DATA_DIR, 'map/transaction/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['hoverDataList']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'district': i['name'].replace('district', '').strip().title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'total_transactions': i['metric'][0]['count'],
                            'total_amount': i['metric'][0]['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_map_user():
    path = os.path.join(DATA_DIR, 'map/user/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for district, metrics in data['data']['hoverData'].items():
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'district': district.replace('district', '').strip().title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'registered_users': metrics['registeredUsers'],
                            'app_opens': metrics['appOpens']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_map_insurance():
    path = os.path.join(DATA_DIR, 'map/insurance/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['hoverDataList']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'district': i['name'].replace('district', '').strip().title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'insurance_count': i['metric'][0]['count'],
                            'insurance_amount': i['metric'][0]['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_top_transaction():
    path = os.path.join(DATA_DIR, 'top/transaction/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    # Top Pincodes
                    for i in data['data']['pincodes']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'pincode': i['entityName'],
                            'transaction_count': i['metric']['count'],
                            'transaction_amount': i['metric']['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_top_user():
    path = os.path.join(DATA_DIR, 'top/user/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['pincodes']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'pincode': i['name'],
                            'registered_users': i['registeredUsers']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

def extract_top_insurance():
    path = os.path.join(DATA_DIR, 'top/insurance/country/india/state/')
    if not os.path.exists(path): return pd.DataFrame()
    states = os.listdir(path)
    data_list = []
    
    for state in states:
        cur_state = os.path.join(path, state)
        if not os.path.isdir(cur_state): continue
        for year in os.listdir(cur_state):
            cur_year = os.path.join(cur_state, year)
            if not os.path.isdir(cur_year): continue
            for file in os.listdir(cur_year):
                if not file.endswith('.json'): continue
                with open(os.path.join(cur_year, file), 'r') as f:
                    data = json.load(f)
                
                try:
                    for i in data['data']['pincodes']:
                        data_list.append({
                            'state': state.replace('-', ' ').title(),
                            'year': int(year),
                            'quarter': int(file.strip('.json')),
                            'pincode': i['entityName'],
                            'insurance_count': i['metric']['count'],
                            'insurance_amount': i['metric']['amount']
                        })
                except: pass
    return pd.DataFrame(data_list) if data_list else pd.DataFrame()

# --- LOADING FUNCTION ---

def load_data_to_sql():
    engine = get_engine()
    if not engine:
        print("Failed to get database engine.")
        return

    tasks = [
        (extract_aggregated_transaction, 'aggregated_transaction', "Aggregated Transaction"),
        (extract_aggregated_user, 'aggregated_user', "Aggregated User"),
        (extract_aggregated_insurance, 'aggregated_insurance', "Aggregated Insurance"),
        (extract_aggregated_user_device, 'aggregated_user_device', "User Devices"),
        (extract_map_transaction, 'map_map', "Map Transaction (map_map)"),
        (extract_map_user, 'map_user', "Map User"),
        (extract_map_insurance, 'map_insurance', "Map Insurance"),
        (extract_top_transaction, 'top_map', "Top Transaction (top_map)"),
        (extract_top_user, 'top_user', "Top User"),
        (extract_top_insurance, 'top_insurance', "Top Insurance"),
    ]

    for extract_func, table_name, desc in tasks:
        print(f"Loading {desc}...")
        try:
            df = extract_func()
            if not df.empty:
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                print(f"Successfully loaded {len(df)} rows to {table_name}")
            else:
                print(f"No data found for {desc}")
        except Exception as e:
            print(f"Error processing {desc}: {e}")

    print("ETL Process Complete.")

if __name__ == "__main__":
    load_data_to_sql()
