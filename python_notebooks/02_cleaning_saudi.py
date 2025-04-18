#%%
import pandas as pd
from scripts.clean_data import *
import numpy as np
import re
#%%
df = pd.read_csv('../data/raw/saudi-arabia_raw.csv')
df.head(10)
#%%
df.tail(10)
#%%
df.info()
#%%
df.describe()
#%%
df.drop('Unnamed: 0', axis = 1, inplace=True)
df
#%%
split_column(df, 'location', index=[1], split_char='·', names=['city'],reverse=True)
df
#%%
df.drop(['salary', 'nationality'], inplace=True, axis=1)
df
#%%
df['remote'].fillna('من المقر', inplace=True)
df['age'].fillna('لا تفضيل', inplace=True)
df['sex'].fillna('لا تفضيل', inplace=True)
df
#%%
split_column(df, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
df