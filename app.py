from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import sqlite3
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
model = pickle.load(open('./saved_model/model_data.sav', 'rb'))
feature_names = ["Fwd Seg Size Avg", "Flow IAT Min", "Flow Duration", "Tot Fwd Pkts", "Pkt Size Avg", "Src Port", "Init Bwd Win Byts"]

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Database setup
def init_db():
    with sqlite3.connect('predictions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Fwd_Seg_Size_Avg REAL,
                Flow_IAT_Min REAL,
                Flow_Duration REAL,
                Tot_Fwd_Pkts REAL,
                Pkt_Size_Avg REAL,
                Src_Port INTEGER,
                Init_Bwd_Win_Byts REAL,
                prediction TEXT
            )
        ''')
    conn.close()

init_db()

def save_to_db(data, prediction):
    with sqlite3.connect('predictions.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (Fwd_Seg_Size_Avg, Flow_IAT_Min, Flow_Duration, Tot_Fwd_Pkts, Pkt_Size_Avg, Src_Port, Init_Bwd_Win_Byts, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data["Fwd Seg Size Avg"], data["Flow IAT Min"], data["Flow Duration"], data["Tot Fwd Pkts"], data["Pkt Size Avg"], data["Src Port"], data["Init Bwd Win Byts"], prediction))
        conn.commit()
        app.logger.debug(f"Stored prediction in database: {data}, Prediction: {prediction}")
    conn.close()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    if not all(feature in data for feature in feature_names):
        error_message = f"Missing features. Required: {feature_names}"
        app.logger.error(error_message)
        return jsonify({"error": error_message}), 400
    
    # Convert input data to DataFrame
    df = pd.DataFrame([data])
    
    # Make prediction
    prediction = model.predict(df)[0]
    
    app.logger.debug(f"Prediction: {prediction}")
    
    # Save to database
    save_to_db(data, prediction)
    
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True, port=5000)




