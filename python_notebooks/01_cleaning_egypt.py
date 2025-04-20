#%%
from scripts.clean_data import *
import warnings
import pandas as pd
import numpy as np
import sqlite3

warnings.filterwarnings("ignore")
#%%
df = pd.read_csv('../data/raw/egypt_raw.csv')
#%%
split_column(df, 'location', [1], '·', ['city'], reverse=True)
#%%
split_career_level(df)
#%%
df.type.value_counts()
#%%
split_industry(df)
#%%
split_column(df, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
#%%
df['exp'].replace('Unknown', np.nan, inplace=True)
#%%
df['experience_'] = df['experience'].combine_first(df['exp'])
#%%
df['no_exp'].replace('Unknown', np.nan, inplace=True)
#%%
df['num_of_exp_years'] = df['num_of_exp'].combine_first(df['no_exp'])
#%%
df['remote'].fillna('من المقر', inplace=True)
df['age'].fillna('لا تفضيل', inplace=True)
df['sex'].fillna('لا تفضيل', inplace=True)
df['experience_'].fillna('لا تفضيل', inplace=True)
df['num_of_exp_years'].fillna('لا تفضيل', inplace=True)
#%%
df = df[~df['title'].str.contains('سعودية', na=False)]
df = df[~df['title'].str.contains('سعوديه', na=False)]
df = df[~df['title'].str.contains('سعوية', na=False)]
#%%
df.drop(columns=['exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link',
                 'Unnamed: 0', 'salary', 'nationality', 'residence_area'],
        inplace=True)
#%%
analyses_date(df, 120)
#%%
df = pd.read_csv('../data/processed/egypt_clean.csv')
#%%
sorted_data = df.sort_values(by="title", key=lambda col: col.str.lower(), ascending=False).reset_index(drop=True)
#%%
apply_translation(sorted_data, 'title', rows=sorted_data.iloc[:40, :].index.tolist())
#%%
sorted_data.index = sorted_data['Unnamed: 0']
#%%
data = pd.read_csv('../data/processed/egypt_clean.csv').drop(columns=['Unnamed: 0'])
conn = sqlite3.connect('../database.db')
data.to_sql('EGYPT', con=conn, if_exists='replace', index=True)
conn.close()
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM EGYPT', conn)