from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

visits_per_country = defaultdict(int)
unique_users_per_country = defaultdict(set)
total_products_bought = defaultdict(int)
revenue_per_product_type = defaultdict(float)
revenue_per_country = defaultdict(float)
records_per_month = defaultdict(int)

@app.route('/process', methods=['POST'])
def process():
    data = request.json

    user_id = data.get("user_id")
    country = data.get("country")
    product_type = data.get("product_type")
    price = float(data.get("price"))
    timestamp = data.get("timestamp")

    visits_per_country[country] += 1
    unique_users_per_country[country].add(user_id)
    total_products_bought[product_type] += 1
    revenue_per_product_type[product_type] += price
    revenue_per_country[country] += price

    date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    month_key = date.strftime("%Y-%m")
    records_per_month[month_key] += 1

    response = {
        "status": "success",
        "metrics": {
            "visits_per_country": dict(visits_per_country),
            "unique_users_per_country": {k: len(v) for k, v in unique_users_per_country.items()},
            "total_products_bought": dict(total_products_bought),
            "revenue_per_product_type": dict(revenue_per_product_type),
            "revenue_per_country": dict(revenue_per_country),
            "records_per_month": dict(records_per_month),
        }
    }

    return jsonify(response)

if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5001)
