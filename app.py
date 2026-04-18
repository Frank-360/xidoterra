from flask import Flask, request, jsonify
from flask_cors import CORS
from soil_engine import analyze_soil
from flask import render_template

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def home():
    return "XidoTerra Soil AI API is running 🚀"

@app.route('/ui')
def ui():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    crop = data.get('crop')
    soil_color = data.get('soil_color')
    previous_yield = data.get('previous_yield')
    fertilizer_used = data.get('fertilizer_used')
    location = data.get('location')
    print("LOCATION RECEIVED:", location)

    if not all([crop, soil_color, previous_yield, fertilizer_used]):
        return jsonify({"error": "Missing input data"}), 400

    result = analyze_soil(crop, soil_color, previous_yield, fertilizer_used, location)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)