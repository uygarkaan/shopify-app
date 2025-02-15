import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Shopify API bilgileri
SHOPIFY_STORE_URL = "https://your-store.myshopify.com"
API_KEY = "your_api_key"
PASSWORD = "your_api_password"

# Shopify müşteri etiketi ekleme fonksiyonu
def add_customer_tag(customer_id, tag):
    url = f"{SHOPIFY_STORE_URL}/admin/api/2023-01/customers/{customer_id}.json"
    headers = {"Content-Type": "application/json"}
    auth = (API_KEY, PASSWORD)
    
    # Mevcut müşteri bilgilerini al
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return f"Error fetching customer: {response.text}"
    
    customer_data = response.json()["customer"]
    existing_tags = customer_data.get("tags", "")
    
    # Yeni etiketi ekleyerek güncelle
    new_tags = existing_tags + ", Beklemede" if existing_tags else "Beklemede"
    update_data = {"customer": {"id": customer_id, "tags": new_tags}}
    
    response = requests.put(url, headers=headers, auth=auth, data=json.dumps(update_data))
    return response.text

# Shopify Webhook Endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    customer_id = data.get("id")
    
    if customer_id:
        add_customer_tag(customer_id, "Beklemede")
        return "Success", 200
    
    return "Invalid data", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
