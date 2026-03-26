import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv
import psycopg
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

load_dotenv()

# pulling login credentials from file outside the project
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')

# Construct the connection string using the variables
DB_CONNECTION = f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST}"

api_server = Flask(__name__)
CORS(api_server)

@api_server.route('/')
def home():
# This tells Flask to look in the /templates folder for your file
    return render_template('index.html')

@api_server.route('/api/metadata')
def get_metadata ():

    # currency button information
    # pulling the lable and description from the table created from 
    # the Bank of Canada Valet API
    # Example: USD/CAD US dollar to Canadian dollar daily exchange rate

    button_query = """ SELECT series_id, label, description FROM series_metadata"""

    try:
        with psycopg.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cur:
                
                cur.execute(button_query)
                rows = cur.fetchall()
        
            # metadata = [{"label": row[0], "description": row[1]} for row in rows]
            metadata = [
                {"series_id": row[0], "label": row[1], "description": row[2]} 
                for row in rows
            ]
            return jsonify(metadata)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
pass

@api_server.route('/api/rates') 
def get_rates():
    
    # pulling data from the three tables created from the 
    # Bank of Canada Valet API with view 
    # Example: 2024-09-23	USD/CAD	1.351	US dollar to Canadian dollar daily exchange rate


    # Chart Data
    row_limit = request.args.get('limit', default=30, type=int)
    selected_currency = request.args.get('currency', default='FXUSDCAD')

    # 1. We define the query with a placeholder
    query = """
            SELECT date, currency, rate, description 
            FROM v_daily_exchange_rates
            WHERE series_id = %s
            ORDER BY date DESC
            LIMIT %s;
            """

    try:
        with psycopg.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cur:
                
                cur.execute(query, (selected_currency, row_limit))
                rows = cur.fetchall()
                                
                # We need to format this for the Chart
                # We reverse it so the oldest date is on the left of the chart
                data = {
                    "labels": [row[0].strftime('%Y-%m-%d') for row in reversed(rows)],
                    "values": [float(row[2]) for row in reversed(rows)],
                    "all_data": [
                        {
                            "date": row[0].strftime('%Y-%m-%d'),
                            "currency": row[1],
                            "rate": float(row[2]),
                            "description": row[3]
                        } for row in reversed(rows)
                    ]
                } 
                return jsonify(data)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_server.route('/api/summary-stats')
def get_summary_stats():
    # The same logic you just tested in the terminal
    query = """
            SELECT 
                MIN(value), 
                MAX(value), 
                ROUND(AVG(value), 4),
                MAX(value) - MIN(value)
            FROM observations
            WHERE series_id = %s;
            """
    selected_currency = request.args.get('currency', default='FXUSDCAD')

    try:
        with psycopg.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (selected_currency,))
                row = cur.fetchone()

                if row[0] is None:
                    return jsonify({"error": "No data found"}), 404
                
                stats = {
                    "min": float(row[0]),
                    "max": float(row[1]),
                    "average": float(row[2]),
                    "range": float(row[3])
                }
                return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        api_server.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        print("Shutting down... running cleanup script.")
        # Ensure the path to your .bat file is correct
        subprocess.run(['./cleanup.bat'], shell=True)