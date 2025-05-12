#%% md
# ### Import required libraries
# 
# - Import `clean_data` module from `scripts`.
# - Import `sqlite3` for database interaction.
# - Import `warnings` and disable warnings.
# - Import `pandas` for data manipulation.
#%%
from scripts.clean_data import *
from scripts.analysis import *
import sqlite3
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
#%% md
# ### Load and preview data
# 
# - Load CSV file `egypt_raw.csv`,`saudi-arabia_raw.csv` from `../data/raw/` into DataFrame.
# - Display first 5 rows of the DataFrame.
#%%
df_egypt = pd.read_csv('data/raw/egypt_raw.csv')
df_egypt.head()
#%%
df_saudi = pd.read_csv('data/raw/saudi-arabia_raw.csv')
df_saudi.head()
#%% md
# ### Split location and career_level columns
# 
# - Split `location` column by separator `·`, keep index 1 as `city`.
# - Split `career_level` column by separator `·`, keep indexes 0, 1, 2 as `type`, `exp`, and `no_exp`.
# - Further process `career_level` column using `split_career_level` function.
#%%
split_column(df_egypt, 'location', [1], '·', ['city'], reverse=True)
split_career_level(df_egypt)
df_egypt.head(15)
#%%
split_column(df_saudi, 'location', [1], '·', ['city'], reverse=True)
split_career_level(df_saudi)
df_saudi.head(15)
#%% md
# ### Clean and combine experience columns
# 
# - Replace 'Unknown' values in `exp` column with `NaN`.
# - Combine `experience` column with `exp` column into a new column `experience_` using `combine_first`.
# - Replace 'Unknown' values in `no_exp` column with `NaN`.
# - Combine `num_of_exp` column with `no_exp` column into a new column `num_of_exp_years` using `combine_first`.
#%%
df_egypt['exp'].replace('Unknown', np.nan, inplace=True)
df_egypt['experience_'] = df_egypt['experience'].combine_first(df_egypt['exp'])
df_egypt['no_exp'].replace('Unknown', np.nan, inplace=True)
df_egypt['num_of_exp_years'] = df_egypt['num_of_exp'].combine_first(df_egypt['no_exp'])
df_egypt.head(15)
#%%
df_saudi['exp'].replace('Unknown', np.nan, inplace=True)
df_saudi['experience_'] = df_saudi['experience'].combine_first(df_saudi['exp'])
df_saudi['no_exp'].replace('Unknown', np.nan, inplace=True)
df_saudi['num_of_exp_years'] = df_saudi['num_of_exp'].combine_first(df_saudi['no_exp'])
df_saudi.head(15)
#%% md
# ### Split and Clean Columns
# 
# 1. **Split `industry` column** using the `split_industry` function.
# 2. **Split `location` column**:
#    - Extract the city from the `location` column by splitting at '·'.
#    - The resulting values are stored in the new `city` column, reversing the split.
# 3. **Split `num_of_vacancies` column**:
#    - Extract the number of vacancies by splitting at a space (' ').
#    - Fill missing values with `1` if no vacancies are specified.
#%%
split_industry(df_egypt)
split_column(df_egypt, 'location', index=[1], split_char='·', names=['city'], reverse=True)
split_column(df_egypt, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
df_egypt.head(15)
#%%
split_industry(df_saudi)
split_column(df_saudi, 'location', index=[1], split_char='·', names=['city'], reverse=True)
split_column(df_saudi, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
df_saudi.head(15)
#%% md
# ### Fill Missing Values in Columns
# 
# 1. **Fill missing values in the `remote` column** with `'من المقر'` to indicate office-based positions.
# 2. **Fill missing values in the `age` column** with `'لا تفضيل'` to represent no preference regarding age.
# 3. **Fill missing values in the `sex` column** with `'لا تفضيل'` to represent no preference regarding sex.
# 4. **Fill missing values in the `experience_` column** with `'لا تفضيل'` to represent no preference regarding experience.
# 5. **Fill missing values in the `num_of_exp_years` column** with `'لا تفضيل'` to represent no preference regarding years of experience.
#%%
df_egypt['remote'].fillna('من المقر', inplace=True)
df_egypt['age'].fillna('لا تفضيل', inplace=True)
df_egypt['sex'].fillna('لا تفضيل', inplace=True)
df_egypt['experience_'].fillna('لا تفضيل', inplace=True)
df_egypt['num_of_exp_years'].fillna('لا تفضيل', inplace=True)
df_egypt.head(15)
#%%
df_saudi['remote'].fillna('من المقر', inplace=True)
df_saudi['age'].fillna('لا تفضيل', inplace=True)
df_saudi['sex'].fillna('لا تفضيل', inplace=True)
df_saudi['experience_'].fillna('لا تفضيل', inplace=True)
df_saudi['num_of_exp_years'].fillna('لا تفضيل', inplace=True)
df_saudi.head(15)
#%% md
# ### Drop Unnecessary Columns
# 
#  * **Remove columns** from the DataFrame that are not needed for further analysis:
#    - `age`, `exp`, `no_exp`, `num_of_exp`, `experience`, `career_level`, `industry`, `location`, `link`, `Unnamed: 0`, `salary`, `nationality`, `residence_area`, `qualification`, `specialization`.
#%%
df_egypt.drop(
    columns=['age', 'exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link',
             'Unnamed: 0', 'salary', 'nationality', 'residence_area', 'qualification', 'specialization'],
    inplace=True)
df_egypt.head(15)
#%%
df_saudi.drop(
    columns=['age', 'exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link',
             'Unnamed: 0', 'salary', 'nationality', 'residence_area', 'qualification', 'specialization'],
    inplace=True)
df_saudi.head(15)
#%% md
# ### Analyze Date Data
# 
# * **Call `analyses_date()` function** to analyze the date data in the DataFrame (`df`):
#    - Parameter `num_days=120` specifies the number of days to consider for analysis.
#%%
analyses_date(df_egypt, num_days=120)
df_egypt.head(15)
#%%
analyses_date(df_saudi, num_days=120)
df_saudi.head(15)
#%% md
# ### Sort and Save Data
# 
# 1. **Sort the DataFrame** by the 'title' column in descending order:
#    - The `ascending=False` argument sorts the data in descending order.
# 
# 2. **Save the DataFrame to an SQLite database** (commented-out code)
# 
#%%
df_egypt.sort_values(by=['title'], ascending=False, inplace=True)
# conn = sqlite3.connect('../database.db')
# df.to_sql('EGYPT', con=conn, if_exists='replace', index=False)
#%%
df_saudi.sort_values(by=['title'], ascending=False, inplace=True)
# sqlite_version = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=sqlite_version, if_exists='replace', index=False)
#%% md
# ### Manual Data Cleaning and Translation
# 
# 1. **Manual Cleaning of 'title' Column**:
#    - Some manual adjustments were made to the 'title' column before starting the translation.
# 
# 2. **Translate the 'title' Column**:
#    - After the manual cleaning, the translation was applied to the 'title' column for the first 400 rows using the `apply_translation` function.
# 
# 3. **Save the Data**
#%%
df_egypt = pd.read_csv('data/processed/egypt_clean.csv')
df_egypt.sort_values(by=['title'], ascending=False, inplace=True)
apply_translation(df_egypt, 'title', rows=df_egypt.iloc[:40, :].index.tolist())
#%%
df_egypt = df_egypt[~df_egypt['title'].str.contains('سعودية', na=False)]
df_egypt = df_egypt[~df_egypt['title'].str.contains('سعوديه', na=False)]
df_egypt = df_egypt[~df_egypt['title'].str.contains('سعوية', na=False)]
df_egypt = df_egypt[~df_egypt['title'].str.contains('saudi arabia', na=False)]
df_egypt = df_egypt[~df_egypt['title'].str.contains('saudi', na=False)]
#%%
df_saudi = pd.read_csv('data/processed/saudi_arabia.csv')
df_saudi.sort_values(by=['title'], ascending=False, inplace=True)
apply_translation(df_saudi, 'title', rows=df_saudi.iloc[:400, :].index.tolist())
#%% md
# ### Data Transformation Process
# 
# 1. **Manual Update on 'experience_' Column**:
#    - Updated rows where 'type' contains the word "تدريب" to set 'experience_' to 'خريج جديد' (New Graduate).
# 
# 2. **Translation**:
#    - Translated 'experience_', 'type', 'sex', and 'remote' using respective translation functions.
# 
# 3. **Gender Extraction**:
#    - Extracted gender information from 'title', 'description', and 'skills'.
# 
# 4. **Remote Work Extraction**:
#    - Extracted remote work information from 'title', 'description', and 'skills'.
# 
# 5. **Drop Irrelevant Columns**:
#    - Dropped 'description' and 'skills' columns.
# 
# 6. **Split 'num_of_exp_years' Column**:
#    - Split and processed the 'num_of_exp_years' column.
# 
# 7. **Save the Data**
#%%
df_egypt = pd.read_csv('data/processed/egypt_clean.csv')
df_saudi = pd.read_csv('data/processed/saudi_arabia.csv')
#%%
translate_experience(df_egypt)
translate_type(df_egypt)
translate_sex(df_egypt)
translate_remote(df_egypt)
#%%
extract_job_grade(df_egypt)
extract_gender(df_egypt, 'title')
extract_gender(df_egypt, 'description')
extract_gender(df_egypt, 'skills')
extract_remotely(df_egypt, 'title')
extract_remotely(df_egypt, 'description')
extract_remotely(df_egypt, 'skills')
#%%
df_egypt.drop(columns=['description', 'skills'], inplace=True)
split_num_of_exp_years(df_egypt)
conn = sqlite3.connect('../database.db')
# df.to_sql('EGYPT', con=conn, if_exists='replace', index=False)
conn.close()
df_egypt.head(15)
#%%
index = df_saudi.type.str.contains(r'تدريب', regex=True)
df_saudi.loc[index, 'experience_'] = 'خريج جديد'
#%%
translate_experience(df_saudi)
translate_type(df_saudi)
translate_sex(df_saudi)
translate_remote(df_saudi)
#%%
extract_job_grade(df_saudi)
extract_gender(df_saudi, 'title')
extract_gender(df_saudi, 'description')
extract_gender(df_saudi, 'skills')
extract_remotely(df_saudi, 'title')
extract_remotely(df_saudi, 'description')
extract_remotely(df_saudi, 'skills')
#%%
df_saudi.drop(columns=['description', 'skills'], inplace=True)
split_num_of_exp_years(df_saudi)
conn = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace', index=False)
conn.close()
df_saudi.head(15)
#%% md
# ### Data Transformation Steps for 'title' Column
# 
# 1. **Remove Leading Numbers**:
#    - Removed leading numbers and periods (e.g., "1.", "2."), and stripped any leading or trailing spaces.
# 
# 2. **Remove Leading "a"**:
#    - Removed any instance of the letter "a" at the beginning of the title followed by a space.
# 
# 3. **Convert to Lowercase**:
#    - Converted all titles to lowercase for consistency.
# 
# 4. **Sort Titles**:
#    - Sorted the titles alphabetically in ascending order.
#%%
conn = sqlite3.connect('data/database.db')
df_egypt = pd.read_sql('SELECT * FROM EGYPT', conn)
df_saudi = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
#%%
df_egypt['title'] = df_egypt['title'].str.replace(r'^\d+\.', '', regex=True).str.strip()
df_egypt['title'] = df_egypt['title'].str.replace(r'^a\s\b', '', regex=True).str.strip()
df_egypt.title = df_egypt.title.str.lower()
df_egypt.sort_values(by=['title'], inplace=True)
df_egypt.head(15)
#%%
df_saudi['title'] = df_saudi['title'].str.replace(r'^\d+\.', '', regex=True).str.strip()
df_saudi['title'] = df_saudi['title'].str.replace(r'^a\s\b', '', regex=True).str.strip()
df_saudi.title = df_saudi.title.str.lower()
df_saudi.sort_values(by=['title'], inplace=True)
df_saudi.head(15)
#%% md
# ### Job Title Cleaning Process
# 
# 1. **Pattern Replacement**:
#    - Applied a regular expression pattern to remove unwanted terms like "sr", "ssr", "senior", "junior", "staff", gender-related terms (e.g., "male", "female"), and specific job rank indicators (e.g., "trainee", "graduate").
#    - Cleaned up job titles to ensure they follow the correct format without extra symbols, spaces, or unnecessary words.
# 
# 2. **Title Editing**:
#    - Applied a predefined title mapping (`edite_title_mapping`) to standardize job titles, ensuring consistency across the dataset (e.g., "cashier" becomes "cashier", "driller" becomes "drilling operator").
# 
# 3. **Save the Data**:
#    - The cleaned titles were saved back into the database for further analysis, ensuring all records follow the standardized format.
#%%
final_mapping_title_egypt = {
    r'3d designer': '3d designer',
    r'^account director': 'account director',
    r'account executive': 'account executive',
    r'account management': 'account management',
    r'(?=.*(account))(?=.*(receivable))': 'account receivable',
    r'ai engineer\b': 'ai engineer',
    r'^ai$': 'ai engineer',
    r'(?=.*(account))(?=.*(manage))^(?!.*(?:sale|hr\b|humanresources|humansresources|human\s*resources|humans\s*resources|market|trade)).*': 'account manager',
    r'^account payable accountant.*': 'account payable accountant',
    r'^account receivable.*': 'account receivable',
    r'^accounting (& financial|& reporting|manager).*': 'accounting manager',
    r'^accounting (section|supervisor|team|assistant|advisory).*': 'accounting supervisor',
    r'^accounting intern.*?': 'accountant',
    r'^accounts payable.*': 'accounts payable',
    r'^accounts receivable.*': 'accounts receivable',
    r'^accounts supervisor.*': 'accounts receivable supervisor',
    r'^accountant.*(?!.*(?:receivable))': 'accountant',
    r'^tax accountant.*': 'accountant',
    r'^tax & legal.*': 'accountant',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(ad|campaign))': 'ad operations manager',
    r'(?=.*(admin))(?=.*(assistant))': 'account assistant',
    r'administrative assistant': 'administrative assistant',
    r'ai product manager': 'ai product manager',
    r'(?=.*(machine learning|ml|machinelearning))(?=.*(engineer))^(?!.*(?:mlops|ops)).*': 'ai/ml engineer',
    r'^analyst': 'analyst',
    r'application specialist': 'application specialist',
    r'architectural engineer': 'architectural engineer',
    r'(?=.*engineer)(?=.*architectur)': 'architectural engineer',
    r'architecture (- co-op trainee|engineer)': 'architecture engineer',
    r'area manager': 'area manager',
    r'art director': 'art director',
    r'assistant director': 'assistant director',
    r'assistant manager': 'assistant manager',
    r'assistant project manager': 'assistant project manager',
    r'assurance - external audit(?!.*manager)': 'assurance - external audit',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(audit))': 'audit operations specialist',
    r'area sales manager': 'area sales manager',
    r'area sales engineer': 'area sales engineer',
    r'area security manager': 'area security engineer',
    r'automation testing engineer': 'automation testing engineer',
    r'associate customer success manager': 'associate customer success manager',
    r'assistant sales manager': 'assistant sales manager',
    r'ar accountant': 'accountant',
    r'arabic english interpreter': 'arabic english interpreter',
    #-------------------------------------------------------------------------
    r'backend developer': 'backend developer',
    r'(?=.*(developer))(?=.*backend)^(?!.*(?:lead|manager|test automation)).*': 'backend developer',
    r'^web developer$': 'fullstack developer',
    r'(?=.*(web developer))^(?!.*(?:full stack)).*': 'backend developer',
    r'^barista': 'barista',
    r'(?=.*(bim))(?=.*(structur))': 'bim structure engineer',
    r'(?<!associate )business analyst': 'business analyst',
    r'^business development(\\s-|$)': 'business development',
    r'business development executive': 'business development executive',
    r'business development lead': 'business development lead',
    r'(business development [a-z]+ manager)|(business development manager)|(manager .* business development)': 'business development manager',
    r'business development representative': 'business development representative',
    r'(business development specialist)|(specialist .* business development)': 'business development specialist',
    r'^business support(?!.*manager)': 'business support',
    r'brand manager': 'brand manager',
    r'(?=.*(development))(?=.*(business))^(?!.*(?:manager|lead|office|director|executive|representative|specialist|associate)).*': 'business development',
    r'(?=.*(intelligence))(?=.*(engineer))(?=.*(business))': 'business intelligence engineer',
    r'(?=.*(research))(?=.*(business))^(?!.*(?:manager|lead)).*': 'business research',
    r'(?=.*(research))(?=.*(business))^(?=.*(manager))': 'business research manager',
    r'(?=.*(research))(?=.*(business))^(?=.*(lead))': 'business research lead',
    #-------------------------------------------------------------------------
    r'(?=.*(call))(?=.*(center))^(?!.*(?:manager|lead)).*': 'call center agent',
    r'(?=.*(call))(?=.*(center))^(?=.*(lead))': 'call center lead',
    r'(?=.*(call))(?=.*(center|centre))^(?=.*(manager))': 'call center manager',
    r'cashier': 'cashier',
    r'category manager': 'category manager',
    r'(?=.*(ceo))': 'ceo assistant',
    r'^(?!.*demi).*chef de partie': 'chef de partie',
    r'(?=.*(chief))(?=.*(accountant))': 'chief accountant',
    r'chief concierge': 'chief concierge',
    r'^(?!.*assistant).*chief engineer': 'chief engineer',
    r'civil 3d': 'civil 3d',
    r'(?=.*engineer)(?=.*civil)^(?!.*(?:mechanical|manager|structure)).*': 'civil engineer',
    r'client partner manager': 'client partner manager',
    r'cluster director': 'cluster director',
    r'commercial manager': 'commercial manager',
    r'commi( |s |s$)': 'commis',
    r'compliance manager': 'compliance manager',
    r'^(?!.*(?:chief|trade|payroll|tax)).*compliance officer': 'compliance officer',
    r'^(?!.*(?:manager|senior)).*^consulting': 'consulting',
    r'^consulting.*senior manager': 'consulting senior manager',
    r'content (creator|maker)': 'content creator',
    r'content (writer|researcher)': 'content writer',
    r'^contract(s)? specialist': 'contract specialist',
    r'contract(s)? engineer': 'contracts engineer',
    r'controls engineer': 'controls engineer',
    r'^coordinator': 'coordinator',
    r'copywriter': 'copywriter',
    r'^cost control engineer': 'cost control engineer',
    r'^counsel': 'counsel',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(customer))': 'customer operations manager',
    r'customer service executive': 'customer service executive',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(lost\\s+and\\s+found))': 'customer service specialist',
    r'cyber security': 'cyber security',
    'captian': 'captain',
    'center quality manager': 'center quality manager',
    'channel management': 'channel management',
    '^consultant.*': 'consultant',
    r'^(consulting)(?!.*(?:manager|quality|lead)).*': 'consultant',
    r'^(?=.*(content))(?=.*(specialist))^(?!.*(?:marketing|photo)).*': 'content specialist',
    r'(?=.*(customer))(?=.*(representative))': 'customer representative',
    r'(?=.*(customer))(?=.*(service))': 'customer service',
    r'(?=.*(customer))(?=.*(support))(?=.*(specialist))': 'customer support specialist',
    r'(?=.*(customer))(?=.*(experience))(?=.*(specialist))': 'customer experience specialist',

    r'^data center': 'data center engineer',
    r'(?=.*(data))(?=.*(analy))^(?!.*(?:manager|quality|lead)).*': 'data analyst',
    r'database expert': 'database engineer',
    r'^data engineer': 'data engineer',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(data|collection))': 'data operations specialist',
    r'data scientist': 'data scientist',
    r'^team lead data scientist': 'data scientist lead',
    r'demi chef de partie': 'demi chef de partie',
    r'^design engineer': 'design engineer',
    r'^design manager': 'design manager',
    r'^developer': 'developer',
    r'^(?!.*(?:lead)).*^devops engineer': 'devops engineer',
    r'(?=.*(engineer))(?=.*(devops))(?=.*(operations|operation))': 'devops operations engineer ',
    r'^director .*(finance|faas)': 'director – finance',
    r'^document controller': 'document controller',
    r'data integrat': 'data integration developer',
    r'(?=.*(data))(?=.*(management))(?=.*(consultant))': 'data management consultant',
    r'(?=.*(data))(?=.*(quality))': 'data quality analyst',
    r'(?=.*(data))(?=.*(scien))^(?!.*(?:manager|director)).*': 'data scientist',
    r'demi coding instructor physical': 'demi coding instructor physical',
    r'(?=.*(digital))(?=.*(marketing))(?=.*(specialist))': 'digital marketing specialist',
    'draftsman': 'draftsman',
    #-------------------------------------------------------------------------
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(ecommerce|b2b))': 'ecommerce operations manager',
    r'(?=.*(electrical))(?=.*(design))(?=.*(engineer))': 'electrical design engineer',
    r'(?=.*(electrical))(?=.*(engineer))^(?!.*(?:lead|design|support|office|maintenance)).*': 'electrical design engineer',
    r'(?i)(?=.*\\b(?:electrical)\\b).*\\boffice engineer\\b.*': 'electrical office engineer',
    r'(?=.*(electrical))(?=.*(technical))(?=.*(office))(?=.*(engineer))': 'electrical technical office engineer',
    r'energy analyst': 'energy analyst',
    r'(?=.*engineer)(?=.*manager)^(?!.*(?:department|and|data|neighborhoods|mechanical|design|interface|cloud|area|divisional|project|software|technical|solution|&|sales|fire)).*': 'engineer manager',
    r'(?=.*engineer)(?=.*planning)^(?!.*(?:strategic|and|master|maintenance|electrical|lead)).*': 'engineer planning',
    r'(?<!ai )engineering manager': 'engineering manager',
    r'(?=.*estimator)': 'estimator',
    r'(?=.*execution)(?=.*manager)': 'execution manager',
    r'(?=.*e-commerce)(?=.*manager)': 'e-commerce manager',
    r'(?=.*executive)(?=.*assistan)^(?!.*(?:manager|front|and)).*': 'executive assistant',
    r'(?=.*executive)(?=.*chef)^(?!.*(?:pastry|sous)).*': 'executive chef',
    r'(?=.*expeditor)': 'expeditor',
    r'engineer \(r\&d\)': 'engineer',
    #-------------------------------------------------------------------------
    r'(?=.*finance controller)': 'finance controller',
    r'(?=.*^finance)(?=.*manager)': 'finance manager',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(finance))': 'finance operations manager',
    r'(?<!lead )financial analyst': 'financial analyst',
    r'(?=.*front)(?=.*office)(?=.*agent)': 'front office agent',
    r'(?=.*front)(?=.*office)(?=.*manager)': 'front office manager',
    r'(?=.*(developer))(?=.*(frontend|front end|front\-end))^(?!.*(?:lead|manager|test automation)).*': 'frontend developer',
    r'(?=.*(developer))(?=.*(fullstack|full stack|full\-stack))^(?!.*(?:lead|manager|test automation)).*': 'fullstack developer',
    r'(?=.*(web developer))^(?!.*(?:php)).*': 'fullstack developer',
    r'(?=.*(developer))(?=.*((fullstack|full stack|full\-stack)|full stack))(?=.*lead)': 'fullstack developer lead',
    r'(?=.*(engineer))(?=.*(fullstack|full stack|full\-stack))(?=.*lead)': 'fullstack engineer lead',
    r'finance director': 'finance director',
    r'data collector': 'data collector',
    r'(?=.*(finance))(?=.*(account))^(?!.*(?:manager)).*': 'finance account',
    r'(?=.*(financ))(?=.*(controller))': 'finance controller',
    r'(?=.*(financ))(?=.*(planning))(?=.*(analysis))^(?!.*(?:head)).*': 'finance planning analysis manager',
    r'first mile hub supervisor': 'first mile hub supervisor',
    r'food and beverage manager': 'food and beverage manager',
    r'fp&a analyst': 'fp&a analyst',
    r'(?=.*(front))(?=.*(desk))^(?!.*(?:manager|officer|supervisor|clerk|receptionist)).*': 'front desk agent',
    #-------------------------------------------------------------------------
    r'(?=.*government)(?=.*(relation))(?=.*officer)^(?!.*&).*': 'government relation officer',
    r'(?=.*graphic)(?=.*(design))^(?!.*(?:and|manager|concept|specialist)).*': 'graphic design',
    r'(?=.*guest)(?=.*(experience))(?=.*agent)': 'guest experience agent',
    r'general accountant': 'general accountant',
    r'global procurement associate analyst': 'global procurement associate analyst',
    #-------------------------------------------------------------------------
    r'(?=.*(hr))(?=.*(account\\s+manager))': 'hr account manager',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(specialist))(?=.*(admin|payroll))': 'hr admin & payroll specialist',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(analyst))': 'hr analyst',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(business\\s*partner))': 'hr business partner',
    r'(?=.*(hr))(?=.*(service\\s+delivery))(?=.*(compensation|benefit))': 'hr compensation & benefits associate',
    r'(?=.*(hr))(?=.*(coordinator))': 'hr coordinator',
    r'(?=.*(director))(?=.*(human\\s*resources))^(?!.*(?:assistant)).*': 'hr director',
    r'(?=.*(hr))(?=.*(employer\\s+branding|marketing))': 'hr employer branding specialist',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(generalist))': 'hr generalist',
    r'(?=.*(head))(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))': 'hr head',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(intern|graduate))': 'hr intern',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(lead))': 'hr lead',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(manager))': 'hr manager',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(officer|executive))': 'hr officer',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(specialist))(?=.*(resourcing|recruitment))': 'hr recruitment specialist',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(people|hr))': 'hr specialist',
    r'(?=.*(hr\b|humanresources|humansresources|human\s*resources|humans\s*resources))(?=.*(specialist))': 'hr specialist',
    r'(?=.*(hr))(?=.*(application|process|pmo))': 'hr systems/process specialist',
    r'(?=.*(hr))(?=.*(partner))(?=.*(talent|performance))': 'hr talent partner',
    r'(?=.*(hub))(?=.*(operations))(?=.*(coordinator))^(?!.*(?:section head|manager)).*': 'hub operations coordinator',
    r'a427-esg': 'hvac technician',
    #-------------------------------------------------------------------------
    r'(?=.*(information))(?=.*(security))^(?!.*(?:section head|manager)).*': 'information security',
    r'(?=.*(integration))(?=.*(developer))': 'integration developer',
    r'(?=.*(interior))(?=.*(designer))': 'interior designer',
    r'(?=.*(design))(?=.*(interior))^(?!.*(?:manager)).*': 'interior designer',
    r'(?=.*(audit))(?=.*(internal))': 'internal auditor',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(technology|it))': 'it operations manager',
    r'it operations': 'it support',
    #-------------------------------------------------------------------------
    r'(?=.*(java))(?=.*(developer))': 'java developer',
    r'(?=.*(java))(?=.*(engineer))': 'java engineer',
    #-------------------------------------------------------------------------
    r'7pqe\\+ dispute resolution associate': 'legal counsel',
    r'(?=.*(logistics))(?=.*(coordinator))^(?!.*(?:section head|manager)).*': 'logistics coordinator',
    r'(?=.*(logistics))(?=.*(coordintor|coordinatoor|coordinator))': 'logistics coordinator',
    #-------------------------------------------------------------------------
    r'maintenance technician': 'maintenance technician',
    r'marketing manager': 'marketing manager',
    r'(?=.*(marketing))(?=.*(manager))': 'marketing manager',
    r'(?=.*engineer)(?=.*mechanical)^(?!.*(?:electrical|manager|design|reliability|civil|maintenance|lead)).*': 'mechanical engineer',
    r'(?=.*engineer)(?=.*mechanical)^(?!.*(?:manager|design|reliability|civil|maintenance|lead)).*': 'mechanical engineer',
    r'(?i)(?=.*\\b(?:mechanical)\\b).*\\boffice engineer\\b.*': 'mechanical office engineer',
    r'(?=.*(medical))(?=.*(assistant))^(?!.*(?:manager|design|reliability|civil|maintenance|lead)).*': 'media assistant',
    r'(?=.*(medical))(?=.*(assistant))': 'media assistant lead',
    r'(?=.*(media))(?=.*(buyer))^(?!.*(?:manager|design|reliability|civil|maintenance|lead)).*': 'media buyer',
    r'(?=.*(media))(?=.*(buyer|buying))(?=.*(lead))': 'media buyer lead',
    r'medical representative': 'medical representative',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(merchant|vendor))': 'merchant operations manager',
    r'(?=.*(developer))(?=.*(mobile|ios|android|flutter))^(?!.*(?:lead|manager|test automation)).*': 'mobile developer',
    r'(?=.*(developer))(?=.*mobile)(?=.*lead)': 'mobile developer lead',
    r'(?=.*(developer))(?=.*mobile)(?=.*manager)': 'mobile developer manager',
    r'(?=.*(developer))(?=.*mobile)(?=.*test automation)': 'mobile developer test automation',
    r'(?=.*(engineer))(?=.*mobile)(?=.*lead)': 'mobile engineer lead',
    r'(?=.*(engineer))(?=.*mobile)(?=.*manager)': 'mobile engineer manager',
    r'(?=.*(engineer))(?=.*mobile)(?=.*test automation)': 'mobile engineer test automation',
    #-------------------------------------------------------------------------
    r'odoo developer': 'odoo developer',
    r'^(?!.*\\b(architecture|electrical|mechanical)\\b).*office engineer.*': 'office engineer',
    r'(?=.*(manager))(?=.*(office))^(?!.*(?:assistant)).*': 'office manager',
    r'^(?!.*\\b(cyber security|cybersecurity|devops)\\b).*operations engineer.*': 'operations engineer',
    r'(?=.*(engineer))(?=.*(operations|operation))^(?!.*(?:devops)).*': 'operations engineer',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))^(?!.*(sales|strategic|data|lost|live|hardware|hub|finance|financial|mall|retail|product|strategy|planning|technology|it|security|soc|merchant|customer|ad|ecommerce|b2b|gym|fitness|procurement)).*': 'operations manager',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))^(?!.*(sales|strategic|data|lost|live|hardware|hub|finance|financial|mall|retail|product|strategy|planning|technology|it|security|soc|merchant|customer|ad|ecommerce|b2b|gym|fitness|procurement)).*': 'operations specialist',
    r'data collection': 'operations specialist data collection',
    #-------------------------------------------------------------------------
    r'people operations specialist': 'people operations specialist',
    r'(?=.*(personal))(?=.*(assistant))': 'personal assistant',
    r'(?=.*(personal))(?=.*(banker))^(?!.*(?:payroll)).*': 'personal banker',
    r'(?=.*(pharmacist))': 'pharmacist',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(procurement))': 'procurement operations manager',
    r'product designer': 'product designer',
    r'(?<!ai )product manager': 'product manager',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(product))': 'product operations manager',
    r'product owner (vois)': 'product owner',
    r'project manager (architect or civil engineer)': 'project manager engineer',
    r'(?=.*(purchase|purchasing))(?=.*(specialist))': 'purchasing specialist',
    #-------------------------------------------------------------------------
    r'qa engineer': 'qa engineer',
    r'quality engineer': 'quality engineer',
    #-------------------------------------------------------------------------
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(retail))': 'retail operations manager',
    #-------------------------------------------------------------------------
    r'sales and business development manager': 'sales & business development manager',
    r'sales account manager': 'sales account manager',
    r'sales assistant(?!.*analyst)': 'sales assistant',
    r'sales development representative': 'sales development representative',
    r'sales director': 'sales director',
    r'sales executive': 'sales executive',
    r'(?<!assistant )sales manager': 'sales manager',
    r'sales manager / account manager': 'sales manager / account manager',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(sales))': 'sales operations specialist',
    r'(?=.*(sales))(?=.*(support))(?=.*(specialist))': 'sales operations specialist',
    r'scrum master smart village,cairo,egypt + 1 more product development posted 14 hours ago': 'scrum master',
    r'security engineer': 'security engineer',
    r'service manager': 'service manager',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(security|soc))': 'soc manager',
    r'social media moderator*': 'social media moderator',
    r'(?!.*\\b(backend|frontend|front end|front\-end|mobile|lead|.net)\\b).*^software engineer.*': 'software engineer',
    r'(?=.*(engineer|engineering))(?=.*backend)^(?!.*(?:lead|manager|test automation)).*': 'software engineer backend',
    r'(?=.*software)(?=.*(engineer|engineering))(?=.*backend)^(?!.*(?:lead|manager|test automation)).*': 'software engineer backend',
    r'(?=.*software)(?=.*(engineer|engineering))(?=.*backend)(?=.*lead)': 'software backend engineer  lead',
    r'(?=.*software)(?=.*(engineer|engineering))(?=.*(frontend|front end|front\-end))': 'software frontend engineer',
    r'(?=.*(engineer|engineering))(?=.*frontend)': 'software frontend engineer',
    r'(?=.*(engineer|engineering))(?=.*(fullstack|full stack|full\-stack))^(?!.*(?:lead|manager|test automation)).*': 'software engineer fullstack',
    r'(?=.*software)(?=.*(engineer|engineering))(?=.*(fullstack|full stack|full\-stack))^(?!.*(?:lead|manager|test automation)).*': 'software engineer fullstack',
    r'(?=.*software)(?=.*(engineer|engineering))(?=.*(mobile|ios|android|flutter))': 'software mobile engineer',
    r'(?=.*(engineer|engineering))(?=.*(mobile|ios|android|flutter))': 'software mobile engineer',
    r'store manager.*': 'store manager',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(strategy|planning))': 'strategy & operations manager',
    r'^(?!.*manager).*supply (chain|planning|demand|analyst).*': 'supply chain analyst',
    r'supply chain executive': 'supply chain lead',
    r'(?i)(?=.*\\b(?:(manager|management))\\b).*\\bsupply (chain|planning|demand|analyst).*': 'supply chain manager',
    r'technical support': 'support engineer',
    r'support engineer': 'support engineer',
    r'technical support &': 'support manager',
    r'system administrator.*': 'system administrator',
    r'system(s)? engineer.*': 'system engineer',
    r'(?=.*(Account))(?=.*(Manager))(?=.*(Sale))': 'Sales Account Manager',
    #-------------------------------------------------------------------------
    r'^talent acquisition .*(manager|head).*': 'talent acquisition manager',
    r'talent acquisition (specialist|partner|&).*': 'talent acquisition specialist',
    r'^talent acquisition and learning and development specialist': 'talent acquisition specialist',
    r'^technical consulting.*': 'technical consulting',
    r'(?!.*\\b(java|(ai/ml)|.net)\\b).*^(technical|tech) lead.*': 'technical lead',
    r'(technical|tech) lead': 'technical lead',
    r'testing engineer|tester': 'testing engineer',
    r'software tester': 'testing engineer',
    r'training manager': 'training manager',
    r'^treasury senior accountant': 'treasury accountant',
    r'^treasury (section|head).*': 'treasury lead',
    r'^treasurer$': 'treasury specialist',
    r'^treasur(y|er)\\s?(specialist|senior specialist|and| - emea).*': 'treasury specialist',
    #-------------------------------------------------------------------------
    r'(?=.*(designer))(?=.*(ux/ui|ui/ux|ux|ui))': 'ux/ui designer',
    r'(?=.*(developer))(?=.*(ux/ui|ui/ux|ux|ui))': 'ux/ui developer',
    #-------------------------------------------------------------------------
}
df_egypt.title.value_counts()
#%%
final_mapping_title_saudi = {
    r'cashier': 'cashier',
    r'driller': 'drilling Operator',
    r'marketing manager': 'marketing manager',
    r'project manager (architect or civil engineer)': 'project manager engineer',
    r'(?<!project manager )civil engineer': 'civil engineer',
    r'(?<!lead )financial analyst': 'financial analyst',
    r'lead financial analyst': 'financial analyst',
    r'"Onshore Oil Driller" OR "Driller"': r'driller',
    r'3d designer': '3d designer',
    r'7pqe\+ dispute resolution associate': 'legal counsel',
    r'a427-esg': 'HVAC Technician',
    r'accelerated command': 'first officer',
    r'accelerator manager': 'accelerator manager',
    r'account development - s8': 'account development',
    r'^account director': 'account director',
    r'account executive': 'account executive',
    r'account management': 'account management',
    r'sales manager / account manager': 'sales manager / account manager',
    r'(?<!sales manager / )account manager': 'account manager',
    r'account receivable': 'account receivable',
    r'account solutions engineer': 'account solutions engineer',
    r'accounting associate': 'accounting associate',
    r'accounting (\(intern\)|- co-op trainee)': 'accounting',
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
    r'^architect\b': 'architect engineer',
    r'application specialist': 'application specialist',
    r'architectural engineer': 'architectural engineer',
    r'area manager': 'area manager',
    r'architecture (- co-op trainee|engineer)': 'architecture engineer',
    r'architecture advisor': 'architecture advisor',
    r'^asset management': 'asset management',
    r'assistant banquet': 'assistant banquet manger',
    r'assistant chief engineer': 'assistant chief engineer',
    r'assistant consultant': 'assistant consultant',
    r'assistant project manager': 'assistant project manager',
    r"assurance - external audit(?!.*manager)": 'assurance - external audit',
    r'assurance - external audit manager': 'assurance - external audit manager',
    r'^barista': 'barista',
    r'(?<!associate )business analyst': 'business analyst',
    r'sales and business development manager': 'sales & business development manager',
    r'business development and partnerships manager': 'business development & partnerships manager',
    r"(business development specialist)|(specialist .* business development)": 'business development specialist',
    r'business development consultant': 'business development consultant',
    r'business development executive': 'business development executive',
    r'business development lead': 'business development lead',
    r'business development representative': 'business development representative',
    r'(business development [a-z]+ manager)|(business development manager)|(manager .* business development)': r'business development manager',
    r'^business development(\s-|$)': 'business development',
    r'^business support(?!.*manager)': 'business support',
    r'^business support manager': 'business support manager',
    r'business system': 'business system analyst',
    r'cafm operator': 'cafm operator',
    r'carpenter': 'carpenter',
    r'cash van sales': 'cash van sales',
    r"(?i)^chief accountant\b": "Chief Accountant",
    r"(?i)^assistant[, ]*accountant\b": "Assistant Accountant",
    r"(?i)^((?!chief|assistant).)*\baccountant\b.*": "Accountant",
    r'assistant director': 'assistant director',
    r'assistant manager': 'assistant manager',
    r"^associate director\b.*": "Associate Director",
    r"^associate manager\b.*": "Associate Manager",
    r"^associate consultant\b.*|associate business & strategy consultant|associate solutions consultant|associate technical consultant": "Associate Consultant",
    r"^associate (project )?manager\b.*": "Associate Project Manager",
    r"^associate (account )?director\b.*": "Associate Director",
    r"^associate (logistics|sales) director\b.*": "Associate Director",
    r"^associate geospatial analyst|associate business analyst|associate underwriter|associate i- reinsurance contract services": "Associate Analyst",
    r"^associate technician\b.*|associate physical therapist": "Associate Technician",
    r"^associate vice president\b.*": "Associate Vice President",
    r"^associate (managing )?consultant\b.*": "Associate Consultant",
    r'call center': 'call center agent',
    r'category manager': 'category manager',
    r'^(?!.*(?:secretary|cofounder)).*ceo': 'ceo',
    r'ceo & cofounder': 'ceo & cofounder',
    r'cet planner': 'cet planner',
    r'chef assistant': 'chef assistant',
    r'chef de cuisine': 'chef de cuisine',
    r'^(?!.*demi).*chef de partie': 'chef de partie',
    r'demi chef de partie': 'demi chef de partie',
    r'chief concierge': 'chief concierge',
    r'^(?!.*assistant).*chief engineer': 'chief engineer',
    r'civil site engineer': 'civil site engineer',
    r'client relations associate': 'client relations associate',
    r'^(?!.*manager).*client partner': 'client partner',
    r'client partner manager': 'client partner manager',
    r'cluster director of learning & quality': 'cluster director of learning & quality',
    r'cluster director of sales': 'cluster director of sales',
    r'commercial manager': 'commercial manager',
    r'commercial sales manager': 'commercial sales manager',
    r'commi( |s |s$)': 'commis',
    r'bids/proposals manager': 'bids/proposals manager',
    r"business continuity (specialist|manager)": "business continuity manager",
    r"business enablement lead": "business enablement lead",
    r"caf(é|e) manager": "cafe manager",
    r"art director": "art director",
    r"backend developer": "backend developer",
    r"^bim s": "bim sme",
    r"civil 3d": "civil 3d",
    r"cluster director": "cluster director",
    r"compliance manager": "compliance manager",
    r"^(?!.*(?:chief|trade|payroll|tax)).*compliance officer": "compliance officer",
    r"construction manager": "construction manager",
    r"construction supervisor": "construction supervisor",
    r"constructions management engineer": "constructions management engineer",
    r"^consultant\s?[^\w] ": "consultant",
    r"consultant anaesthesia": "consultant anaesthesia",
    r"consultant.*(anaesthesia|anesthesia)": "consultant anaesthesia",
    r"consultant ent": "consultant ent surgeon",
    r"consultant medical imaging": "consultant medical imaging",
    r"consultant neurology": "consultant neurology",
    r"consultant (paediatric (intensive care|(cardiac )?icu)|icu|picu)": "consultant paediatric intensive",
    r"consultant spinal": 'consultant spinal surgeon',
    r"consultant plastic": "consultant plastic surgeon",
    r'^(?!.*(?:specialist|senior|management|general|payment)).*^contract(s)? .*manager': 'contract manager',
    r'^(?!.*(?:specialist|senior|management|general|payment)).*^consulting.*manager': 'consulting manager',
    r'contract(s)? management department manager': 'contract management department manager',
    r'^(?!.*(?:manager|senior)).*^consulting': 'consulting',
    r'^consulting.*senior manager': "Consulting Senior Manager",
    r"^contract(s)? specialist": 'contract specialist',
    r"content (creator|maker)": "content creator",
    r"content (writer|researcher)": "content writer",
    r"continuous .*improvement(s)? specialist": "continuous improvements specialist",
    r"contract administrator": 'contract administrator',
    r"contract(s)? advisor": "contract advisor",
    r'^contract(s)? .*(co-op trainee|intern)': 'contract',
    r'contract(s)? engineer': "contracts engineer",
    r'controls engineer': "controls engineer",
    r'cooperative': "cooperative",
    r'^coordinator': "coordinator",
    r'copywriter': "copywriter",
    r'customer care operations specialist': "customer care operations specialist",
    r'credit controller': "credit controller",
    r'country manager': "country manager",
    r'^cost manager': "cost manager",
    r'cost engineer': "cost engineer",
    r'^cost control engineer': "cost control engineer",
    r'^counsel': "counsel",
    r'customer service executive': "customer service executive",
    r'cyber security': "cyber security",
    r'cybersecurity instructor': "cybersecurity instructor",
    r'^data center': "data center engineer",
    r'^data engineer': "data engineer",
    r'data scientist': "data scientist",
    r'database expert': "data database engineer",
    r'^demand planner': "demand plannerr",
    r"department manager - operational excellence": "department manager - operational excellence",
    r"department manager - strategic planning": "department manager - strategic planning",
    r'^design engineer': "design engineer",
    r'design director': "design director",
    r'^design manager': "design manager",
    r'^developer': "developer",
    r'^(?!.*(?:lead)).*^devops engineer': "devops engineer",
    r"director of (sustainability|wellness)": "director – sustainability & wellness",
    r'director of sales': "director – sales & marketing",
    r'director of marketing': "director – marketing",
    r'director (of|–) public': 'director – public relations & communication',
    r'director of (procurement|operations)': "director – procurement/operations",
    r'director.*health': "director – health & safety",
    r"director (of )?(hr|it operations|learning & development|housekeeping)": "director – hr/operations",
    r'director (of )food': "director – food & beverage",
    r'^director .*(finance|faas)': "director – finance",
    r"director - design": "director – design",
    r"director .*city": 'director – city design coordination',
    r'^document controller': 'document controller',
    r'^draftsman': 'draftsman',
    r'duty manager': 'duty manager',
    r'e(-\s?)?commerce specialist.*web administrator': 'ecommerce specialist/web administrator',
    r'electrical design engineer': 'electrical design engineer',
    r'^(?!.*(?:lead)).*^electrical engineer': 'electrical engineer',
    r'electrical supervisor': 'electrical supervisor',
    r'(?=.*electrical)(?=.*technician)': 'electrical technician',
    r'emergency nurse': 'emergency nurse',
    r'energy analyst': 'energy analyst',
    r'(?=.*engineer)(?=.*architectur)': 'architectural engineer',
    r'(?=.*engineer)(?=.*mechanical)^(?!.*(?:electrical|manager|design|reliability|civil|maintenance|lead)).*': 'mechanical engineer',
    r'(?=.*engineer)(?=.*civil)^(?!.*(?:mechanical|manager|structure)).*': 'civil engineer',
    r'(?=.*engineer)(?=.*planning)^(?!.*(?:strategic|and|master|maintenance|electrical|lead)).*': 'engineer planning',
    r'(?=.*engineer)(?=.*manager)^(?!.*(?:department|and|data|neighborhoods|mechanical|design|interface|cloud|area|divisional|project|software|technical|solution|&|sales|fire)).*': 'engineer manager',
    r'(?=.*engineering)(?=.*technician)': 'engineering technician',
    r'(?=.*english)(?=.*teacher)^(?!.*(?:arabic|esl|maths|humanities|perspective|myp)).*': 'english teacher',
    r'^enterprise architect': 'enterprise architect',
    r'(?=.*environmental)(?=.*engineer)': 'environmental engineer',
    r'(?=.*estimator)': 'estimator',
    r'(?=.*event)(?=.*manager)^(?!.*(?:&|project)).*': 'event manager',
    r'(?=.*execution)(?=.*manager)': 'execution manager',
    r'(?=.*executive)(?=.*assistan)^(?!.*(?:manager|front|and)).*': 'executive assistant',
    r'(?=.*executive)(?=.*chef)^(?!.*(?:pastry|sous)).*': 'executive chef',
    r'(?=.*executive)(?=.*pastry)(?=.*chef)': 'executive pastry chef',
    r'(?=.*executive)(?=.*sous)(?=.*chef)': 'executive sous chef',
    r'^executive director': 'executive director',
    r'(?=.*expeditor)': 'expeditor',
    r'(?=.*field)(?=.*marketing)(?=.*specialist)': 'field marketing specialist',
    r'(?=.*front)(?=.*office)(?=.*manager)': 'front office manager',
    r'(?=.*front)(?=.*office)(?=.*agent)': 'front office agent',
    r'(?=.*food)(?=.*beverage)(?=.*server)': 'food & beverage server',
    r'(?=.*field)(?=.*service)(?=.*engineer)': 'field service engineer',
    r'(?=.*field)(?=.*troubleshooter)': 'field troubleshooter',
    r'(?=.*^finance)(?=.*manager)': 'finance manager',
    r'(?=.*finance controller)': 'finance controller',
    r'(?=.*^finance)(?=.*advisor)': 'finance advisor',
    r'(?=.*government)(?=.*(relation))(?=.*officer)^(?!.*&).*': 'government relation officer',
    r'(?=.*guest)(?=.*(experience))(?=.*agent)': 'guest experience agent',
    r'(?=.*guest)(?=.*(experience))(?=.*manager)': 'guest experience manager',
    r'(?=.*graphic)(?=.*(design))^(?!.*(?:and|manager|concept|specialist)).*': 'graphic design',
    r'(?=.*gis)(?=.*(i&c team lead))': 'gis i&c team lead',
    r'(?=.*general)(?=.*(technician))': 'general technician',
    r'(?=.*(design))(?=.*(graphic))': 'graphic designer',
    r'human resources specialist': 'human resources specialist',
    r'human resources coordinator': 'human resources coordinator',
    r"^(?!.*(?:associate)).*human resources business partner": "human resources business partner",
    r'^hse officer': 'hse officer',
    r'^hse manager': 'hse manager',
    r'housekeeping supervisor': 'housekeeping supervisor',
    r'^(hostess($| -)|host)': 'host',
    r'health & safety manager': 'health & safety manager',
    r'^(?!.*(?:and)).*^head of sales': "head of sales",
    r'head baker': 'head baker',
    r'(?=.*(director))(?=.*(human\s*resources))^(?!.*(?:assistant)).*': 'hr director',
    r'(?=.*(hr|human\s*resources))(?=.*(manager))^(?!.*(?:assistant|\&)).*': 'hr manager',
    r'(?=.*(hr|human\s*resources))(?=.*(officer|executive))^(?!.*(?:and|\&)).*': 'hr officer',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(people|hr))': 'hr specialist',
    r'(?=.*(design))(?=.*(interior))^(?!.*(?:manager|decor|/)).*': 'interior designer',
    r'(?=.*(audit))(?=.*(internal))^(?!.*(?:manager|consultant|lead)).*': 'internal auditor',
    r'^integrity engineer': 'integrity engineer',
    r'income auditor': 'income auditor',
    r'incident manager': 'incident manager',
    r'i&c commissioning engineer': 'i&c commissioning engineer',
    r'^(?!.*(?:compliance)).*legal counsel': 'legal counsel',
    r'landscape architect': 'landscape architect',
    r'(?=.*(java))(?=.*(developer))': 'java developer',
    r'(?=.*(java))(?=.*(engineer))': 'java engineer',
    r'middle school teacher': 'middle school teacher',
    r'merchandiser': 'merchandiser',
    r"mep draftsman": "mep draftsman",
    r'^maintenance technician': 'maintenance technician',
    r'^^(?!.*(?:product)).*marketing manager': 'marketing manager',
    r'(?=.*engineer)(?=.*mechanical)^(?!.*(?:manager|design|reliability|civil|maintenance|lead|electrical)).*': 'mechanical engineer',
    r'(?=.*(media))(?=.*(buyer))^(?!.*(?:manager|design|reliability|civil|maintenance|lead)).*': 'media buyer',
    r'medical representative': 'medical representative',
    r'mechanical technician': 'mechanical technician',
    r'mechanical design engineer': 'mechanical design engineer',
    r'material controller': 'material controller',
    r'^marketing specialist': 'marketing specialist',
    r"^marketing executive": "marketing executive",
    r'^nurse': 'nurse',
    r'odoo developer': 'odoo developer',
    r'^office manager': 'office manager',
    'outpatient nurse': 'outpatient nurse',
    r'organizational development.*specialist': 'organizational development specialist',
    r'oracle cloud fusion consultant': 'oracle cloud fusion consultant',
    r'^operations manager': 'operations manager',
    r'^operations executive': 'operations executive',
    r'^operation manager': 'operation manager',
    r'purchasing manager': 'purchasing manager',
    r'proposal engineer': 'proposal engineer',
    r'project scope and quality control specialist': 'project scope and quality control specialist',
    r"project sales engineer": "project sales engineer",
    r'^project planner': 'project planner',
    r'project lead': 'project lead',
    r'^(?!.*(?:manager)).*^project engineer': 'project engineer',
    r'^program manager': 'program manager',
    r'program director': 'program director',
    r'professional services consultant': 'professional services consultant',
    r'^procurement manager': 'procurement manager',
    r'procurement lead': 'procurement lead',
    r'^procurement engineer': 'procurement engineer',
    r'process engineer utilities': 'process engineer utilities',
    r'^(?!.*(?:utilities)).*^process engineer': 'process engineer',
    r'^power systems engineer': 'power systems engineer',
    r'portfolio manager': 'portfolio manager',
    r'^pmo manager': 'pmo manager',
    r'^planning manager': 'planning manager',
    r'^planner': 'planner',
    r"piping engineer": "piping engineer",
    r'people and culture manager': 'people and culture manager',
    r'patriot maintenance technician': 'patriot maintenance technician',
    r'^partnership(s)? manager': 'partnership manager',
    r'partner solution engineer': 'partner solution engineer',
    r'paralegal': 'paralegal',
    r'(?=.*(pharmacist))': 'pharmacist',
    r'^(?!.*(?:web)).*product designer': 'product designer',
    r'^product manager': 'product manager',
    r'^quality engineer($| \(e3-5\))': 'quality engineer',
    r'quantity surveyor($| \-)': 'quantity surveyor',
    r'(?=.*\bqa)(?=.*qc\b)(?=.*inspector)': 'qa/qc inspector',
    r'(?=.*\bqa)(?=.*qc\b)(?=.*manager)': 'qa/qc manager',
    r'qa/qc (job|engineer)': 'qa/qc engineer',
    r'quality assurance engineer': 'quality assurance engineer',
    r'quality assurance analyst': 'quality assurance analyst',
    r'^qc engineer': 'qc engineer',
    r'^risk manager': 'risk manager',
    r'risk engineer': 'risk engineer',
    r'restaurant supervisor': 'restaurant supervisor',
    r'^(?!.*(?:assistant)).*restaurant manager': 'restaurant manager',
    r'^resident engineer': 'resident engineer',
    r'reservations agent': 'reservations agent',
    r'representative.*sales': 'representative sales',
    r"^reporting manager": "reporting manager",
    r'^relationship manager': 'relationship manager',
    r'registered nurse': 'registered nurse',
    r'refinery process engineer': 'refinery process engineer',
    r'recruitment specialist': 'recruitment specialist',
    r'recruitment manager': 'recruitment manager',
    r"^(?!.*(?:and)).*^receptionist": "receptionist",
    r'^(?!.*(?:technical|power|and|desk)).*system(s)? engineer': 'system engineer',
    r'service manager': 'service manager',
    r'(?=.*(structural))(?=.*(engineer))^(?!.*principal).*': 'systems engineer',
    r'(?<!assistant )sales manager': 'sales manager',
    r'system(s)? analyst': 'system analyst',
    r'strategic planning engineer (e2)': 'strategic planning engineer',
    r'storekeeper': 'storekeeper',
    r'store supervisor': 'store supervisor',
    r'^(?!.*(?:assistant)).*store manager': 'store manager',
    r'stewarding supervisor': 'stewarding supervisor',
    r'stakeholders interface engineer': 'stakeholders interface engineer',
    r'stakeholder specialist': 'stakeholder specialist',
    r'^(?!.*(?:executive)).*sous chef': 'sous chef',
    r'^(?!.*(?:channel security|account)).*solutions engineer': 'solutions engineer',
    r'solution(s)? architect': 'solutions architect',
    r'solar pv engineer': 'solar pv engineer',
    r'site manager': 'site manager',
    r'^(?!.*(?:supervisor)).*service sales': 'service sales engineer',
    r'^(?!.*(?:support|administrative|field)).*service (level )?manager': 'service manager',
    r'service engineer': 'service engineer',
    r'^service advisor': 'service advisor',
    r"^security manager": "security manager",
    r"security guard": "security guard",
    r'sector sales manager': 'sector sales manager',
    r'scheduling engineer': 'scheduling engineer',
    r'salesman': 'salesman',
    r'sales team leader': 'sales team leader',
    r'sales supervisor': 'sales supervisor',
    r'^sales representative': 'sales representative',
    r'^(?!.*(?:account|corporate|physical)).*^sales manager ': 'sales manager',
    r'sales executive': 'sales executive',
    r'^(?!.*(?:manager|application|lighting|project|pre|solutions|specifications|surveying)).*sales engineer': 'sales engineer',
    r"pre\b.*sales engineer": "pre-sales engineer",
    r'^sales consultant': 'sales consultant',
    r'sales associate': 'sales associate',
    r'sales and service engineer': 'sales and service engineer',
    r'sales and leasing manager': 'sales and leasing manager',
    r'sales administrator': 'sales administrator',
    r"^(?!.*(?:and|\&)).*safety officer": 'safety officer',
    r'^(?!.*(?:healthcare)).*sales director': 'sales director',
    r'(?=.*(operations|operation))(?=.*(specialist|coordinator|associate))(?=.*(sales))': 'sales operations specialist',
    r'(?=.*(engineer|engineering))(?=.*backend)^(?!.*(?:lead|manager|test automation)).*': 'software engineer backend',
    r'(?=.*(engineer|engineering))(?=.*(mobile|ios|android))': 'software mobile engineer',
    r'(?=.*(operations|operation))(?=.*(manager|senior manager|area manager))(?=.*(strategy|planning))': 'strategy & operations manager',
    r'^(?!.*(?:and)).*system administrator.*': 'system administrator',
    r'talent acquisition (specialist|partner|&).*': 'talent acquisition specialist',
    r'(technical|tech) lead': 'technical lead',
    r'^(?!.*(?:automation)).*testing engineer|tester': 'testing engineer',
    r'software tester': 'testing engineer',
    r'tuv rigger': 'tuv rigger',
    r'^translat': "translator",
    r'^training manager': 'training manager',
    r'^training coordinator': 'training coordinator',
    r'testing & commissioning engineer': 'testing & commissioning engineer',
    r"territory specialist": "territory specialist",
    r'tender manager': 'tender manager',
    r'talent acquisition specialist': r'talent acquisition specialist',
    r'tax & legal services': 'tax & legal services',
    r'^team leader': 'team leader',
    r'technical analyst': 'technical analyst',
    r'technical delivery manager': 'technical delivery manager',
    r'technical design manager': 'technical design manager',
    r'technical project manager': 'technical project manager',
    r'technical recruiter': 'technical recruiter',
    r'technical success manager': 'technical success manager',
    r'technical writer': 'technical writer',
    r'ux/ui|ui/ux': 'ui/ux designer',
    r'(^|\s)ui ': 'ui designer',
    r'(^|\s)ux ': 'ux designer',
    r"workshop supervisor": 'workshop supervisor',
    r'web developer': 'web developer',
    r'waiter': "waiter",
}
df_saudi.title.value_counts()
#%%
pattern_replace = r'(^((sr(\b|\s)|\ssr(\b|\s))|senior|junior|staff|female|\bmen\b|\bmale\b|women(\'s)|tpe (iv|iii|ii|i|v)(\s)?(-|/)?)( (senior|graduate))?|^graduate|^trainee\b( -)?)(\s)?(\.|-|/|\\)?|(\.|\-|/|\,|\\)$'
df_egypt.title = df_egypt.title.str.replace(pattern_replace, '', regex=True).str.strip()
df_saudi.title = df_saudi.title.str.replace(pattern_replace, '', regex=True).str.strip()
df_egypt = df_egypt.sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)
df_saudi = df_saudi.sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
review_matches(df_egypt, final_mapping_title_egypt)
#%%
review_matches(df_saudi, final_mapping_title_saudi)
#%%
edit_title(df_egypt, final_mapping_title_egypt)
df_egypt.title.value_counts()
#%%
edit_title(df_saudi, final_mapping_title_saudi)
df_saudi.title.value_counts()
#%%
conn = sqlite3.connect('data/database.db')
# df.to_sql('EGYPT', con=conn, if_exists='replace')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace')
#conn.close()
#%% md
# ## Analysis
# 
#%%
conn = sqlite3.connect('data/database.db')
df_egy = pd.read_sql('SELECT * FROM EGYPT', conn)
df_saudi = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
#%%
df_egy.head()
#%%
df_saudi.head()
#%%
df_egy['title'].nunique()
#%%
df_saudi['title'].nunique()
#%%
df_egy['city'].unique()
#%%
df_saudi['city'].unique()
#%%
df_egy['city'].value_counts().head()
#%%
df_saudi['city'].value_counts().head()
#%%
df_egy['title'].value_counts().head()
#%%
df_saudi['title'].value_counts().head()
#%% md
# # Analysis and Explanation of Plots
#%% md
# ### **Plot 1: Top 10 Cities by Number of Jobs (Egypt)**
# 
# #### **Description**
# - This bar chart shows the top 10 cities in Egypt based on the number of jobs available.
# - The x-axis represents the names of the cities, while the y-axis represents the number of jobs.
# - The cities are listed from left to right in descending order of job availability.
# 
# #### **Key Observations**
# 1. **Cairo** has the highest number of jobs, with over 2,000 jobs, making it the dominant city.
# 2. **Alexandria** follows as the second city with approximately 100 jobs.
# 3. Other cities such as **New Cairo**, **Sharm El-Sheikh**, **Matrouh**, **Aswan**, **Luxor**, **Giza**, and **Suez** have very low job availability, with most having fewer than 50 jobs.
# 
# #### **Meaning**
# - Cairo is the capital and largest city in Egypt, serving as the country's political, economic, and cultural center, which explains its high job availability.
# - Alexandria, as the second-largest city, offers some job opportunities but is far behind Cairo.
# - Smaller cities like Sharm El-Sheikh, Matrouh, and Aswan have minimal job opportunities, likely due to their smaller populations and more specialized economies (e.g., tourism).
# 
# ---
# 
# ### **Plot 2: Top 10 Cities by Number of Jobs (Saudi Arabia)**
# 
# #### **Description**
# - This bar chart shows the top 10 cities in Saudi Arabia based on the number of jobs available.
# - The x-axis represents the names of the cities, while the y-axis represents the number of jobs.
# - The cities are listed from left to right in descending order of job availability.
# 
# #### **Key Observations**
# 1. **Riyadh** has the highest number of jobs, significantly outperforming other cities with over 2,000 jobs.
# 2. **Jeddah** follows as the second city with approximately 500 jobs.
# 3. **Dammam**, **Khobar**, and **Sharqia** have moderate numbers of jobs, ranging from 100 to 300.
# 4. The remaining cities (**Al-Madinah Al-Munawarah**, **Qatif**, **Jizan**, **Tabuk**, and **Makkah**) have relatively low job availability, with most having fewer than 100 jobs.
# 
# #### **Meaning**
# - Riyadh is the economic and political hub of Saudi Arabia, which explains its dominance in job availability.
# - Jeddah, being a major port city and financial center, also offers a substantial number of jobs.
# - Smaller cities like Qatif, Jizan, and Tabuk have limited job opportunities, likely due to their size and economic focus.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Capital Cities**:
#    - In both countries, the capital cities (Riyadh for Saudi Arabia and Cairo for Egypt) have the highest number of jobs, highlighting their central role in the economy.
# 2. **Skewed Distribution**:
#    - Both plots show a highly skewed distribution, where a few cities dominate job availability, while the majority have very low numbers.
# 3. **Economic Hubs**:
#    - Major economic hubs (e.g., Jeddah in Saudi Arabia and Alexandria in Egypt) offer significant job opportunities but are still far behind the capital cities.
# 
# #### **Differences**
# 1. **Second-Largest City Job Availability**:
#    - In Saudi Arabia, Jeddah offers around 500 jobs, which is a substantial number.
#    - In Egypt, Alexandria offers only about 100 jobs, indicating a much lower secondary hub compared to Saudi Arabia.
# 2. **Overall Job Distribution**:
#    - Saudi Arabia has a broader distribution of jobs across multiple cities (e.g., Dammam, Khobar, Sharqia), whereas Egypt's job market is heavily centralized in Cairo.
# 3. **Smaller Cities**:
#    - In Saudi Arabia, smaller cities like Qatif, Jizan, and Tabuk still have some job availability, albeit low.
#    - In Egypt, smaller cities like Sharm El-Sheikh, Matrouh, and Aswan have almost negligible job opportunities.
# 
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong concentration of jobs in their capital cities, reflecting their economic and political significance.
# - However, Saudi Arabia shows a slightly more diversified job market across multiple cities, while Egypt's job market is heavily centralized in Cairo, with minimal opportunities elsewhere.
#%%
fig11 = job_distribution_by_city(df_egy[df_egy['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_egypt", folder='egypt',
                                 top_n=10, save=False)
fig12 = job_distribution_by_city(df_saudi[df_saudi['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_saudi", folder='saudi',
                                 top_n=10, save=False)
#%% md
# ### **Plot 1: Number of Jobs by Company (Egypt)**
# 
# #### **Description**
# - This bar chart shows the number of jobs offered by different companies in Egypt.
# - The x-axis represents the names of the companies, while the y-axis represents the number of jobs.
# - The companies are listed from left to right in descending order of job availability.
# 
# #### **Key Observations**
# 1. **Talent 360** has the highest number of jobs, with over 290 jobs, making it the dominant employer.
# 2. **SSC - Egypt** follows as the second company with approximately 180 jobs.
# 3. **Vodafone - Egypt**, **Giza Systems**, and **Orange - Other locations** have moderate numbers of jobs, ranging from 100 to 120.
# 4. Other companies such as **Raya Holding for Financial Investments**, **swatX Solutions**, and **ProjectGrowth** offer around 50 to 100 jobs.
# 5. Smaller companies like **RAWAJ**, **Delivery Hero SE**, **ElsewedyElectric**, and **Tagaddod** have relatively low job availability, with most having fewer than 50 jobs.
# 
# #### **Meaning**
# - **Talent 360** appears to be a major player in the Egyptian job market, possibly due to its focus on recruitment or staffing services.
# - Companies like **SSC - Egypt** and **Vodafone - Egypt** are significant employers, reflecting the importance of technology and telecommunications in Egypt's economy.
# - The presence of international brands (e.g., Vodafone) and local companies (e.g., Giza Systems) highlights a diverse job market.
# - Smaller companies have limited job offerings, indicating a fragmented job landscape outside the top employers.
# 
# ---
# 
# ### **Plot 2: Number of Jobs by Company (Saudi Arabia)**
# 
# #### **Description**
# - This bar chart shows the number of jobs offered by different companies in Saudi Arabia.
# - The x-axis represents the names of the companies, while the y-axis represents the number of jobs.
# - The companies are listed from left to right in descending order of job availability.
# 
# #### **Key Observations**
# 1. **Saudi Aramco** has the highest number of jobs, significantly outperforming other companies with over 200 jobs.
# 2. **InterContinental Hotels Group** follows as the second company with approximately 180 jobs.
# 3. **Jobs for Humanity**, **HILL INTERNATIONAL**, and **JASARA PMC** have moderate numbers of jobs, ranging from 120 to 170.
# 4. Other companies such as **NEOM**, **Eram Talent**, **Antal International**, and **Bechtel Corporation** offer around 50 to 70 jobs.
# 5. Smaller companies like **Arthur Lawrence**, **WorleyParsons**, **Giza Arabia**, and **Ash International** have relatively low job availability, with most having fewer than 50 jobs.
# 
# #### **Meaning**
# - **Saudi Aramco**, being one of the largest oil companies globally and a major employer in Saudi Arabia, dominates the job market.
# - Companies like **InterContinental Hotels Group** and **Jobs for Humanity** also play significant roles in providing employment opportunities.
# - The presence of international companies (e.g., Bechtel Corporation) indicates a mix of local and global businesses contributing to the job market.
# - Smaller companies have limited job offerings, reflecting a more fragmented job market outside the top employers.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Leading Employers**:
#    - In both countries, a few leading companies dominate the job market. For example, **Saudi Aramco** in Saudi Arabia and **Talent 360** in Egypt have significantly higher job counts compared to other companies.
# 2. **Skewed Distribution**:
#    - Both plots show a highly skewed distribution, where a few companies offer the majority of jobs, while the rest have relatively low job availability.
# 3. **Presence of International Companies**:
#    - Both countries have international companies (e.g., Bechtel Corporation in Saudi Arabia and Vodafone in Egypt) contributing to the job market.
# 
# #### **Differences**
# 1. **Leading Employer Job Availability**:
#    - In Saudi Arabia, **Saudi Aramco** offers over 200 jobs, which is substantial but not as high as **Talent 360** in Egypt, which offers over 290 jobs.
#    - The second-largest employer in Saudi Arabia (**InterContinental Hotels Group**) offers around 180 jobs, while in Egypt, **SSC - Egypt** offers around 180 jobs.
# 2. **Overall Job Distribution**:
#    - Saudi Arabia has a more diversified job market with several companies offering moderate job opportunities (e.g., NEOM, Eram Talent).
#    - Egypt has a more concentrated job market, with a few large employers (e.g., Talent 360, SSC - Egypt) dominating, while smaller companies have very limited job availability.
# 3. **Smaller Companies**:
#    - In Saudi Arabia, smaller companies like **Arthur Lawrence** and **WorleyParsons** still have some job availability, albeit low.
#    - In Egypt, smaller companies like **RAWAJ** and **Delivery Hero SE** have almost negligible job opportunities, indicating a more fragmented job market.
# 
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong concentration of jobs in a few leading companies, reflecting their economic significance.
# - However, Saudi Arabia shows a slightly more diversified job market across multiple companies, while Egypt's job market is heavily centralized in a few large employers, with minimal opportunities elsewhere.
# 
#%%
fig21 = analyze_jobs_by_company(df_egy, plot_name="analyze_jobs_by_company_egypt", folder='egypt',
                                save=False)
fig22 = analyze_jobs_by_company(df_saudi, plot_name="analyze_jobs_by_company_saudi", folder='saudi',
                                save=False)
#%% md
# ### **Plot 1: Top 10 Most Frequent Job Titles (Egypt)**
# 
# #### **Description**
# - This horizontal bar chart shows the top 10 most frequent job titles in Egypt based on the number of occurrences.
# - The y-axis represents the job titles, while the x-axis represents the number of occurrences.
# - The job titles are listed from top to bottom in descending order of frequency.
# 
# #### **Key Observations**
# 1. **Accountant** is the most frequent job title, with over 80 occurrences.
# 2. **Business Analyst** follows closely with approximately 65 occurrences.
# 3. **Account Manager** is the third most frequent job title, with around 60 occurrences.
# 4. **Support Engineer** and **Graphic Design** have moderate frequencies, with around 40 and 38 occurrences, respectively.
# 5. Other job titles such as **Software Engineer**, **Customer Service**, **Sales Manager**, **Product Manager**, and **Marketing Manager** have relatively lower frequencies, ranging from 27 to 35 occurrences.
# 
# #### **Meaning**
# - **Accounting roles** (e.g., Accountant, Account Manager) are highly prevalent, indicating a strong demand for financial expertise in the Egyptian job market.
# - **Business Analyst** and **Support Engineer** roles suggest a focus on data analysis and technical support, reflecting the growing importance of technology and analytics.
# - The presence of graphic design and software engineering roles highlights the significance of creative and IT sectors in Egypt.
# - Customer service and sales roles indicate a focus on client interaction and relationship management.
# 
# ---
# 
# ### **Plot 2: Top 10 Most Frequent Job Titles (Saudi Arabia)**
# 
# #### **Description**
# - This horizontal bar chart shows the top 10 most frequent job titles in Saudi Arabia based on the number of occurrences.
# - The y-axis represents the job titles, while the x-axis represents the number of occurrences.
# - The job titles are listed from top to bottom in descending order of frequency.
# 
# #### **Key Observations**
# 1. **Sales Manager** is the most frequent job title, with over 85 occurrences.
# 2. **Account Manager** follows closely with approximately 85 occurrences.
# 3. **Accountant** is the third most frequent job title, with around 80 occurrences.
# 4. **Mechanical Engineer** and **Civil Engineer** have moderate frequencies, with around 45 occurrences each.
# 5. Other job titles such as **Business Development Manager**, **Sales Executive**, **Marketing Manager**, **Account Executive**, and **Sales Representative** have relatively lower frequencies, ranging from 40 to 45 occurrences.
# 
# #### **Meaning**
# - **Sales-related roles** (e.g., Sales Manager, Account Manager) are highly prevalent, indicating a strong focus on sales and customer engagement in the Saudi Arabian job market.
# - **Accounting and engineering roles** (e.g., Accountant, Mechanical Engineer, Civil Engineer) are also common, reflecting the importance of these fields in industries like construction, finance, and manufacturing.
# - The presence of business development and marketing roles suggests a focus on growth and strategic planning within organizations.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Accounting Roles**:
#    - In both countries, **Accountant** and **Account Manager** are among the top job titles, highlighting the importance of financial roles in both markets.
# 2. **Presence of Sales Roles**:
#    - Both plots show significant occurrences of sales-related roles (e.g., Sales Manager, Account Manager).
# 3. **Moderate Frequency of Technical Roles**:
#    - Both countries have moderate occurrences of technical roles, such as engineers (Mechanical Engineer, Civil Engineer in Saudi Arabia; Support Engineer, Software Engineer in Egypt).
# 
# #### **Differences**
# 1. **Most Frequent Job Title**:
#    - In Saudi Arabia, **Sales Manager** is the most frequent job title, emphasizing a strong focus on sales.
#    - In Egypt, **Accountant** is the most frequent job title, indicating a greater emphasis on financial roles.
# 2. **Focus on Specific Industries**:
#    - Saudi Arabia shows a stronger focus on engineering roles (e.g., Mechanical Engineer, Civil Engineer), reflecting its industrial and infrastructure development.
#    - Egypt has a higher prevalence of roles related to technology and creativity (e.g., Business Analyst, Graphic Design, Software Engineer).
# 3. **Variation in Secondary Roles**:
#    - In Saudi Arabia, secondary roles include **Account Manager**, **Accountant**, and **Mechanical Engineer**.
#    - In Egypt, secondary roles include **Business Analyst**, **Account Manager**, and **Support Engineer**.
# 
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong demand for accounting and sales roles, reflecting their importance across various industries.
# - However, Saudi Arabia shows a more pronounced focus on engineering and sales, likely due to its industrial and economic structure.
# - Egypt, on the other hand, demonstrates a greater emphasis on technology, analytics, and creative roles, indicating a different set of industry priorities.
#%%
fig31 = get_top_job_titles_with_plot(df_egy, plot_name="get_top_job_titles_with_plot_egypt",
                                     folder='egypt', save=False)
fig32 = get_top_job_titles_with_plot(df_saudi, plot_name="get_top_job_titles_with_plot_saudi",
                                     folder='saudi', save=False)
#%% md
# ### **Plot 1: Job Distribution by Work Type (Egypt)**
# 
# #### **Description**
# - This pie chart shows the distribution of job types based on work arrangements in Egypt.
# - The chart is divided into three segments:
#   - **On-site**: Jobs that require physical presence at a workplace.
#   - **Remote**: Jobs that can be performed entirely from a remote location.
#   - **Hybrid**: Jobs that combine both on-site and remote work.
# 
# #### **Key Observations**
# 1. **On-site** jobs dominate the distribution, accounting for **86.5%** of the total jobs.
# 2. **Remote** jobs make up **9.9%** of the total jobs.
# 3. **Hybrid** jobs have the smallest share, representing only **3.6%** of the total jobs.
# 
# #### **Meaning**
# - The overwhelming majority of jobs in Egypt are **on-site**, indicating that most employers prefer or require employees to work physically at a workplace.
# - **Remote** jobs represent a small but notable portion of the job market, suggesting some flexibility in work arrangements but not as prevalent as on-site roles.
# - **Hybrid** jobs are minimal, reflecting limited adoption of flexible work models that combine both on-site and remote work.
# 
# ---
# 
# ### **Plot 2: Job Distribution by Work Type (Saudi Arabia)**
# 
# #### **Description**
# - This pie chart shows the distribution of job types based on work arrangements in Saudi Arabia.
# - The chart is divided into three segments:
#   - **On-site**: Jobs that require physical presence at a workplace.
#   - **Remote**: Jobs that can be performed entirely from a remote location.
#   - **Hybrid**: Jobs that combine both on-site and remote work.
# 
# #### **Key Observations**
# 1. **On-site** jobs dominate the distribution, accounting for **93.0%** of the total jobs.
# 2. **Remote** jobs make up **3.4%** of the total jobs.
# 3. **Hybrid** jobs have a slightly larger share compared to Egypt, representing **3.5%** of the total jobs.
# 
# #### **Meaning**
# - Similar to Egypt, **on-site** jobs are overwhelmingly dominant in Saudi Arabia, indicating a strong preference for physical workplace attendance.
# - **Remote** jobs are even less prevalent in Saudi Arabia compared to Egypt, suggesting fewer opportunities for fully remote work.
# - **Hybrid** jobs show a slightly higher proportion than in Egypt, indicating a marginal increase in the adoption of flexible work models.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of On-site Jobs**:
#    - Both countries exhibit a strong preference for **on-site** jobs, with over 85% of jobs requiring physical presence.
# 2. **Low Remote Jobs**:
#    - Both countries have a very low percentage of **remote** jobs, indicating limited opportunities for fully remote work.
# 3. **Minimal Hybrid Jobs**:
#    - Both countries show a small share of **hybrid** jobs, reflecting limited adoption of flexible work models.
# 
# #### **Differences**
# 1. **Proportion of On-site Jobs**:
#    - In Saudi Arabia, **on-site** jobs account for **93.0%**, which is significantly higher than Egypt's **86.5%**.
#    - This suggests a stronger emphasis on traditional workplace settings in Saudi Arabia.
# 2. **Proportion of Remote Jobs**:
#    - Egypt has a slightly higher percentage of **remote** jobs (9.9%) compared to Saudi Arabia (3.4%), indicating more opportunities for remote work in Egypt.
# 3. **Proportion of Hybrid Jobs**:
#    - Saudi Arabia has a slightly higher percentage of **hybrid** jobs (3.5%) compared to Egypt (3.6%), although both are minimal.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia heavily favor **on-site** jobs, reflecting a traditional approach to work arrangements.
# - However, Egypt shows a slightly higher prevalence of **remote** jobs, while Saudi Arabia demonstrates a marginally higher adoption of **hybrid** work models.
# - Overall, both countries have limited flexibility in work arrangements, with a strong reliance on physical workplace attendance.
# 
#%%
fig41 = analyze_jobs_by_work_type(df_egy, plot_name="analyze_jobs_by_work_type_egypt",
                                  folder='egypt', save=False)
fig42 = analyze_jobs_by_work_type(df_saudi, plot_name="analyze_jobs_by_work_type_saudi",
                                  folder='saudi', save=False)
#%% md
# ### **Plot 1: Job Distribution by Gender (Egypt)**
# 
# #### **Description**
# - This bar chart shows the job distribution based on gender in Egypt.
# - The x-axis represents the gender categories: **No Preference**, **Female**, and **Male**.
# - The y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **No Preference**:
#    - Dominates the distribution with **3,815 jobs**, indicating that most job postings do not specify a gender preference.
# 2. **Female**:
#    - Has a very small share with **130 jobs**.
# 3. **Male**:
#    - Has an even smaller share with **64 jobs**.
# 
# #### **Meaning**
# - The vast majority of job postings in Egypt are **gender-neutral** (No Preference), suggesting that employers are open to hiring candidates regardless of gender.
# - The extremely low numbers for **Female** and **Male** indicate that gender-specific job postings are rare in Egypt.
# 
# ---
# 
# ### **Plot 2: Job Distribution by Gender (Saudi Arabia)**
# 
# #### **Description**
# - This bar chart shows the job distribution based on gender in Saudi Arabia.
# - The x-axis represents the gender categories: **No Preference**, **Male**, and **Female**.
# - The y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **No Preference**:
#    - Dominates the distribution with **4,986 jobs**, indicating that most job postings do not specify a gender preference.
# 2. **Male**:
#    - Has a slightly higher share compared to Egypt with **274 jobs**.
# 3. **Female**:
#    - Has a share of **245 jobs**, which is also higher than Egypt but still relatively low.
# 
# #### **Meaning**
# - Similar to Egypt, the majority of job postings in Saudi Arabia are **gender-neutral** (No Preference), showing that employers prioritize gender-inclusive hiring practices.
# - While **Male** and **Female** specific job postings are still low, they are slightly more prevalent in Saudi Arabia compared to Egypt, indicating a marginal increase in gender-specific job opportunities.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of No Preference**:
#    - In both countries, the majority of job postings fall under the **No Preference** category, reflecting a strong trend toward gender-neutral job advertisements.
# 2. **Low Gender-Specific Jobs**:
#    - Both countries have very few job postings that specify a preference for either **Male** or **Female** candidates.
# 
# #### **Differences**
# 1. **Proportion of No Preference Jobs**:
#    - In Saudi Arabia, **No Preference** jobs account for **4,986 jobs**, which is significantly higher than Egypt's **3,815 jobs**.
#    - This suggests that Saudi Arabia has a larger overall job market or more gender-neutral job postings.
# 2. **Gender-Specific Jobs**:
#    - Egypt has very low numbers for both **Female** (130 jobs) and **Male** (64 jobs).
#    - Saudi Arabia shows slightly higher numbers for **Male** (274 jobs) and **Female** (245 jobs), indicating a marginal increase in gender-specific job opportunities compared to Egypt.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong preference for gender-neutral job postings, with the majority of jobs falling under the **No Preference** category.
# - However, Saudi Arabia shows a slightly higher prevalence of gender-specific job postings (both Male and Female) compared to Egypt, although these numbers remain relatively low overall.
# - This indicates a general trend toward inclusive hiring practices in both countries, with Saudi Arabia showing a marginally higher level of gender-specific job opportunities.
#%%
fig51 = analyze_jobs_by_gender(df_egy, plot_name="analyze_jobs_by_gender_egypt", folder='egypt',
                               save=False)
fig52 = analyze_jobs_by_gender(df_saudi, plot_name="analyze_jobs_by_gender_saudi", folder='saudi',
                               save=False)
#%% md
# ### **Plot 1: Job Distribution by Job Level (Egypt)**
# 
# #### **Description**
# - This bar chart shows the distribution of jobs based on job levels in Egypt.
# - The x-axis represents the job levels: **Senior**, **Management**, **Junior**, **Senior Management**, **Graduate**, **Mid Level**, and **C-Suite**.
# - The y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **Senior**:
#    - Dominates the distribution with **843 jobs**, indicating that senior-level positions are the most prevalent.
# 2. **Management**:
#    - Is the second most common job level with **679 jobs**.
# 3. **Junior**:
#    - Has **79 jobs**, representing a moderate share.
# 4. **Senior Management**:
#    - Has **67 jobs**, which is relatively low compared to other levels.
# 5. **Graduate**:
#    - Has **52 jobs**, indicating a small but present share.
# 6. **Mid Level**:
#    - Has **28 jobs**, showing a very low occurrence.
# 7. **C-Suite**:
#    - Has only **4 jobs**, reflecting an extremely small presence.
# 
# #### **Meaning**
# - The majority of job opportunities in Egypt are concentrated at the **Senior** and **Management** levels, suggesting a strong demand for experienced professionals and managers.
# - Entry-level positions (**Junior**, **Graduate**) and higher executive roles (**C-Suite**) are less common, indicating a limited number of opportunities for both fresh graduates and top-tier executives.
# - Mid-level positions (**Mid Level**) also have a low representation, highlighting a potential gap in mid-career opportunities.
# 
# ---
# 
# ### **Plot 2: Job Distribution by Job Level (Saudi Arabia)**
# 
# #### **Description**
# - This bar chart shows the distribution of jobs based on job levels in Saudi Arabia.
# - The x-axis represents the job levels: **Mid Level**, **Management**, **Junior**, **Graduate**, **Senior**, **Senior Management**, and **C-Suite**.
# - The y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **Mid Level**:
#    - Dominates the distribution with **138 jobs**, indicating that mid-level positions are the most prevalent.
# 2. **Management**:
#    - Is the second most common job level with **69 jobs**.
# 3. **Junior**:
#    - Has **28 jobs**, representing a moderate share.
# 4. **Graduate**:
#    - Has **22 jobs**, indicating a small but present share.
# 5. **Senior**:
#    - Has **11 jobs**, showing a very low occurrence.
# 6. **Senior Management**:
#    - Has **6 jobs**, reflecting an extremely small presence.
# 7. **C-Suite**:
#    - Has only **3 jobs**, indicating an even smaller number of opportunities.
# 
# #### **Meaning**
# - In Saudi Arabia, **Mid Level** positions are the most common, suggesting a strong demand for professionals with some experience but not yet at the senior or management level.
# - **Management** roles follow closely, indicating a need for middle-to-upper management skills.
# - Entry-level positions (**Junior**, **Graduate**) and higher executive roles (**C-Suite**, **Senior Management**) are less common, similar to Egypt.
# - Senior-level positions (**Senior**) are particularly scarce, highlighting a potential shortage of high-level leadership roles.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Higher-Level Positions**:
#    - Both countries show a strong preference for higher-level positions such as **Senior** (in Egypt) and **Mid Level** (in Saudi Arabia).
# 2. **Low Representation of C-Suite and Senior Management**:
#    - Both countries have very few job openings for **C-Suite** and **Senior Management** roles, indicating a limited number of top-tier executive positions.
# 3. **Moderate Presence of Entry-Level Jobs**:
#    - Both countries have a moderate number of **Junior** and **Graduate** positions, suggesting opportunities for early-career professionals.
# 
# #### **Differences**
# 1. **Most Common Job Level**:
#    - In Egypt, **Senior** positions are the most common, with **843 jobs**.
#    - In Saudi Arabia, **Mid Level** positions dominate with **138 jobs**.
# 2. **Distribution of Mid-Level Roles**:
#    - Egypt has a relatively low number of **Mid Level** jobs (**28 jobs**), while Saudi Arabia has a significantly higher number (**138 jobs**).
# 3. **Representation of Senior Roles**:
#    - Egypt has a much higher number of **Senior** jobs (**843 jobs**) compared to Saudi Arabia (**11 jobs**).
# 4. **Management Roles**:
#    - Egypt has more **Management** jobs (**679 jobs**) than Saudi Arabia (**69 jobs**).
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia prioritize hiring experienced professionals, with Egypt focusing more on **Senior** roles and Saudi Arabia emphasizing **Mid Level** positions.
# - There is a general scarcity of **C-Suite** and **Senior Management** roles in both countries, indicating a limited number of top executive opportunities.
# - While entry-level positions exist in both countries, they are not as dominant as higher-level roles, reflecting a stronger demand for experienced talent.
#%%
fig61 = analyze_jobs_by_job_level(df_egy[df_egy['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_egypt",
                                  folder='egypt', save=False)
fig62 = analyze_jobs_by_job_level(df_saudi[df_saudi['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_saudi",
                                  folder='saudi', save=False)
#%% md
# ### **Plot 1: Number of Job Entries Over Time (Egypt)**
# 
# #### **Description**
# - This line chart shows the trend in the number of job entries over time in Egypt.
# - The x-axis represents the date, spanning from November 2025 to April 2025.
# - The y-axis represents the number of job entries.
# 
# #### **Key Observations**
# 1. **Initial Phase (November 2025)**:
#    - The number of job entries starts at a very low value, close to zero.
# 2. **Gradual Increase**:
#    - From November to December 2025, there is a steady increase in job entries.
# 3. **Significant Growth**:
#    - Between January and February 2025, the number of job entries grows more rapidly.
# 4. **Peak in March 2025**:
#    - The highest number of job entries is observed in March 2025, reaching approximately **1,200 jobs**.
# 5. **Slight Decline in April 2025**:
#    - There is a minor decline in April 2025, but the number of job entries remains high, around **1,200 jobs**.
# 
# #### **Meaning**
# - The chart indicates a consistent upward trend in job entries over the six-month period, suggesting increasing job opportunities in Egypt.
# - The rapid growth between January and March 2025 could be due to seasonal factors, economic improvements, or specific industry developments.
# - The slight dip in April 2025 might indicate a temporary slowdown or stabilization after the peak.
# 
# ---
# 
# ### **Plot 2: Number of Job Entries Over Time (Saudi Arabia)**
# 
# #### **Description**
# - This line chart shows the trend in the number of job entries over time in Saudi Arabia.
# - The x-axis represents the date, spanning from November 2025 to April 2025.
# - The y-axis represents the number of job entries.
# 
# #### **Key Observations**
# 1. **Initial Phase (November 2025)**:
#    - The number of job entries starts at a very low value, close to zero.
# 2. **Gradual Increase**:
#    - From November to December 2025, there is a steady increase in job entries.
# 3. **Significant Growth**:
#    - Between January and February 2025, the number of job entries grows more rapidly.
# 4. **Peak in March 2025**:
#    - The highest number of job entries is observed in March 2025, reaching approximately **1,600 jobs**.
# 5. **Slight Decline in April 2025**:
#    - There is a minor decline in April 2025, but the number of job entries remains high, around **1,500 jobs**.
# 
# #### **Meaning**
# - Similar to Egypt, the chart shows a consistent upward trend in job entries over the six-month period, indicating growing job opportunities in Saudi Arabia.
# - The rapid growth between January and March 2025 suggests strong economic activity or specific initiatives driving job creation.
# - The slight dip in April 2025 might reflect a temporary pause or adjustment after the peak, similar to Egypt.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Overall Trend**:
#    - Both countries show a consistent upward trend in job entries from November 2025 to March 2025, indicating increasing job opportunities.
# 2. **Rapid Growth Period**:
#    - In both countries, the most significant growth occurs between January and March 2025, suggesting a common factor influencing job market dynamics during this period.
# 3. **Slight Decline in April**:
#    - Both countries experience a minor decline in job entries in April 2025, although the numbers remain high compared to earlier months.
# 
# #### **Differences**
# 1. **Magnitude of Job Entries**:
#    - Saudi Arabia consistently has a higher number of job entries compared to Egypt throughout the entire period.
#    - For example, in March 2025, Saudi Arabia reaches **1,600 jobs**, while Egypt reaches **1,200 jobs**.
# 2. **Initial Starting Point**:
#    - Both countries start with a very low number of job entries in November 2025, but Saudi Arabia appears to have a slightly higher initial baseline.
# 3. **Peak Values**:
#    - Saudi Arabia's peak in March 2025 is significantly higher (**1,600 jobs**) compared to Egypt's peak (**1,200 jobs**).
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit positive trends in job entries over the six-month period, reflecting improving job markets.
# - However, Saudi Arabia demonstrates a stronger job market overall, with consistently higher job entry numbers and a more pronounced peak in March 2025.
# - The slight declines in April 2025 for both countries suggest potential temporary adjustments or seasonal fluctuations, but the overall upward trajectory remains strong.
#%%
fig71 = plot_job_trend_over_time(df_egy, plot_name="plot_job_trend_over_time_egypt", folder='egypt',
                                 save=False)
fig72 = plot_job_trend_over_time(df_saudi, plot_name="plot_job_trend_over_time_saudi", folder='saudi',
                                 save=False)
#%% md
# ### **Plot 1: The Highest 10 Areas Declared for Business Opportunities (Egypt)**
# 
# #### **Description**
# - This bar chart shows the top 10 domains with the highest number of business opportunities in Egypt.
# - The x-axis represents the domains, while the y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **خدمات الدعم التجاري الأخرى (Other Commercial Support Services)**:
#    - Dominates the chart with **3,240 jobs**, indicating it is the most significant area for business opportunities.
# 2. **الاستشارات الهندسية العامة (General Engineering Consultancy)**:
#    - Has **97 jobs**, making it the second-highest domain.
# 3. **الاستشارات الإدارية (Management Consultancy)**:
#    - Follows with **85 jobs**.
# 4. **الاستعانة بالمصادر الخارجية المبيعات (Outsourcing Sales Resources)**:
#    - Has **65 jobs**.
# 5. **التعليم العالي (Higher Education)**:
#    - Shows **58 jobs**.
# 6. **الضيافة والسكن (Hospitality and Accommodation)**:
#    - Also has **58 jobs**.
# 7. **التسوق (Retail)**:
#    - Has **43 jobs**.
# 8. **Unknown**:
#    - Shows **36 jobs**.
# 9. **البناء والتشييد (Construction)**:
#    - Has **35 jobs**.
# 10. **البيع بالتجزئة وبالجملة (Wholesale and Retail Trade)**:
#     - Has **30 jobs**.
# 
# #### **Meaning**
# - **Other Commercial Support Services** is the leading domain, suggesting a strong demand for services that support commercial activities.
# - **General Engineering Consultancy** and **Management Consultancy** also show significant activity, indicating a focus on professional services.
# - Domains like **Higher Education**, **Hospitality and Accommodation**, and **Retail** have moderate job opportunities, reflecting their importance in the Egyptian economy.
# - The presence of "Unknown" suggests some data may not be categorized, but even so, it indicates limited opportunities compared to other sectors.
# 
# ---
# 
# ### **Plot 2: The Highest 10 Areas Declared for Business Opportunities (Saudi Arabia)**
# 
# #### **Description**
# - This bar chart shows the top 10 domains with the highest number of business opportunities in Saudi Arabia.
# - The x-axis represents the domains, while the y-axis represents the number of jobs.
# 
# #### **Key Observations**
# 1. **خدمات الدعم التجاري الأخرى (Other Commercial Support Services)**:
#    - Dominates the chart with **3,835 jobs**, indicating it is the most significant area for business opportunities.
# 2. **الاستشارات الإدارية (Management Consultancy)**:
#    - Has **109 jobs**, making it the second-highest domain.
# 3. **البناء والتشييد (Construction)**:
#    - Follows with **94 jobs**.
# 4. **الاستشارات الهندسية العامة (General Engineering Consultancy)**:
#    - Has **84 jobs**.
# 5. **البيع بالتجزئة وبالجملة (Wholesale and Retail Trade)**:
#    - Shows **70 jobs**.
# 6. **المطاعم وخدمات الطعام (Restaurants and Food Services)**:
#    - Has **54 jobs**.
# 7. **خدمات تكنولوجيا المعلومات (Information Technology Services)**:
#    - Shows **52 jobs**.
# 8. **النفط والغاز (Oil and Gas)**:
#    - Has **46 jobs**.
# 9. **الضيافة والسكن (Hospitality and Accommodation)**:
#    - Shows **41 jobs**.
# 10. **خدمات الرعاية الصحية الأخرى (Other Healthcare Services)**:
#     - Has **39 jobs**.
# 
# #### **Meaning**
# - **Other Commercial Support Services** is the leading domain, highlighting a strong demand for services that support commercial activities.
# - **Management Consultancy** and **Construction** also show significant activity, indicating a focus on professional services and infrastructure development.
# - Domains like **General Engineering Consultancy**, **Wholesale and Retail Trade**, and **Restaurants and Food Services** have moderate job opportunities, reflecting their importance in the Saudi Arabian economy.
# - **Oil and Gas** and **Hospitality and Accommodation** also contribute to the job market, showcasing the diversity of opportunities across various sectors.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Other Commercial Support Services**:
#    - Both countries show **Other Commercial Support Services** as the leading domain, indicating a strong demand for services that support commercial activities.
# 2. **Presence of Professional Services**:
#    - Both plots highlight domains such as **Management Consultancy** and **General Engineering Consultancy**, reflecting a focus on professional services.
# 3. **Moderate Presence of Retail and Hospitality**:
#    - Both countries have moderate job opportunities in **Retail** and **Hospitality and Accommodation**, showing the importance of these sectors in both economies.
# 
# #### **Differences**
# 1. **Magnitude of Job Opportunities**:
#    - In Saudi Arabia, **Other Commercial Support Services** has **3,835 jobs**, which is significantly higher than Egypt's **3,240 jobs**.
#    - This suggests a larger overall job market or more diverse opportunities in Saudi Arabia.
# 2. **Prominence of Construction**:
#    - **Construction** is a significant domain in Saudi Arabia (**94 jobs**) but does not appear in the top 10 for Egypt, indicating a stronger focus on infrastructure development in Saudi Arabia.
# 3. **Oil and Gas Sector**:
#    - **Oil and Gas** is a notable domain in Saudi Arabia (**46 jobs**) but is not present in Egypt, reflecting the importance of the oil industry in Saudi Arabia.
# 4. **Healthcare Services**:
#    - **Other Healthcare Services** appears in the top 10 for Saudi Arabia (**39 jobs**) but is not present in Egypt, suggesting a stronger emphasis on healthcare opportunities in Saudi Arabia.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong demand for **Other Commercial Support Services**, indicating a common trend in the need for services that support commercial activities.
# - However, Saudi Arabia shows a larger overall job market and a stronger focus on sectors like **Construction**, **Oil and Gas**, and **Healthcare Services**, reflecting its economic diversification efforts.
# - Egypt, on the other hand, has a more balanced distribution of opportunities across domains such as **General Engineering Consultancy**, **Management Consultancy**, and **Retail**, highlighting a different set of priorities in its economy.
#%%
fig81 = plot_job_postings_by_industry(df_egy, plot_name="plot_job_postings_by_industry_egypt",
                                       folder='egypt', save=False)
fig82 = plot_job_postings_by_industry(df_saudi, plot_name="plot_job_postings_by_industry_saudi",
                                       folder='saudi', save=False)
#%% md
# ### **Plot 1: Job Distribution by Type (Egypt)**
# 
# #### **Description**
# - This pie chart shows the distribution of job types in Egypt.
# - The chart is divided into several segments representing different job types:
#   - **Unknown**: 76.48%
#   - **Management**: 18.68%
#   - **Full-Time**: 3.14%
#   - **Intern**: 1.47%
#   - **Part-Time**: 0.10%
#   - **Contracts**: 0.10%
#   - **Temporary**: 0.02%
# 
# #### **Key Observations**
# 1. **Unknown**:
#    - Dominates the distribution with **76.48%**, indicating that a significant portion of job listings do not specify the job type.
# 2. **Management**:
#    - Is the second-largest segment with **18.68%**, showing a notable presence of management roles.
# 3. **Full-Time**:
#    - Represents **3.14%** of the jobs, indicating a moderate number of full-time positions.
# 4. **Intern**:
#    - Accounts for **1.47%**, suggesting a small but present number of internship opportunities.
# 5. **Part-Time**, **Contracts**, and **Temporary**:
#    - Have very low percentages (**0.10%, 0.10%, and 0.02%**, respectively), indicating minimal occurrences of these job types.
# 
# #### **Meaning**
# - The overwhelming majority of job listings in Egypt are categorized as **Unknown**, which could imply incomplete data or a lack of detailed job type information.
# - **Management** roles are the next most common, reflecting a strong demand for leadership and managerial positions.
# - Full-time positions are moderately prevalent, while internships, part-time roles, contracts, and temporary jobs are relatively rare.
# 
# ---
# 
# ### **Plot 2: Job Distribution by Type (Saudi Arabia)**
# 
# #### **Description**
# - This pie chart shows the distribution of job types in Saudi Arabia.
# - The chart is divided into several segments representing different job types:
#   - **Unknown**: 76.77%
#   - **Full-Time**: 21.82%
#   - **Management**: 0.73%
#   - **Intern**: 0.31%
#   - **Part-Time**: 0.27%
#   - **Contracts**: 0.09%
#   - **Temporary**: 0.02%
# 
# #### **Key Observations**
# 1. **Unknown**:
#    - Dominates the distribution with **76.77%**, similar to Egypt, indicating a significant portion of job listings without specified job types.
# 2. **Full-Time**:
#    - Is the second-largest segment with **21.82%**, showing a higher prevalence compared to Egypt.
# 3. **Management**:
#    - Represents only **0.73%**, which is significantly lower than Egypt's **18.68%**.
# 4. **Intern**, **Part-Time**, **Contracts**, and **Temporary**:
#    - Have very low percentages (**0.31%, 0.27%, 0.09%, and 0.02%**, respectively), indicating minimal occurrences of these job types.
# 
# #### **Meaning**
# - Similar to Egypt, the majority of job listings in Saudi Arabia are categorized as **Unknown**, suggesting incomplete data or a lack of detailed job type information.
# - **Full-Time** positions are more prevalent in Saudi Arabia compared to Egypt, reflecting a stronger focus on permanent employment.
# - Management roles are much less common in Saudi Arabia, indicating a potential difference in organizational structures or industry demands.
# - Internships, part-time roles, contracts, and temporary jobs are similarly rare in both countries.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Unknown Jobs**:
#    - Both countries show a high percentage of **Unknown** job types, with Egypt at **76.48%** and Saudi Arabia at **76.77%**. This suggests a common issue of incomplete job descriptions across both markets.
# 2. **Low Occurrence of Part-Time, Contracts, and Temporary Jobs**:
#    - Both countries have very low percentages for part-time, contract, and temporary jobs, indicating that these job types are not widely available in either market.
# 3. **Moderate Presence of Internships**:
#    - Both countries have a small but present number of internship opportunities, with Egypt at **1.47%** and Saudi Arabia at **0.31%**.
# 
# #### **Differences**
# 1. **Full-Time Jobs**:
#    - In Saudi Arabia, **Full-Time** jobs account for **21.82%**, which is significantly higher than Egypt's **3.14%**. This suggests a stronger emphasis on permanent employment in Saudi Arabia.
# 2. **Management Roles**:
#    - Egypt has a much higher percentage of **Management** roles (**18.68%**) compared to Saudi Arabia (**0.73%**). This indicates a substantial difference in the demand for leadership positions between the two countries.
# 3. **Distribution of Other Job Types**:
#    - While both countries have low percentages for internships, part-time roles, contracts, and temporary jobs, the specific percentages differ slightly. For example, Saudi Arabia has a slightly higher percentage for internships (**0.31%**) compared to Egypt (**1.47%**).
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia face a challenge with a large proportion of job listings being categorized as **Unknown**, highlighting a need for more detailed job descriptions.
# - Saudi Arabia shows a stronger focus on **Full-Time** employment compared to Egypt, while Egypt has a significantly higher demand for **Management** roles.
# - Overall, both countries exhibit a limited availability of part-time, contract, and temporary jobs, with internships also being relatively rare but more prevalent in Egypt.
#%%
fig91 = analyze_job_type_distribution(df_egy, plot_name="analyze_job_type_distribution_egypt",
                                      folder='egypt', save=False)
fig92 = analyze_job_type_distribution(df_saudi, plot_name="analyze_job_type_distribution_saudi",
                                      folder='saudi', save=False)
#%% md
# ### **Plot 1: Comparison of Min & Max Experience Requirements (Egypt)**
# 
# #### **Description**
# - This box plot compares the minimum (`min_num_of_years`) and maximum (`max_num_of_years`) years of experience required for jobs in Egypt.
# - The y-axis represents the number of years of experience.
# - The x-axis has two categories: `min_num_of_years` and `max_num_of_years`.
# 
# #### **Key Observations**
# 1. **Minimum Years of Experience (`min_num_of_years`)**:
#    - The median value is around **3 years**.
#    - The interquartile range (IQR) spans from approximately **0 to 6 years**, indicating that most job postings require between 0 and 6 years of experience.
#    - There are a few outliers with higher minimum requirements, reaching up to **10 years**.
# 
# 2. **Maximum Years of Experience (`max_num_of_years`)**:
#    - The median value is around **8 years**.
#    - The IQR spans from approximately **5 to 15 years**, showing that most job postings have a maximum requirement between 5 and 15 years.
#    - There are several outliers with very high maximum requirements, reaching up to **20 years**.
# 
# #### **Meaning**
# - **Minimum Experience**:
#   - Most job postings in Egypt do not require extensive experience, with a median of 3 years. However, there are some roles that demand more, such as those requiring 10 years or more.
# - **Maximum Experience**:
#   - The majority of job postings have a maximum experience requirement of around 8 years, but there is significant variability, with some roles accepting candidates with up to 20 years of experience.
#   - The presence of outliers suggests that certain specialized or senior-level positions may have much higher experience requirements.
# 
# ---
# 
# ### **Plot 2: Comparison of Min & Max Experience Requirements (Saudi Arabia)**
# 
# #### **Description**
# - This box plot compares the minimum (`min_num_of_years`) and maximum (`max_num_of_years`) years of experience required for jobs in Saudi Arabia.
# - The y-axis represents the number of years of experience.
# - The x-axis has two categories: `min_num_of_years` and `max_num_of_years`.
# 
# #### **Key Observations**
# 1. **Minimum Years of Experience (`min_num_of_years`)**:
#    - The median value is around **3 years**.
#    - The IQR spans from approximately **0 to 6 years**, similar to Egypt, indicating that most job postings require between 0 and 6 years of experience.
#    - There are a few outliers with higher minimum requirements, reaching up to **10 years**.
# 
# 2. **Maximum Years of Experience (`max_num_of_years`)**:
#    - The median value is around **9 years**.
#    - The IQR spans from approximately **5 to 17 years**, showing that most job postings have a maximum requirement between 5 and 17 years.
#    - There are several outliers with very high maximum requirements, reaching up to **20 years**.
# 
# #### **Meaning**
# - **Minimum Experience**:
#   - Similar to Egypt, most job postings in Saudi Arabia do not require extensive experience, with a median of 3 years. However, there are some roles that demand more, such as those requiring 10 years or more.
# - **Maximum Experience**:
#   - The majority of job postings have a maximum experience requirement of around 9 years, but there is significant variability, with some roles accepting candidates with up to 20 years of experience.
#   - The presence of outliers suggests that certain specialized or senior-level positions may have much higher experience requirements.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Median Minimum Experience**:
#    - Both countries show a median minimum experience requirement of around **3 years**, indicating that most entry-level or mid-level roles do not require extensive prior experience.
# 2. **Range of Minimum Experience**:
#    - Both countries have a similar IQR for minimum experience, ranging from **0 to 6 years**, suggesting a comparable distribution of low-experience roles.
# 3. **Presence of Outliers**:
#    - Both plots show outliers with higher minimum experience requirements (up to **10 years**), indicating that specialized or senior roles exist in both markets.
# 4. **Median Maximum Experience**:
#    - Both countries have a median maximum experience requirement of around **8–9 years**, suggesting that most job postings target professionals with moderate experience levels.
# 5. **Range of Maximum Experience**:
#    - Both countries have a wide range of maximum experience requirements, with IQRs spanning from **5 to 15–17 years**, reflecting diverse job opportunities across different experience levels.
# 6. **High Outliers for Maximum Experience**:
#    - Both plots show outliers with very high maximum experience requirements (up to **20 years**), indicating that senior-level or highly specialized roles exist in both markets.
# 
# #### **Differences**
# 1. **Median Maximum Experience**:
#    - Saudi Arabia has a slightly higher median maximum experience requirement (**9 years**) compared to Egypt (**8 years**), suggesting that Saudi Arabia may have a slightly higher demand for experienced professionals.
# 2. **Range of Maximum Experience**:
#    - Saudi Arabia has a slightly wider IQR for maximum experience (**5 to 17 years**) compared to Egypt (**5 to 15 years**), indicating a broader range of experience requirements in Saudi Arabia.
# 3. **Outliers for Maximum Experience**:
#    - Saudi Arabia has more pronounced outliers for maximum experience, with values reaching **20 years**, compared to Egypt, which also has outliers but at a similar level.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit similar patterns in terms of minimum and maximum experience requirements, with most job postings targeting professionals with 3–9 years of experience.
# - However, Saudi Arabia shows a slightly higher demand for experienced professionals, as indicated by the higher median maximum experience requirement and the broader range of experience levels.
# - Both countries have a mix of entry-level, mid-level, and senior-level roles, with some specialized positions requiring significantly more experience.
#%%
fig101 = compare_experience_requirements(df_egy, plot_name="compare_experience_requirements_egypt",
                                         folder='egypt', save=False)
fig102 = compare_experience_requirements(df_saudi, plot_name="compare_experience_requirements_saudi",
                                         folder='saudi', save=False)
#%% md
# ### **Plot 1: Heatmap of Job Count by City and Job Level (Egypt)**
# 
# #### **Description**
# - This heatmap shows the distribution of job counts across different cities in Egypt, categorized by job levels.
# - The x-axis represents the job levels: **C-Suite**, **Graduate**, **Junior**, **Management**, **Mid Level**, **No Preference**, **Senior**, and **Senior Management**.
# - The y-axis represents the cities in Egypt.
# - The color intensity indicates the number of jobs, with darker shades representing higher job counts.
# 
# #### **Key Observations**
# 1. **Most Prominent Cities**:
#    - **القاهرة (Cairo)** has the highest job counts across multiple job levels:
#      - **No Preference**: 1,160 jobs.
#      - **Mid Level**: 509 jobs.
#      - **Management**: 377 jobs.
#      - Other levels have moderate to low job counts.
#    - **الإسكندرية (Alexandria)** also shows significant job counts:
#      - **No Preference**: 62 jobs.
#      - **Mid Level**: 21 jobs.
#      - Other levels have minimal job counts.
# 2. **Job Levels with High Demand**:
#    - **No Preference** consistently shows the highest job counts across most cities.
#    - **Mid Level** and **Management** also have notable job counts in major cities like Cairo and Alexandria.
# 3. **Cities with Low Job Counts**:
#    - Many smaller cities (e.g., أسوان, الجونة, السويس) have very low or zero job counts across all levels.
#    - Only a few cities (e.g., القاهرة, الإسكندرية) contribute significantly to the job market.
# 
# #### **Meaning**
# - **Cairo** is the dominant city in terms of job opportunities, offering a wide range of roles at various levels, particularly in **No Preference** and **Mid Level** positions.
# - **Alexandria** is the second-largest contributor but with significantly fewer job opportunities compared to Cairo.
# - Smaller cities have limited job availability, indicating that the majority of job opportunities are concentrated in major urban centers.
# - The high count of **No Preference** jobs suggests that many employers are open to hiring candidates regardless of specific job level preferences.
# 
# ---
# 
# ### **Plot 2: Heatmap of Job Count by City and Job Level (Saudi Arabia)**
# 
# #### **Description**
# - This heatmap shows the distribution of job counts across different cities in Saudi Arabia, categorized by job levels.
# - The x-axis represents the job levels: **C-Suite**, **Graduate**, **Junior**, **Management**, **Mid Level**, **No Preference**, **Senior**, and **Senior Management**.
# - The y-axis represents the cities in Saudi Arabia.
# - The color intensity indicates the number of jobs, with darker shades representing higher job counts.
# 
# #### **Key Observations**
# 1. **Most Prominent Cities**:
#    - **الرياض (Riyadh)** has the highest job counts across multiple job levels:
#      - **No Preference**: 1,970 jobs.
#      - **Mid Level**: 2,020 jobs.
#      - **Management**: 17 jobs.
#      - Other levels have moderate to low job counts.
#    - **الدمام (Dammam)** also shows significant job counts:
#      - **No Preference**: 262 jobs.
#      - **Mid Level**: 42 jobs.
#      - Other levels have minimal job counts.
# 2. **Job Levels with High Demand**:
#    - **No Preference** consistently shows the highest job counts across most cities.
#    - **Mid Level** and **Management** also have notable job counts in major cities like Riyadh and Dammam.
# 3. **Cities with Low Job Counts**:
#    - Many smaller cities (e.g., الباحة, حفر الباطن, عنيزة) have very low or zero job counts across all levels.
#    - Only a few cities (e.g., الرياض, الدمام) contribute significantly to the job market.
# 
# #### **Meaning**
# - **Riyadh** is the dominant city in terms of job opportunities, offering a wide range of roles at various levels, particularly in **No Preference** and **Mid Level** positions.
# - **Dammam** is the second-largest contributor but with significantly fewer job opportunities compared to Riyadh.
# - Smaller cities have limited job availability, indicating that the majority of job opportunities are concentrated in major urban centers.
# - Similar to Egypt, the high count of **No Preference** jobs suggests that many employers are open to hiring candidates regardless of specific job level preferences.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Major Cities**:
#    - In both countries, a few major cities (Cairo in Egypt and Riyadh in Saudi Arabia) dominate the job market, offering the majority of job opportunities.
# 2. **High Count of No Preference Jobs**:
#    - Both countries show a strong preference for **No Preference** jobs, indicating that many employers are flexible regarding job level requirements.
# 3. **Concentration of Opportunities**:
#    - Both countries exhibit a concentration of job opportunities in major urban centers, with smaller cities having very limited job availability.
# 4. **Mid Level and Management Roles**:
#    - Both countries show significant demand for **Mid Level** and **Management** roles in major cities.
# 
# #### **Differences**
# 1. **Magnitude of Job Counts**:
#    - Saudi Arabia has significantly higher job counts overall, especially in major cities like Riyadh, where the **No Preference** category reaches 1,970 jobs.
#    - Egypt's highest job count is 1,160 jobs in Cairo, which is lower than Saudi Arabia's numbers.
# 2. **Number of Prominent Cities**:
#    - Egypt has two prominent cities (Cairo and Alexandria), while Saudi Arabia has more prominent cities (Riyadh, Dammam, etc.), although Riyadh dominates the job market.
# 3. **Distribution Across Job Levels**:
#    - In Egypt, **No Preference** jobs are highly dominant across all cities.
#    - In Saudi Arabia, **Mid Level** jobs also show high counts in major cities, contributing significantly to the job market.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong concentration of job opportunities in major urban centers, with Cairo and Riyadh being the primary hubs for employment.
# - The high count of **No Preference** jobs in both countries reflects a trend toward flexible hiring practices.
# - Saudi Arabia shows a larger overall job market, with higher job counts across major cities, while Egypt has a more focused job market centered around Cairo and Alexandria.
#%%
fig111 = jobs_heatmap_by_city_and_job_level(df_egy, plot_name="jobs_heatmap_by_city_and_job_level_egypt",
                                            folder='egypt', save=False)
fig112 = jobs_heatmap_by_city_and_job_level(df_saudi, plot_name="jobs_heatmap_by_city_and_job_level_saudi",
                                            folder='saudi', save=False)
#%% md
# ### **Plot 1: Most Common Job Titles (Wordcloud) - Egypt**
# 
# #### **Description**
# - This word cloud visualizes the most common job titles in Egypt.
# - The size of each word represents its frequency in the dataset, with larger words indicating more frequent job titles.
# - Words like **Account Manager**, **Manager**, **Senior**, **Lead**, **Specialist**, and **Accountant** are prominently displayed.
# 
# #### **Key Observations**
# 1. **Prominent Job Titles**:
#    - **Account Manager**: One of the most frequently occurring job titles.
#    - **Manager**: A very common role, reflecting a strong demand for managerial positions.
#    - **Senior**, **Lead**, and **Specialist**: These terms indicate higher-level or specialized roles.
#    - **Accountant**: Another prominent title, suggesting a significant demand for financial expertise.
# 2. **Other Common Roles**:
#    - Words like **Engineer**, **Software**, **Project**, and **Sales** appear frequently, indicating roles in engineering, software development, project management, and sales.
#    - Terms such as **Business Analyst**, **Support**, and **Coordinator** also appear, showing a mix of analytical, support, and coordination roles.
# 3. **Industry-Specific Roles**:
#    - Words like **Data Analyst**, **Design Engineer**, and **Customer Service** suggest a diverse range of industries, including technology, engineering, and customer service.
# 
# #### **Meaning**
# - The word cloud highlights a strong emphasis on **management** and **specialized roles** in Egypt, with a particular focus on **accounting** and **managerial positions**.
# - The presence of technical roles (e.g., **Software Engineer**, **Project Manager**) indicates a growing demand for skills in technology and project management.
# - The inclusion of **Sales** and **Customer Service** roles suggests a focus on client-facing and business development activities.
# 
# ---
# 
# ### **Plot 2: Most Common Job Titles (Wordcloud) - Saudi Arabia**
# 
# #### **Description**
# - This word cloud visualizes the most common job titles in Saudi Arabia.
# - The size of each word represents its frequency in the dataset, with larger words indicating more frequent job titles.
# - Words like **Consultant**, **Supervisor**, **Specialist**, **Engineer**, **Lead**, and **Manager** are prominently displayed.
# 
# #### **Key Observations**
# 1. **Prominent Job Titles**:
#    - **Consultant**: A highly frequent job title, indicating a strong demand for consulting roles.
#    - **Supervisor**: Another common role, reflecting a need for supervisory positions.
#    - **Specialist**, **Engineer**, and **Lead**: These terms highlight roles that require specialized skills and leadership.
#    - **Manager**: A prevalent title, similar to Egypt, showing a demand for managerial positions.
# 2. **Other Common Roles**:
#    - Words like **Director**, **Sales Manager**, and **Project Manager** appear frequently, indicating roles in leadership, sales, and project management.
#    - Terms such as **Business Development**, **Analyst**, and **Technician** suggest a mix of business-focused, analytical, and technical roles.
# 3. **Industry-Specific Roles**:
#    - Words like **Civil Engineer**, **Security**, and **Procurement** indicate roles in construction, security, and supply chain management.
#    - The presence of **Sales Executive Process Engineer** and **Human Resource Officer** reflects a blend of technical and administrative roles.
# 
# #### **Meaning**
# - The word cloud highlights a strong emphasis on **consulting**, **supervisory**, and **specialized roles** in Saudi Arabia, with a particular focus on **engineering** and **managerial positions**.
# - The inclusion of **business development** and **sales** roles suggests a focus on growth and client engagement.
# - Technical roles (e.g., **Engineer**, **Technician**) indicate a demand for skilled professionals in various industries.
# 
# ---
# 
# ### **Comparison Between the Two Plots**
# 
# #### **Similarities**
# 1. **Dominance of Managerial Roles**:
#    - Both countries show a strong emphasis on **managerial positions**, with words like **Manager**, **Lead**, and **Supervisor** appearing prominently.
# 2. **Presence of Specialized Roles**:
#    - Both word clouds include terms like **Specialist**, **Engineer**, and **Analyst**, indicating a demand for specialized skills.
# 3. **Focus on Sales and Customer-Facing Roles**:
#    - Words like **Sales Manager**, **Account Manager**, and **Customer Service** appear in both plots, reflecting a common need for sales and client-facing roles.
# 4. **Technical and Analytical Roles**:
#    - Both countries have a mix of technical and analytical roles, with terms like **Software Engineer**, **Data Analyst**, and **Business Analyst** appearing in both word clouds.
# 
# #### **Differences**
# 1. **Prominent Job Titles**:
#    - In Egypt, **Account Manager** and **Accountant** are highly prominent, indicating a strong focus on accounting and sales roles.
#    - In Saudi Arabia, **Consultant** and **Engineer** stand out, reflecting a greater emphasis on consulting and engineering roles.
# 2. **Industry-Specific Roles**:
#    - Egypt has more prominent roles in **customer service** and **design engineering**, while Saudi Arabia shows a stronger presence of **civil engineering** and **security** roles.
# 3. **Leadership Roles**:
#    - Saudi Arabia has a higher prominence of **Director** and **Business Development** roles, suggesting a stronger focus on leadership and strategic roles compared to Egypt.
# 
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong demand for **managerial** and **specialized roles**, with a focus on **technical** and **analytical** skills.
# - However, Egypt shows a stronger emphasis on **accounting** and **sales**, while Saudi Arabia highlights **consulting**, **engineering**, and **leadership** roles.
# - The differences reflect variations in industry priorities and economic structures between the two countries, with Egypt leaning toward services and sales, and Saudi Arabia focusing on engineering and strategic development.
#%%
fig121 = plot_top_job_titles_wordcloud(df_egy, plot_name="plot_top_job_titles_wordcloud_egypt",
                                       folder='egypt', save=False)
fig122 = plot_top_job_titles_wordcloud(df_saudi, plot_name="plot_top_job_titles_wordcloud_saudi",
                                       folder='saudi', save=False)