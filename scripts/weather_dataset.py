import pandas as pd
import numpy as np

# List of cities in Maharashtra
cities = ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Kolhapur', 'Amravati']

# Generate date range
dates = pd.date_range(start='2020-01-01', end='2024-12-31')

data = []

for date in dates:
    month = date.month
    for city in cities:
        # Base temperature by city (approximate average ranges)
        base_temp = {
            'Mumbai': 30,
            'Pune': 28,
            'Nagpur': 32,
            'Nashik': 29,
            'Aurangabad': 31,
            'Solapur': 33,
            'Kolhapur': 28,
            'Amravati': 32
        }[city]
        
        # Seasonal adjustment
        if month in [6,7,8,9]:  # Monsoon
            temp = np.random.normal(loc=base_temp - 5, scale=3)
            humidity = np.random.uniform(80, 100)
            rainfall = np.random.uniform(5, 50)  # Significant rainfall
        elif month in [3,4,5]:  # Summer
            temp = np.random.normal(loc=base_temp + 5, scale=3)
            humidity = np.random.uniform(40, 60)
            rainfall = np.random.uniform(0, 5)
        else:  # Winter
            temp = np.random.normal(loc=base_temp - 10, scale=2)
            humidity = np.random.uniform(50, 80)
            rainfall = np.random.uniform(0, 2)
        
        wind_speed = np.random.uniform(5, 25)
        
        data.append([date.strftime('%Y-%m-%d'), city, round(temp, 2), round(humidity, 2), round(rainfall, 2), round(wind_speed, 2)])

# Create DataFrame
weather_df = pd.DataFrame(data, columns=['Date', 'City', 'Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)', 'Wind Speed (km/h)'])

# Save to CSV
weather_df.to_csv('synthetic_maharashtra_weather_2020_2024.csv', index=False)
