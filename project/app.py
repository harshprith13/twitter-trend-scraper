from flask import Flask, render_template, jsonify
import subprocess
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['twitter_trends']  # Database name
collection = db['trending_topics']  # Collection name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the Selenium script as a subprocess
        subprocess.run(['python3', 'twitter_scraper.py'], check=True)

        # After running the script, fetch the latest entry from MongoDB
        latest_entry = collection.find_one(sort=[("timestamp", -1)])

        # Return the relevant data
        return jsonify({
            "timestamp": latest_entry["timestamp"],
            "trend1": latest_entry["trend1"],
            "trend2": latest_entry["trend2"],
            "trend3": latest_entry["trend3"],
            "trend4": latest_entry["trend4"],
            "trend5": latest_entry["trend5"],
            "ip_address": latest_entry["ip_address"],
            "record": latest_entry
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)