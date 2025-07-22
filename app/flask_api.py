import pickle
from flask import Flask, request, jsonify
import pandas as pd
from dataProcess import process
from sklearn.preprocessing import RobustScaler

app = Flask(__name__)


# Load the model (pipeline or custom object)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure file was sent
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Try to read and process the CSV
    try:
        df = pd.read_csv(file)
        df = process(df)  # your custom cleaning logic

        # Select features used during training
        features = ['merchant_category', 'transaction_type', 'days_since_last_txn',
                    'location_freq_for_customer', 'is_night_transaction',
                    'weekly_txn_count', 'transaction_amount_log']

        # Scale only the selected features
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(df[features])  # X_scaled is a NumPy array

        # Predict using the trained model
        df["anomaly_score"] = model.predict(X_scaled)
        df["anomaly_rate"] = model.decision_function(X_scaled)

        # Save the result
        df.to_csv('output.csv', index=False)

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    # Build and return a response
    results = []
    for pred, score in zip(df["anomaly_score"], df["anomaly_rate"]):
        results.append({
            "prediction": int(pred),
            "anomaly_score": float(score)
        })

    return jsonify({'predictions': results})

if __name__ == "__main__":
    app.run(host="", port=5000)

