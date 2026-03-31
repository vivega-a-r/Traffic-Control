import pandas as pd
import numpy as np

# Configuration
n_rows = 100  # Number of simulated sensor readings
filename = "real_sensor_data.csv"

# Generate random but realistic traffic data
np.random.seed(42)
cars = np.random.randint(0, 150, n_rows)
bikes = np.random.randint(0, 100, n_rows)
buses = np.random.randint(0, 40, n_rows)
trucks = np.random.randint(0, 30, n_rows)

# The model expects 'TotalCount' as a specific feature
total = cars + bikes + buses + trucks

# Create DataFrame
df = pd.DataFrame({
    'CarCount': cars,
    'BikeCount': bikes,
    'BusCount': buses,
    'TruckCount': trucks,
    'TotalCount': total
})

# Save to CSV
df.to_csv(filename, index=False)
print(f"✅ Success! {filename} created with {n_rows} rows of test data.")
print("You can now upload this file to your Traffic Command Dashboard.")