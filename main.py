from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=['https://socialpulse-iota.vercel.app'])

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "b813fde7-815c-419a-b02f-c3983c6e2d4f"
FLOW_ID = "fc69aa7e-9ae9-4ff7-8570-23546e8c9983"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Text input is required"}), 400
    
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
        payload = {
            "input_value": text,
            "output_type": "chat",
            "input_type": "chat",
        }
        headers = {
            "Authorization": "Bearer " + APPLICATION_TOKEN,
            "Content-Type": "application/json",
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
 port = int(os.environ.get('PORT', 5000))
 app.run(host='0.0.0.0', port=port)
