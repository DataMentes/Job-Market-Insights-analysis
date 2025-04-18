#%%
from scripts.clean_data import *
#%%
df = pd.read_csv('../data/raw/saudi-arabia_raw.csv')
#%%
split_column(df, 'location', [1], '·', ['city'], reverse=True)
#%%
split_column(df, 'career_level', [0, 1, 2], '·', ['type', 'exp', 'no_exp'], reverse=True)
#%%
split_career_level(df)
#%%
df['exp'].replace('Unknown', np.nan, inplace=True)
#%%
df['experience_'] = df['experience'].combine_first(df['exp'])
#%%
df['no_exp'].replace('Unknown', np.nan, inplace=True)
#%%
df['num_of_exp_years'] = df['num_of_exp'].combine_first(df['no_exp'])
#%%
split_industry(df)
#%%
df
#%%
split_column(df, 'location', index=[1], split_char='·', names=['city'],reverse=True)
#%%
split_column(df, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
#%%
df['remote'].fillna('من المقر', inplace=True)
df['age'].fillna('لا تفضيل', inplace=True)
df['sex'].fillna('لا تفضيل', inplace=True)
df['experience_'].fillna('لا تفضيل', inplace=True)
df['num_of_exp_years'].fillna('لا تفضيل', inplace=True)
#%%
df.drop(columns=['exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link','Unnamed: 0','salary', 'nationality'],
        inplace=True)
#%%
df
#%%