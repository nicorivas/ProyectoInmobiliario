import pandas as pd

df = pd.read_csv('test.csv')
print(df.head())
print(df.sample(frac=0.1))
print(df.describe())