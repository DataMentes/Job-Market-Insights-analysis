#%%
from scripts.clean_data import *
#%%
df = pd.read_csv('../data/raw/egypt_raw.csv')
#%%
split_column(df, 'location', [1], '·', ['city'])
#%%
df.career_level.value_counts()
#%%
df['career_level'].str.split('·')
#%%
df['industry'].value_counts()
#%%
split_column(df, 'career_level', [0,1,2], '·', ['type','exp','no_exp'],reverse=True)
#%%
split_career_level(df)
#%%
df.get()