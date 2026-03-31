import pandas as pd
import numpy as np

# Generate 500 rows of data
np.random.seed(42)
n_rows = 500

cars = np.random.randint(5, 100, n_rows)
bikes = np.random.randint(10, 150, n_rows)
buses = np.random.randint(0, 20, n_rows)
trucks = np.random.randint(0, 15, n_rows)
total = cars + bikes + buses + trucks

data = {
    'CarCount': cars,
    'BikeCount': bikes,
    'BusCount': buses,
    'TruckCount': trucks,
    'TotalCount': total
}

df = pd.DataFrame(data)
df.to_csv('traffic_data.csv', index=False)
print("✅ Created traffic_data.csv with 500 rows of sample data!")