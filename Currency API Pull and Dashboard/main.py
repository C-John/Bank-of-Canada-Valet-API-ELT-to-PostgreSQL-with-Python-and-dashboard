# # datasource:
# "Data provided by the Bank of Canada."
	
# 	https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json

# 	https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/

# 	https://www.bankofcanada.ca/valet/

#   https://www.bankofcanada.ca/terms/


# # This Python Project. Copyright (c) 2026 Calder Henry. All rights reserved

# import getpass
import requests
import psycopg
import sys
import json
import subprocess
import os


# Connect to PostgreSQL
def get_connection():

    # # Manually prompt for username
    # db_username = input("Enter Username: ")
    # # Manually prompt for the password
    # db_password = getpass.getpass("Enter Password: ")
# Use environment variables instead of manual prompts
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    try:
        db_connect = psycopg.connect(
            host="db",
            dbname=db_name,
            user = db_user,
            password = db_password,
            port="5432"
        )
        
        # Create a cursor to execute commands
        db_cursor = db_connect.cursor()
        
        # Execute a simple query to check the version
        db_cursor.execute("SELECT version();")
        record = db_cursor.fetchone()
        
        print(f"Connection successful! You are connected to: {record}")
        return db_connect

    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None
pass

def execute_sql_file(db_connect, filename):
    # Run PostgreSQL script
    with db_connect.cursor() as db_cursor:
        with open(filename, 'r') as sql_file:
            # Using read().split(';') can sometimes struggle with complex scripts
            # but for your current structure, just ensure we strip whitespace
            full_script = sql_file.read()
            for command in full_script.split(';'):
                clean_command = command.strip()
                if clean_command: # Only execute if not empty
                    db_cursor.execute(clean_command)
        db_connect.commit()
    print(f"Finished executing: {filename}")

def load_rates(db_connect):

    # Dynamically finding the currency serise ids from the Bank of Canada Valet API
    # and pulling each one (currenly 26 of them) from their own API

    # Finished tables for the transformation schema
    # The list of tables we expect to see for a complete setup
    required_tables = ['raw_valet_data', 'series_metadata', 'calendar', 'observations']
  
    try:
        data = requests.get("https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json").json()
        with db_connect.cursor() as db_cursor:
            
            # Pulling what tables are in the database
            db_cursor.execute("""SELECT table_name 
                                FROM information_schema.tables 
                                WHERE table_schema = 'public';""")
            tables_in_db = [row[0] for row in db_cursor.fetchall()]

            are_all_tables_present = True
            
            # Checking if all required tables exist
            for table_name in required_tables:
                if table_name not in tables_in_db:
                    are_all_tables_present = False
                    break
            
            if are_all_tables_present is False:
        
                print("Missing tables detected. Creating missing structures...")
                # 1. Ensure the staging table exists (just in case it's the one missing)
                # with db_connect.cursor() as db_cursor:
                db_cursor.execute("CREATE TABLE IF NOT EXISTS currency_db_elt.public.raw_valet_data (raw_content JSONB);")
                
                # # 1. Clean Up Phase
                # drop 'raw_valet_data', 'series_metadata', 'calendar', 'observations'
                # then create 'raw_valet_data' again
                # execute_sql_file(db_connect, 'Clean Up.sql')
            else:
                print("All tables present. Appending new data...")
                # clear staging table
                db_cursor.execute("TRUNCATE TABLE currency_db_elt.public.raw_valet_data;")

            # 2. Python Load Phase
            for series_id in list(data['seriesDetail'].keys()):
                with requests.get(f"https://www.bankofcanada.ca/valet/observations/{series_id}/json") as response:
                    with db_cursor.copy("COPY raw_valet_data (raw_content) FROM STDIN") as copy:
                        json_string = json.dumps(response.json())
                        copy.write(json_string)
                        print('Complete upload: '+ series_id)
                    db_connect.commit()

            # 3. Transformation Phase
            execute_sql_file(db_connect, 'Transform SQL Queries.sql')
            return True
    except Exception as error:
        print(f"Error connecting to Valet API: {error}")
        return None
pass

def main():

#     The New Pipeline Order 
# Clean Up Script: Drops existing tables and recreates the empty raw_valet_data staging table.

# Python Load: Fetches data from the Bank of Canada API and uses COPY to fill the staging table.

# Transformation Script: Runs your SQL logic to parse the JSON and populate series_metadata, calendar, and observations.

    db_connect = get_connection()
    if db_connect is None:
        print("Failed to connect to the database.")
    
    # Extract: Script to pull raw HTML/JSON and save to local storage or a landing table
    # Load: Python to move raw data into a PostgreSQL "staging" schema
    # Transform: Use SQL views or procedures within Postgres to clean and structure the data
    loading_data = load_rates(db_connect)
    if loading_data is True:
        print("Files finish loading")
        print("ELT complete. Restarting app.py...")
        # This command starts app.py as a new process
        # Use 'python' or 'python3' depending on your environment
        subprocess.Popen(['python', 'app.py'])
        
    db_connect.close()
    sys.exit(1)
pass

if __name__ == '__main__':
    main()
pass
