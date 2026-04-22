from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from soil_engine import analyze_soil
import os

app = Flask(__name__)
CORS(app)

# Home route (serves UI)
@app.route("/")
def home():
    return render_template("index.html")

# API route
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    crop = data.get('crop')
    soil_color = data.get('soil_color')
    previous_yield = data.get('previous_yield')
    fertilizer_used = data.get('fertilizer_used')
    location = data.get('location')

    if not all([crop, soil_color, previous_yield, fertilizer_used]):
        return jsonify({"error": "Missing input data"}), 400

    result = analyze_soil(crop, soil_color, previous_yield, fertilizer_used, location)

    return jsonify(result)

# Render-compatible run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
