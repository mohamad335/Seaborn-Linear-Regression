import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('data/cost_revenue_dirty.csv')
chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget', 
                    'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']
 
for col in columns_to_clean:
    for char in chars_to_remove:
        # Replace each character with an empty string
        df[col] = df[col].astype(str).str.replace(char, "")
    # Convert column to a numeric data type
    df[col] = pd.to_numeric(df[col])
df['Release_Date'] = pd.to_datetime(df['Release_Date'])
