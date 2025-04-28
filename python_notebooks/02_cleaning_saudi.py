#%%
from scripts.clean_data import *
import sqlite3
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
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
df.drop(columns=['exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link','Unnamed: 0','salary', 'nationality', 'residence_area'],
        inplace=True)
#%%
df
#%%
analyses_date(df, num_days = 120)
#%%
df
#%%
df.sort_values(by=['title'], ascending=False, inplace=True)
# sqlite_version = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=sqlite_version, if_exists='replace', index=False)
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
#%%
df.sort_values(by=['title'], ascending=False, inplace=True)
apply_translation(df, 'title', rows=df.iloc[:400, :].index.tolist())
# conn = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace', index=True)
#%%
from scripts.clean_data import *
import sqlite3
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
df.title = df.title.str.lower()
df.sort_values(by=['title'], ascending=True, inplace=True)
index = df.type.str.contains(r'تدريب', regex=True)
df.loc[index, 'experience_'] = 'خريج جديد'
translate_experience(df)
translate_type(df)
translate_sex(df)
translate_remote(df)
extract_job_grade(df)
extract_gender(df,'title')
extract_gender(df,'description')
extract_gender(df,'skills')
extract_remotely(df,'title')
extract_remotely(df,'description')
extract_remotely(df,'skills')
df.drop(columns=['age', 'description', 'skills', 'qualification', 'specialization'], inplace=True)
df['title'] = df['title'].str.replace(r'^\d+\.', '', regex=True)
df['title'] = df['title'].str.replace(r'^a\s\b', '', regex=True)
split_num_of_exp_years(df)
df
#%%
pd.set_option('display.max_rows', None)    # عرض جميع الصفوف
pd.set_option('display.max_columns', None) # عرض جميع الأعمدة

def review_matches(df, title_mapping):
    """
    البحث عن الأنماط المحددة في القاموس `title_mapping` داخل عمود `title` في DataFrame `df`.

    المدخلات:
        df (pd.DataFrame): الجدول الذي يحتوي على البيانات.
        title_mapping (dict): قاموس يحتوي على الأنماط المراد البحث عنها.

    المخرجات:
        قائمة بالنتائج التي تم العثور عليها.
    """
    for pattern in title_mapping.keys():

        matches = df.title[df.title.str.contains(pattern, regex=True, na=False)]
        print(pattern)
        print(matches)
        print('#'*80)
#%%
test_title_mapping = {
    r'^analyst': 'analyst',
    r'anesthesia assistant consultant': 'anesthesia assistant consultant',
    r'anesthesia consultant': 'anesthesia consultant',    
}
review_matches(df, test_title_mapping)
#%%
title_mapping = {
    r'driller': 'drilling Operator',
    r'\(senior\) marketing manager, games': 'marketing manager',
    r'\(مهندس مدني\) - civil engineer': 'civil engineer',
    r'financial analyst': 'financ"Onshore Oil Driller" OR "Driller"ial analyst',
    r'3d designer': '3d designer',
    r'7pqe\+ dispute resolution associate': 'legal counsel',
    r'a427-esg': 'HVAC Technician',
    r'accelerated command': 'first officer',
    r'accelerator manager': 'accelerator manager',
    r'account development - s8': 'retail vertical leader',
    r'^account director': 'account director',
    r'account executive': 'account executive',
    r'account management': 'account management',
    r'account manager': 'account manager',
    r'accountant': 'accountant',
    r'account receivable': 'account receivable',
    r'account solutions engineer': 'account solutions engineer',
    r'accounting associate': 'accounting associate',
    r'accounting \(intern\)': 'accounting',
    r'accounting - co-op trainee': 'accounting',
    r'accounts payable \(pre-opening\)': 'accounts payable',
    r'administrative assistant': 'administrative assistant',
    r'admin manager': 'admin manager',
    r'accounts receivable & accounts payable supervisor \(ar & ap supervisor\)': 'Accounts Receivable & Payable Supervisor',
    r'acquisition associate': 'acquisition associate',
    r'administration executive': 'administration executive',
    r'administrative manager': 'administrative manager',
    r'administrative coordinator': 'administrative coordinator',
    r'advanced application engr': "Advanced Application Engineer",
    r'aesthetics clinic manager': r'aesthetics clinic manager',
    r'^analyst': 'analyst',
    r'anesthesia assistant consultant': 'anesthesia assistant consultant',
    r'anesthesia consultant': 'anesthesia consultant',
    r'application architect': 'application architect',
    r'application engineer': 'application engineer',
    r'arabic to english': 'arabic to english',
    r'^architect\b': 'architect'
}

#%%
for pattern, replacement in title_mapping.items():
    df.title[df.title.str.contains(pattern, regex=True)] = replacement.lower()


df.sort_values(by=['title'], ascending=True, inplace=True)