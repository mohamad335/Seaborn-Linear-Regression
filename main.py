import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
avarage_budget = df['USD_Production_Budget'].mean() 
#min of Worldwide gross and domestic gross
min_world_wide_Gross=df['USD_Worldwide_Gross'].min()
min_domestic_gross = df['USD_Domestic_Gross'].min()
#highest production budget and highest worldwide gross
max_world_wide_gross=df['USD_Worldwide_Gross'].max()
max_production_budget=df['USD_Production_Budget'].max()
#revenue of the highest and lowest budget films
max_revenue=df['USD_Worldwide_Gross'].idxmax()
min_revenue=df['USD_Worldwide_Gross'].idxmin()
#films grossed 0$ domestically
zero_domestic=df.query('USD_Domestic_Gross==0')
#highest budget films that grossed nothing
grossed_nothing_budget=df.query('USD_Production_Budget==0')
#have budget but zero dpmestic
worldwide_released=df.query('USD_Domestic_Gross==0 & USD_Worldwide_Gross!=0')
print(f'Number of international releases: {len(worldwide_released)}')
print(worldwide_released.tail())
#identigy which films were not released yet as of the time of data collection (May 1st, 2018)
future_releases=df.query('Release_Date>= "2018-05-01"')
print(f'Number of un-released movies: {len(future_releases)}')
print(future_releases.head())
#drop all these movies
df_clean=df.drop(future_releases.index)
#films tat lost money
money_lost=df_clean.query('USD_Worldwide_Gross<USD_Production_Budget')
percent_lost=(len(money_lost)/len(df_clean))*100
print(f'Percentage of movies that lost money: {round(percent_lost,2)}')