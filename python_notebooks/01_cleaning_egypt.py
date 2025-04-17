#%%
import pandas as pd
from scripts.clean_data import apply_translation
#%%
df = pd.read_csv('../data/raw/egypt_raw.csv')
#%%
apply_translation(df, 'title5555', rows=[7, 20, 128])
#%%
apply_translation(df, 'title', rows=[7, 20, 128])
#%%
df.loc[7, 'title'] = 'Storekeeper'
df.loc[16, 'title'] = 'waiter'
df.head()
df.info