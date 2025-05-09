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
conn = sqlite3.connect('database.db')
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
conn = sqlite3.connect('database.db')
# df.to_sql('EGYPT', con=conn, if_exists='replace')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace')
#conn.close()
#%% md
# ## Analysis
# 
#%%
conn = sqlite3.connect('database.db')
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
# ##  Visualization 1: Top 10 Cities by Number of Jobs
# 
# ### Description:
# A vertical bar chart displaying the number of job listings in the top 10 Egyptian cities.
# 
# ###  Key Insights:
# 
# 1. **Cairo is the Undisputed Hub:**
#    - Cairo alone accounts for the vast majority of job postings (over 2,000).
#    - Reflects its status as the economic and business capital of Egypt.
# 
# 2. **Limited Opportunities in Other Cities:**
#    - Alexandria comes second, but with a significantly lower count (~100+).
#    - All other cities (like New Alamein, Sharm El Sheikh, Luxor, etc.) have minimal job postings.
#    - Suggests a high centralization of employment opportunities in the capital.
# 
# 3. **Implications:**
#    - Indicates potential internal migration toward Cairo for job seekers.
#    - May signal the need for investment in decentralizing job markets and regional development.
# 
# ###  Overall Takeaway:
# > Cairo dominates the job market in Egypt, with a steep drop-off in job availability in other cities, highlighting urban centralization and regional imbalance in employment opportunities.
# 
#%%
fig11 = job_distribution_by_city(df_egy[df_egy['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_egypt", folder='egypt',
                                 top_n=10, save=False)
#%%
fig12 = job_distribution_by_city(df_saudi[df_saudi['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_saudi", folder='saudi',
                                 top_n=10, save=False)
#%% md
# ## Visualization 2: Number of Jobs by Company
# 
# ### Description:
# A vertical bar chart illustrating how many job postings come from each company.
# 
# ### Key Insights:
# 
# 1. **Talent 360 Dominates the Market:**
#    - Over 250 job postings — far ahead of any other company.
#    - Likely a recruitment firm or aggregator serving multiple clients.
# 
# 2. **High Activity from Tech and Telecom Firms:**
#    - Notable companies include Vodafone Egypt, Giza Systems, Orange, and Accenture.
#    - Reflects strong demand for digital and telecom roles.
# 
# 3. **Diverse but Uneven Sector Representation:**
#    - Other sectors also visible:
#      - Real Estate: Palm Hills, Arabia Group
#      - Tourism: Grand Rotana Resort
#      - Industrial: Siemens, Schneider Electric
#    - Shows a variety of industries are hiring, but the majority of roles are concentrated in tech and recruitment.
# 
# ### Overall Takeaway:
# > Tech and staffing companies are leading job providers, while other sectors like real estate, tourism, and manufacturing contribute modestly to the hiring landscape.
# 
#%%
fig21 = analyze_jobs_by_company(df_egy, plot_name="analyze_jobs_by_company_egypt", folder='egypt',
                                save=False)
#%%
fig22 = analyze_jobs_by_company(df_saudi, plot_name="analyze_jobs_by_company_saudi", folder='saudi',
                                save=False)
#%% md
# ## Visualization 3: Top 10 Most Frequent Job Titles
# 
# ### Description:
# A horizontal bar chart showing the most commonly listed job titles in the dataset based on the number of occurrences.
# 
# ### Key Insights:
# 
# 1. **Strong Demand for Accounting Roles:**
#    - 5 of the top 10 job titles are finance/accounting-related:
#      - Accountant
#      - Senior Accountant
#      - Finance Manager
#      - Junior Accountant
#      - Chief Accountant
#    - Indicates a significant demand in the job market for financial expertise.
# 
# 2. **Data and Analytics Roles Are Rising:**
#    - Positions like Senior Business Analyst and Data Engineer appear in the top 10.
#    - Shows increasing importance of data-driven decision-making.
# 
# 3. **Support and Creative Roles Are Present:**
#    - Executive Assistant and Graphic Designer made the list.
#    - Suggests administrative and creative skills are still needed, though in smaller volumes.
# 
# ### Overall Takeaway:
# > The job market is currently dominated by finance-related positions, with a growing interest in data and analytics, and a continuing (but smaller) need for creative and support roles.
# 
#%%
fig31 = get_top_job_titles_with_plot(df_egy, plot_name="get_top_job_titles_with_plot_egypt",
                                     folder='egypt', save=False)
#%%
fig32 = get_top_job_titles_with_plot(df_saudi, plot_name="get_top_job_titles_with_plot_saudi",
                                     folder='saudi', save=False)
#%% md
# ##  Visualization 4: Job Distribution by Work Type
# 
# ### Description:
# A pie chart showing the percentage distribution of jobs based on their work format (On-site, Remote, Hybrid).
# 
# ###  Key Insights:
# 
# 1. **Overwhelming Majority are On-site Jobs:**
#    - 88.6% of listings are for on-site positions.
#    - Implies that traditional office presence is still dominant in Egypt.
# 
# 2. **Remote and Hybrid Work Are Very Limited:**
#    - Only 7.4% remote and 4.0% hybrid roles.
#    - Indicates slow adoption of flexible work models.
# 
# 3. **Implications:**
#    - May be due to lack of infrastructure, cultural preferences, or the nature of jobs requiring physical presence.
#    - A gap exists compared to global trends favoring hybrid and remote work, especially post-COVID.
# 
# ### Overall Takeaway:
# > The job market in Egypt is still heavily reliant on on-site roles, with minimal adoption of remote or hybrid work formats, highlighting a lag in workplace flexibility.
# 
#%%
fig41 = analyze_jobs_by_work_type(df_egy, plot_name="analyze_jobs_by_work_type_egypt",
                                  folder='egypt', save=False)
#%%
fig42 = analyze_jobs_by_work_type(df_saudi, plot_name="analyze_jobs_by_work_type_saudi",
                                  folder='saudi', save=False)
#%% md
# ##  Visualization 5: Job Distribution by Month
# 
# ###  Key Insights:
# 
# - A dominant majority (2253 jobs) have no gender preference.
# - Female-targeted roles are 97, while male-targeted roles are just 55.
# 
# ###  Overall Takeaway:
# - The job market is largely gender-neutral in job listings, which may reflect a trend toward inclusivity or a focus on qualifications over demographics
# 
#%%
fig51 = analyze_jobs_by_gender(df_egy, plot_name="analyze_jobs_by_gender_egypt", folder='egypt',
                               save=False)
#%%
fig52 = analyze_jobs_by_gender(df_saudi, plot_name="analyze_jobs_by_gender_saudi", folder='saudi',
                               save=False)
#%% md
# ##  visualization 6 :Job Level Distribution Analysis
# 
# ###  Key Insights:
# 
# **"No Preference" Dominates**
#   - 1,312 job postings have no specified job level.
#   - This may indicate flexibility in hiring or a lack of clarity in role definitions.
# 
# - **Strong Demand for Experienced Talent**
#   - Senior-level: 544 jobs
#   - Management: 409 jobs
#   - These figures highlight a clear demand for experienced and leadership-level professionals.
# 
# - **Limited Entry-Level Opportunities**
#   - Junior: 54
#   - Graduate: 27
#   - Mid Level: 21
#   - Opportunities for early-career candidates are noticeably fewer.
# 
# - **Minimal Executive-Level Roles**
#   - C-Suite positions: 2
#   - These roles are naturally scarce due to their seniority and selectiveness.
# 
# ### Overall Takeaway:
# - The job market is heavily skewed toward senior and management-level positions, with a surprising number of listings having no specified level. This may reflect a broad hiring strategy or incomplete data entry. Entry-level and executive roles are limited, indicating that companies are prioritizing experienced professionals over new graduates or top-tier executives.
# 
#%%
fig61 = analyze_jobs_by_job_level(df_egy[df_egy['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_egypt",
                                  folder='egypt', save=False)
#%%
fig62 = analyze_jobs_by_job_level(df_saudi[df_saudi['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_saudi",
                                  folder='saudi', save=False)
#%% md
# ## Visualization 7 : M-Level Job Entries Over Time
# 
# This line chart tracks the number of job postings for **Management-level (M-level)** roles from **November 2024 to April 2025**.
# 
# ### Key Insights
# 
# - **Consistent Growth**:
#   The number of M-level job postings increased steadily each month, showing sustained demand.
# 
# - **Sharp Growth Between Feb–Mar 2025**:
#   - February: ~400 jobs
#   - March: ~740 jobs
#   - This marks the most significant month-over-month growth.
# 
# - **Early Acceleration (Nov–Jan)**:
#   - Job entries started at a low point (~30 in Nov) and grew gradually through Jan (~230), indicating the early stages of hiring momentum.
# 
# - **Stabilization in April**:
#   - April saw continued growth (~840 jobs), but at a slower rate compared to the March surge.
# 
# 
# ### Overall Takeaway
# 
# The hiring trend for management-level roles has shown strong upward momentum over the past six months, particularly peaking in early 2025. This suggests increasing organizational needs for mid-to-senior management talent, likely driven by business expansion or restructuring initiatives.
# 
# 
# 
#%%
fig71 = plot_job_trend_over_time(df_egy, plot_name="plot_job_trend_over_time_egypt", folder='egypt',
                                 save=False)
#%%
fig72 = plot_job_trend_over_time(df_saudi, plot_name="plot_job_trend_over_time_saudi", folder='saudi',
                                 save=False)
#%% md
# ## Visualization 8: The Highest 10 Areas Declared for Business Opportunities
# 
# This bar chart illustrates the distribution of business opportunities across different domains, highlighting the most prominent areas based on the number of jobs declared. The chart provides insights into which sectors are currently experiencing the highest demand for business opportunities.
# 
# ### Key Insights
# 
# - **Dominance of "خدمات الدعم التجاري الأخرى" (Other Commercial Support Services)**:
#   - This domain leads by a significant margin with **3,240 job opportunities**, far exceeding all other sectors.
#   - This suggests that businesses in this area are actively seeking support services, possibly due to high operational needs or expansion plans.
# 
# - **Engineering Consultancy and Administrative Consulting**:
#   - Both "الاستشارات الهندسية العامة" (General Engineering Consultancy) and "الاستشارات الإدارية" (Administrative Consulting) show moderate activity, with **97** and **85** job opportunities, respectively.
#   - These sectors indicate a steady demand for professional advisory services, likely driven by infrastructure projects or organizational restructuring.
# 
# - **Low Activity in Traditional Sectors**:
#   - Traditional sectors such as "البناء والتشييد" (Construction and Building) and "التail بالتجزئة والجملة" (Retail and Wholesale Trade) have relatively low job counts (**35** and **30**, respectively).
#   - This could imply that these industries are either saturated or facing challenges in attracting new business opportunities.
# 
# - **Miscellaneous Categories**:
#   - Domains like "Unknown" and "التسويق" (Marketing) have minimal activity, indicating either limited data availability or less focus on these areas.
#   - "التعليم العالي" (Higher Education) and "الصحة والسكن" (Healthcare and Housing) also show low engagement, suggesting they might not be prioritized in current business strategies.
# 
# ### Overall Takeaway
# 
# The data reveals a **clear preference for service-oriented sectors**, particularly in *"Other Commercial Support Services"*, which dominates the landscape with over **3,000 job opportunities**.
# 
# Professional consulting services (*engineering* and *administrative*) remain active but at a much lower scale compared to the leading sector.
# 
# Traditional sectors such as *construction* and *retail* appear to be less attractive for business opportunities, potentially due to economic shifts or industry-specific challenges.
# 
# The dominance of support services highlights a trend toward outsourcing and specialized expertise, reflecting modern business practices focused on efficiency and scalability.
# 
# ### Recommendations
# 
# - **Focus on High-Demand Sectors**: Businesses should prioritize exploring opportunities in *"Other Commercial Support Services"* due to its overwhelming dominance.
# - **Diversify Investment**: While traditional sectors show low activity, they may present long-term growth potential. Companies can consider strategic investments in these areas for future expansion.
# - **Data Collection and Analysis**: Further investigation is needed to understand why certain sectors, like marketing and higher education, have minimal activity. This could involve analyzing market trends, regulatory factors, or industry-specific challenges.
# 
# ### Visual Summary
# 
# | Sector                                 | Arabic Name                             | Job Count |
# |----------------------------------------|------------------------------------------|-----------|
# | Other Commercial Support Services      | خدمات الدعم التجاري الأخرى               | 3,240     |
# | General Engineering Consultancy        | الاستشارات الهندسية العامة                | 97        |
# | Administrative Consulting              | الاستشارات الإدارية                      | 85        |
# | Construction and Building              | البناء والتشييد                          | 35        |
# | Retail and Wholesale Trade             | التجزئة والجملة                          | 30        |
# 
# This visualization underscores the importance of understanding sector-specific dynamics to identify lucrative business opportunities effectively.
#%%
fig81 = plot_job_postings_by_industry(df_egy, plot_name="plot_job_postings_by_industry_egypt",
                                       folder='egypt', save=False)
#%%
fig82 = plot_job_postings_by_industry(df_saudi, plot_name="plot_job_postings_by_industry_saudi",
                                       folder='saudi', save=False)
#%% md
# # ____________________________________________________________________________________
#%%
fig91 = analyze_job_type_distribution(df_egy, plot_name="analyze_job_type_distribution_egypt",
                                      folder='egypt', save=False)
#%%
fig92 = analyze_job_type_distribution(df_saudi, plot_name="analyze_job_type_distribution_saudi",
                                      folder='saudi', save=False)
#%% md
# # ____________________________________________________________________________________
#%%
fig101 = compare_experience_requirements(df_egy, plot_name="compare_experience_requirements_egypt",
                                         folder='egypt', save=False)
#%%
fig102 = compare_experience_requirements(df_saudi, plot_name="compare_experience_requirements_saudi",
                                         folder='saudi', save=False)
#%% md
# # ____________________________________________________________________________________
#%%
fig111 = jobs_heatmap_by_city_and_job_level(df_egy, plot_name="jobs_heatmap_by_city_and_job_level_egypt",
                                            folder='egypt', save=False)
#%%
fig112 = jobs_heatmap_by_city_and_job_level(df_saudi, plot_name="jobs_heatmap_by_city_and_job_level_saudi",
                                            folder='saudi', save=False)
#%% md
# # ____________________________________________________________________________________
#%%
fig121 = plot_top_job_titles_wordcloud(df_egy, plot_name="plot_top_job_titles_wordcloud_egypt",
                                       folder='egypt', save=False)
#%%
fig122 = plot_top_job_titles_wordcloud(df_saudi, plot_name="plot_top_job_titles_wordcloud_saudi",
                                       folder='saudi', save=False)