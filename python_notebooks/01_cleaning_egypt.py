#%%
from scipy.signal import unique_roots

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
# data.to_sql('EGYPT', con=conn, if_exists='replace', index=True)
conn.close()
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM EGYPT', conn)
#%%
df = df.sort_values(by="title", key=lambda col: col.str.lower()).reset_index(drop=True)
df.title = df.title.str.lower()
#%%
df = df[~df['title'].str.contains('saudi arabia', na=False)]
df = df[~df['title'].str.contains('saudi', na=False)]
#%%
split_num_of_exp_years(df)
#%%
translate_sex(df)
translate_type(df)
translate_remote(df)
translate_experience(df)
#%%
extract_job_grade(df)
extract_gender(df, 'title')
extract_gender(df, 'description')
extract_gender(df, 'skills')
extract_remotely(df, 'title')
extract_remotely(df, 'description')
extract_remotely(df, 'skills')
#%%
df.to_sql('EGYPT', con=conn, if_exists='replace')
conn.close()
#%%
# df.drop(columns=['age','description','skills','qualification','specialization'], axis=1, inplace=True)
#%%
from scripts.clean_data import *
import warnings
import pandas as pd
import numpy as np
import sqlite3

warnings.filterwarnings("ignore")
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM EGYPT', conn)
conn.close()
#%%
df = df[~df['title'].str.contains('saudi', na=False)]
df.title = df.title.str.replace(r'^((sr(\b|\s)|\ssr?(\b|\s))|senior|junior|staff)', '', regex=True).str.strip()
df.title = df.title.str.replace(r'^(\.|\-|/|\,|\\)', '', regex=True).str.strip()
df.title = df.title.str.replace(r'(\.|\-|/|\,|\\)+$', '', regex=True).str.strip()
df = df.sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
unique = pd.DataFrame(df.title.value_counts()).reset_index().rename(columns={'index': 'title', 'count': 'count'}).sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
replace_dict = {
    # r'^account management.*': 'Account Management',
    # r'^account manager.*': 'Account Manager',
    # r'^account payable accountant.*': 'Account Payable Accountant',
    # r'^account receivable.*': 'Account Receivable',
    # r'^accounting (& financial|& reporting|manager).*': 'Accounting Manager',
    # r'^accounting (section|supervisor|team|assistant|advisory).*': 'Accounting Supervisor',
    # r'^accounting intern.*?': 'Accountant',
    # r'^accounts payable.*': 'Accounts Payable',
    # r'^accounts receivable.*': 'Accounts Receivable',
    # r'^accounts supervisor.*': 'Accounts Receivable Supervisor',
    # r'^accountant.*': 'Accountant',
    # r'^(admin|administrative) assistant.*': 'Admin Assistant',
    # r'^admin .* office manager': 'Office Manager',
    # r'^admin (account management)*': 'Account Management',
    # r'^administrator (facilities)': 'Admin',
    # r'^(administration|administrative) supervisor': 'Admin Supervisor',
    # r'^administrative experience in the field of contracting': 'Admin',
    # r'^ai(\s|/|\b).*': "AI/ML Engineer",
    # r'^ai(\s|/|\b).* lead': "AI/ML Lead",
    # r'^ai engineering manager': "AI/ML Manager",
    # r'^analyst.*': 'Customer Insights Analyst',
    # r'^analyst, sales support': 'Sales Support Analyst',
    # main
    r'^treasurer$': 'treasury specialist',
    r'^treasur(y|er)\s?(specialist|senior specialist|and| - emea).*': 'treasury specialist',
    r'^treasury senior accountant': 'treasury accountant',
    r'^treasury (section|head).*': 'treasury lead',
    r'technical support': 'Support Engineer',
    r'technical support &': 'Support manager',
    r'service manager': 'service manager',
    r'(?<!assistant )sales manager': 'sales manager',
    r'(?<!ai )product manager': 'product manager',
    r'ai product manager': "AI Product Manager",
    r'office manager': 'office manager',
    r'^(?!.*\b(architecture|electrical|mechanical)\b).*office engineer.*': 'office engineer',
    r'(?i)(?=.*\b(?:mechanical)\b).*\boffice engineer\b.*': 'mechanical office engineer',
    r'(?i)(?=.*\b(?:electrical)\b).*\boffice engineer\b.*': 'electrical office engineer',
    r'(?i)(?=.*\b(?:architecture)\b).*\boffice engineer\b.*': 'architecture office engineer',
    r'it operations': 'IT Support',
    r'(?<!ai )engineering manager': 'engineering manager',
    r'^technical consulting.*': 'technical consulting',
    r'training manager': 'training manager',
    r'^tech lead \(ai/ml\)': "AI/ML Lead",
    r'data scientist': 'data scientist',
    r'^team lead data scientist': "data scientist Lead",
    r'^tax accountant.*': 'Accountant',
    r'^tax & legal.*': 'Accountant',
    r'talent acquisition (specialist|partner|&).*': 'Talent Acquisition Specialist',
    r'^talent acquisition and learning and development specialist': 'Talent Acquisition Specialist',
    r'^talent acquisition .*(manager|head).*': 'Talent Acquisition Manager',
    r'system(s)? engineer.*': 'system engineer',
    r'^(?!.*manager).*supply (chain|planning|demand|analyst).*': 'supply chain analyst',
    r'(?i)(?=.*\b(?:(manager|management))\b).*\bsupply (chain|planning|demand|analyst).*': 'supply chain manager',
    r'supply chain executive': 'supply chain lead',
    r'(?!.*\b(java|(ai/ml)|.net)\b).*^(technical|tech) lead.*': 'Technical Lead',
    r'store manager.*': 'store manager',
    r'(?!.*\b(backend|frontend|mobile|lead|.net)\b).*^software engineer.*': 'software engineer',
    r'quality engineer': 'quality engineer',
    r'system administrator.*' :'system administrator',
    r'testing engineer|tester': 'testing engineer',
    r'software tester': 'testing engineer',
    r'social media moderator*': 'social media moderator',
    r'(technical|tech) lead': 'Technical Lead',
    r'security engineer': 'security engineer',
    'scrum master smart village,cairo,egypt + 1 more product development posted 14 hours ago':'scrum master',
    r'web developer': 'web developer',
    'ux/ui designer': 'ui/ux designer',
    'ui/ux designer': 'ui/ux designer',
    r'sales account manager':'sales account manager',
    r'qa engineer':'qa engineer',
    'product designer':'product designer',
    'product owner (vois)':'product owner',
    'people operations specialist':'people operations specialist',
    'operations engineer':'people operations specialist',
}
#%%
# r'.*\b(architecture|electrical|mechanical)\b.*\boffice engineer\b.*'
# cybersecurity project manager (vois)
regex = 'operations engineer'
# r'^(?!.*\b(architecture|electrical|mechanical)\b).*office engineer.*'
# regex = r'(?i)(?=.*\b(?:(manager|managment))\b).*\bsupply (chain|planning|demand|analyst)\b.*'
df[df.title.str.contains(regex, regex=True) == True][['title', 'description', 'job_level', 'min_num_of_years', 'max_num_of_years']]
#%%
for pattern, replacement in replace_dict.items():
    df.title[df.title.str.contains(pattern, regex=True)] = replacement
#%%
df.title.value_counts()
#%%
df = df.sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)