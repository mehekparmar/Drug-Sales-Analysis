import pandas as pd

# Load pharma sales dataset
sales_file_path = '/mnt/data/synthetic_pharma_sales_maharashtra.csv'
sales_df = pd.read_csv("synthetic_pharma_sales_maharashtra.csv")

# Create 'date' column in sales dataset
sales_df['date'] = pd.to_datetime(
    sales_df['Year'].astype(str) + '-' + sales_df['Month'].astype(str).str.zfill(2) + '-01'
)

# Load weather dataset
weather_file_path = '/mnt/data/synthetic_maharashtra_weather_2020_2024.csv'
weather_df = pd.read_csv("synthetic_maharashtra_weather_2020_2024.csv")

# Prepare weather dataset
weather_df['Date'] = pd.to_datetime(weather_df['Date'])
weather_df = weather_df.rename(columns={'Date': 'date', 'City': 'Region'})

# Merge datasets
combined_df = pd.merge(
    sales_df,
    weather_df,
    how='left',
    on=['date', 'Region']
)

# Step 1: Check initial state
print(f"Initial rows: {len(combined_df)}")
print(f"Duplicate rows: {combined_df.duplicated().sum()}")
print(f"Rows completely empty: {(combined_df.isnull().all(axis=1)).sum()}")
print("\nMissing values per column before cleaning:")
print(combined_df.isnull().sum())

# Step 2: Clean the dataset
combined_df = combined_df.drop_duplicates()                # Remove duplicates
combined_df = combined_df.dropna(how='all')              # Drop fully empty rows

# Apply interpolation to fill missing values (numeric columns only)
combined_df = combined_df.interpolate(method='linear', limit_direction='both')

# Step 3: Final check
print("\nAfter Cleaning:")
print(f"Rows after cleaning: {len(combined_df)}")
print(f"Duplicate rows now: {combined_df.duplicated().sum()}")
print(f"Rows completely empty now: {(combined_df.isnull().all(axis=1)).sum()}")
print("\nMissing values per column after cleaning:")
print(combined_df.isnull().sum())

# Display first 10 cleaned rows
print("\nCleaned data:")
print(combined_df.head(10))
