import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

df = pd.read_csv('customer_shopping_behavior.csv')
print(df.head())

print(df.info())
print(df.describe(include='all'))

print(df.columns)

print(df.isnull().sum())

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")

print(df.columns)

df.rename(columns = {'purchase_amount_(usd)':'purchase_amount'},inplace = True)

print(df.columns)


print(df['age'].describe())


labels = ['New Adult','Mid Adult','Senior Adult','Old']

df['age_group'] = pd.qcut(df['age'],labels= labels, q = 4)

print(df[['age','age_group']].head())


print(df.groupby('frequency_of_purchases').describe())


frequency_mapping = {'Annually':365,'Bi-Weekly':14,'Every 3 Months':90,'Fortnightly':14,'Monthly':30,'Quarterly':90,'Weekly':7}


df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['frequency_of_purchases','purchase_frequency_days']].head())



print((df.discount_applied == df.promo_code_used).all())

df = df.drop('promo_code_used',axis = 1)



from sqlalchemy import create_engine


#connect to postgresql

username = 'postgres'
password = 'Hrishi12345'
host = 'localhost'
port = '5432'
database = 'customer_info'


engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")

