import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

print("🚀 Starting model training...")

try:
    # 1. Read the file
    df = pd.read_csv('traffic_data.csv')
    
    # Debug: Show what Python actually sees in the file
    print(f"Found Columns: {list(df.columns)}")
    
    # 2. Define features
    features = ['CarCount', 'BikeCount', 'BusCount', 'TruckCount', 'TotalCount']
    
    # 3. Process
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])
    
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    model.fit(scaled)
    
    # 4. Save
    pickle.dump(scaler, open('scaler.pkl', 'wb'))
    pickle.dump(model, open('traffic_model.pkl', 'wb'))
    
    print("✅ Success! Model and Scaler are ready.")

except Exception as e:
    print(f"❌ Error: {e}")