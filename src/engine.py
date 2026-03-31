import pickle
import numpy as np
import pandas as pd

class TrafficEngine:
    def __init__(self, model_path='models/traffic_model.pkl', scaler_path='models/scaler.pkl'):
        """Initializes the engine by loading the saved model and scaler."""
        with open(model_path, 'rb') as m, open(scaler_path, 'rb') as s:
            self.model = pickle.load(m)
            self.scaler = pickle.load(s)

    def get_signal_config(self, car, bike, bus, truck):
        """Single prediction for the slider-based dashboard."""
        total = car + bike + bus + truck
        # Match the feature order from training: CarCount, BikeCount, BusCount, TruckCount, TotalCount
        features = np.array([[car, bike, bus, truck, total]])
        scaled_data = self.scaler.transform(features)
        
        cluster = self.model.predict(scaled_data)[0]
        
        configs = {
            0: {"status": "SMOOTH FLOW", "color": "#10b981", "timer": 30},
            1: {"status": "MODERATE", "color": "#f59e0b", "timer": 60},
            2: {"status": "CONGESTED", "color": "#ef4444", "timer": 120}
        }
        return configs.get(cluster, configs[1])

    def predict_batch(self, df):
        """Batch prediction for uploaded CSV files."""
        # Ensure the columns match what the model expects
        required_cols = ['CarCount', 'BikeCount', 'BusCount', 'TruckCount', 'TotalCount']
        
        # Validation: Check if all columns exist
        if not all(col in df.columns for col in required_cols):
            missing = [c for c in required_cols if c not in df.columns]
            raise ValueError(f"CSV missing columns: {missing}")
        
        # Scale and Predict the entire dataframe at once
        scaled_data = self.scaler.transform(df[required_cols])
        clusters = self.model.predict(scaled_data)
        
        # Map clusters to Timers/Status
        mapping = {
            0: {"status": "SMOOTH", "timer": 30},
            1: {"status": "MODERATE", "timer": 60},
            2: {"status": "CONGESTED", "timer": 120}
        }
        
        df['Predicted_Timer'] = [mapping[c]['timer'] for c in clusters]
        df['Traffic_Status'] = [mapping[c]['status'] for c in clusters]
        return df