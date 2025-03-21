from flask import Flask, request, jsonify
import requests
from datetime import datetime
import geoip2.database

app = Flask(__name__)

GEOIP_DATABASE_PATH = "ingestion/GeoLite2-Country.mmdb"

ANALYSIS_SERVICE_A_I = "http://128.110.223.14:5001/process"
ANALYSIS_SERVICE_J_R = "http://128.110.223.15:5001/process"
ANALYSIS_SERVICE_S_Z = "http://128.110.223.13:5001/process"

def get_country_from_ip(ip):
    try:
        with geoip2.database.Reader(GEOIP_DATABASE_PATH) as reader:
            response = reader.country(ip)
            return response.country.name
    except Exception as e:
        return f"Error: {e}"

def get_analysis_service_url(country):
    if not country:
        return None
    first_letter = country[0].upper()
    if first_letter >= 'A' and first_letter <= 'I':
        return ANALYSIS_SERVICE_A_I
    elif first_letter >= 'J' and first_letter <= 'R':
        return ANALYSIS_SERVICE_J_R
    elif first_letter >= 'S' and first_letter <= 'Z':
        return ANALYSIS_SERVICE_S_Z
    return None

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json

    user_id = data.get("user_id")
    ip = data.get("IP")
    product_type = data.get("product_type")
    price = data.get("price")
    timestamp = data.get("timestamp")

    country = get_country_from_ip(ip) if ip else None

    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + "Z"

    analysis_service_url = get_analysis_service_url(country)
    if not analysis_service_url:
        return jsonify({"status": "error", "message": "Invalid country"}), 400

    cleaned_data = {
        "user_id": user_id,
        "country": country,
        "product_type": product_type,
        "price": price,
        "timestamp": timestamp
    }

    try:
        response = requests.post(analysis_service_url, json=cleaned_data)
        response.raise_for_status()
        return jsonify({"status": "success", "analysis_response": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
