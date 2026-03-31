import pandas as pd
import os

filename = 'traffic_data.csv'

# 1. Remove the old file if it exists to clear any errors
if os.path.exists(filename):
    os.remove(filename)
    print("🗑️ Old empty file deleted.")

# 2. Create fresh data with proper headers
data = {
    'CarCount': [10, 50, 5, 80, 15, 60, 20, 100, 12, 75],
    'BikeCount': [20, 60, 10, 90, 25, 70, 30, 120, 15, 85],
    'BusCount': [2, 10, 1, 15, 3, 12, 5, 20, 2, 18],
    'TruckCount': [1, 5, 0, 10, 2, 8, 3, 12, 1, 11],
    'TotalCount': [33, 125, 16, 195, 45, 150, 58, 252, 30, 189]
}

df = pd.DataFrame(data)

# 3. Save it and FORCE it to write immediately
df.to_csv(filename, index=False)
print(f"✅ Fresh '{filename}' created with {len(df)} rows!")