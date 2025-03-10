import pandas as pd
from pandas import DatetimeIndex
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
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
#print(f'Number of international releases: {len(worldwide_released)}')
#print(worldwide_released.tail())
#identigy which films were not released yet as of the time of data collection (May 1st, 2018)
future_releases=df.query('Release_Date>= "2018-05-01"')
#print(f'Number of un-released movies: {len(future_releases)}')
#print(future_releases.head())
#drop all these movies
df_clean=df.drop(future_releases.index)
#films that lost money
money_lost=df_clean.query('USD_Worldwide_Gross<USD_Production_Budget')
percent_lost=(len(money_lost)/len(df_clean))*100
#print(f'Percentage of movies that lost money: {round(percent_lost,2)}')
#create a scatter plot by using a seaborn library 
def scatter_plot():
    plt.figure(figsize=(8,4), dpi=110)
    with sns.axes_style("darkgrid"):
        ax = sns.scatterplot(data=df_clean, 
                        x='Release_Date', 
                        y='USD_Production_Budget',
                        hue='USD_Worldwide_Gross',
                        size='USD_Worldwide_Gross',)
    
        ax.set(ylim=(0, 450000000),
            xlim=(df_clean.Release_Date.min(), df_clean.Release_Date.max()),
            xlabel='Year',
            ylabel='Budget in $100 millions')
    plt.savefig('images/scatter_plot.png')
    plt.show()
df_time=DatetimeIndex(df_clean.Release_Date)
year=df_time.year
decades_year=year//10*10
df_clean['Decade']=decades_year
old_films=df_clean[df_clean.Decade<=1960]
new_films=df_clean[df_clean.Decade >1960]
def old_film():
    plt.figure(figsize=(8, 4), dpi=110)
    with sns.axes_style('darkgrid'):
        sns.regplot(data=old_films,
                    x='USD_Production_Budget',
                    y='USD_Worldwide_Gross',
                    scatter_kws={'alpha': 0.4},
                    line_kws={'color': 'black'})
    plt.savefig('images/old_films.png')
    plt.show()
def new_film():
    plt.figure(figsize=(8, 4), dpi=110)
    with sns.axes_style('darkgrid'):
        sns.regplot(data=new_films,
                    x='USD_Production_Budget',
                    y='USD_Worldwide_Gross',
                    color='#2f4b7c',
                    scatter_kws={'alpha': 0.4},
                    line_kws={'color': '#ff7c43'})
    plt.savefig('images/new_films.png')
    plt.show()

regression=LinearRegression()
# Explanatory Variable(s) or Feature(s)
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
# Response Variable or Target
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)
print(regression.intercept_)
print(regression.coef_)
print(regression.score(X, y))
#linear regression for old_films
x=pd.DataFrame(old_films,columns=['USD_Production_Budget'])
y=pd.DataFrame(old_films,columns=['USD_Worldwide_Gross'])
regression.fit(x, y)
print(f"the slope cooficient is: {regression.coef_[0]}")
print(f"the intercept cooficient is: {regression.intercept_}")
print(f"the R-squared is: {regression.score(x, y)}")
#calculate the estimate about 350 million $
budget=350000000
revenue_estimate=regression.intercept_[0]+regression.coef_[0,0]*budget
print(f"the estimated revenue for a $350 film is: {round(revenue_estimate, -6)/1000000} million $")


