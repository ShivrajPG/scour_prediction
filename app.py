from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib
import os

app = Flask(__name__, static_folder='web')

# Change path logic strictly to access the correct model directory relative to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained ML Model and Scaler globally
try:
    rf_model = joblib.load(os.path.join(BASE_DIR, 'models', 'rf_model.pkl'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'models', 'scaler.pkl'))
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    # Fallback to importing train and eval on the fly if needed
    from src.model import train_and_evaluate
    print("Retraining fallback triggered...")
    data_path = os.path.join(BASE_DIR, 'data', 'synthetic_scour_data.csv')
    rf_model, _, scaler, _, _, _ = train_and_evaluate(data_path)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory(app.static_folder, 'style.css')

@app.route('/output/<path:filename>')
def serve_output(filename):
    out_dir = os.path.join(BASE_DIR, 'output')
    return send_from_directory(out_dir, filename)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Format the data exactly as the scaler expects
        features = ['Flow_Velocity_V', 'Pier_Diameter_D', 'Water_Depth_h', 'Grain_Size_d50']
        
        # Build scenario DataFrame
        input_data = pd.DataFrame([{
            'Flow_Velocity_V': float(data.get('v', 1.0)),
            'Pier_Diameter_D': float(data.get('d', 1.0)),
            'Water_Depth_h': float(data.get('h', 3.0)),
            'Grain_Size_d50': float(data.get('d50', 1.0)),
        }])

        X_scaled = scaler.transform(input_data[features])
        prediction = rf_model.predict(X_scaled)[0]
        
        # Ensure prediction uses realistic non-negative floor
        prediction = max(0.01, prediction)

        return jsonify({'success': True, 'scour_depth': round(float(prediction), 2)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting ML Backend Server explicitly on http://127.0.0.1:5000")
    print("   Ready for live professor testing.")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
