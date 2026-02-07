import pandas as pd

# Step 1: Load the dataset
file_path = '/mnt/data/synthetic_pharma_sales_maharashtra.csv'
df = pd.read_csv("synthetic_pharma_sales_maharashtra.csv")

# Step 2: Print column names
print("Column Names:")
print(df.columns.tolist())
print("\n")

# Step 3: Check for duplicates, missing values, and empty rows
print(f"Initial number of rows: {len(df)}")
print(f"Number of duplicate rows: {df.duplicated().sum()}")
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nCompletely empty rows:")
print((df.isnull().all(axis=1)).sum())

# Step 4: Clean the data
# Remove duplicate rows
df = df.drop_duplicates()

# Drop completely empty rows (if any)
df = df.dropna(how='all')

# Optionally: Fill missing values (example: fill with 0 or a placeholder)
df = df.fillna(0)

# Step 5: Check after cleaning
print("\nAfter Cleaning:")
print(f"Number of rows after cleaning: {len(df)}")
print(f"Number of duplicate rows after cleaning: {df.duplicated().sum()}")
print("\nMissing values per column after cleaning:")
print(df.isnull().sum())
print("\nCompletely empty rows after cleaning:")
print((df.isnull().all(axis=1)).sum())



#rolling features
print("    ")
# Create 'date' column assuming 'Month' is numeric or string month
df['date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2) + '-01')
# Sort by date
df = df.sort_values('date')
# Create rolling feature: average sales volume over the last 7 months
df['sales_volume_last_7m_avg'] = df['Sales Volume'].rolling(window=7, min_periods=1).mean()
# Display sample of the results
print(df[['date', 'Drug', 'Sales Volume', 'sales_volume_last_7m_avg']].head(15))




#seasonal indicator
def get_season(month):
    if month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Winter'

df['season'] = df['date'].dt.month.apply(get_season)

# Step 7: Display sample results
print(df[['date', 'Drug', 'Sales Volume', 'sales_volume_last_7m_avg', 'season']].head(15))


# weekend indicator
df['is_weekend'] = df['date'].dt.dayofweek.apply(lambda x: x >= 5)


# Add Sales Trend Flag
# Compare current month's Sales Volume with previous month (per Region + Drug)
df['sales_volume_prev_month'] = df.groupby(['Region', 'Drug'])['Sales Volume'].shift(1)
df['sales_trend'] = (df['Sales Volume'] > df['sales_volume_prev_month']).astype(int)
# Convert date to month
df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
# Aggregate sales by month, Region, Drug
monthly_sales = df.groupby(['month', 'Region', 'Drug'])['Sales Volume'].sum().reset_index()
# Add previous month's sales
monthly_sales['sales_volume_prev_month'] = monthly_sales.groupby(['Region', 'Drug'])['Sales Volume'].shift(1)
# Add trend flag
monthly_sales['sales_trend'] = (monthly_sales['Sales Volume'] > monthly_sales['sales_volume_prev_month']).astype(int)


# Display Sample Data
print(df[['date', 'Region', 'Drug', 'Sales Volume', 'sales_volume_last_7m_avg', 'season', 'is_weekend', 'sales_volume_prev_month', 'sales_trend']].head(15))


#business alerts
# Compute 90th percentile per Region + Drug
percentiles = df.groupby(['Region', 'Drug'])['Sales Volume'].quantile(0.90).reset_index()
percentiles.rename(columns={'Sales Volume': 'sales_volume_90th'}, inplace=True)
# Merge back into main df
df = pd.merge(df, percentiles, on=['Region', 'Drug'], how='left')
# Flag high sales days
df['high_sales_alert'] = (df['Sales Volume'] > df['sales_volume_90th']).astype(int)
# --- Display with alert column ---
print(df[['date', 'Region', 'Drug', 'Sales Volume', 'sales_volume_last_7m_avg',
          'season', 'is_weekend', 'sales_volume_prev_month', 'sales_trend',
          'high_sales_alert']].head(20))






