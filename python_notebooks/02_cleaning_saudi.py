#%%
import pandas as pd
from scripts.clean_data import *
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
df.location.value_counts()
#%%
split_column(df, 'location', index=1, split_char='·', names='location')
df