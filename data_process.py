import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# Load data
df = pd.read_csv('traffic_data.csv')

# Select only numerical features for clustering
features = ['CarCount', 'BikeCount', 'BusCount', 'TruckCount', 'TotalCount']
data = df[features].dropna()

# Scaling (Crucial for K-Means)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# Save the scaler to use later in the UI
pickle.dump(scaler, open('scaler.pkl', 'wb'))
print("Data scaled and scaler saved!")