#%% md
# ### Import required libraries
# 
# - Import `clean_data` module from `scripts`.
# - Import `sqlite3` for database interaction.
# - Import `warnings` and disable warnings.
# - Import `pandas` for data manipulation.
#%%
from scripts.clean_data import *
import sqlite3
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
#%% md
# ### Load and preview data
# 
# - Load CSV file `saudi-arabia_raw.csv` from `../data/raw/` into DataFrame.
# - Display first 15 rows of the DataFrame.
#%%
df = pd.read_csv('../data/raw/saudi-arabia_raw.csv')
df.head(15)
#%% md
# ### Split location and career_level columns
# 
# - Split `location` column by separator `·`, keep index 1 as `city`.
# - Further process `career_level` column using `split_career_level` function.
#%%
split_column(df, 'location', [1], '·', ['city'], reverse=True)
split_career_level(df)
df.head(15)
#%% md
# ### Clean and combine experience columns
# 
# - Replace 'Unknown' values in `exp` column with `NaN`.
# - Combine `experience` column with `exp` column into a new column `experience_` using `combine_first`.
# - Replace 'Unknown' values in `no_exp` column with `NaN`.
# - Combine `num_of_exp` column with `no_exp` column into a new column `num_of_exp_years` using `combine_first`.
#%%
df['exp'].replace('Unknown', np.nan, inplace=True)
df['experience_'] = df['experience'].combine_first(df['exp'])
df['no_exp'].replace('Unknown', np.nan, inplace=True)
df['num_of_exp_years'] = df['num_of_exp'].combine_first(df['no_exp'])
df.head(15)
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
split_industry(df)
split_column(df, 'location', index=[1], split_char='·', names=['city'],reverse=True)
split_column(df, 'num_of_vacancies', index=[3], split_char=' ', names=['num_of_vacancies'], fill_value=1)
df.head(15)
#%% md
# ### Fill Missing Values in Columns
# 
# 1. **Fill missing values in the `remote` column** with `'من المقر'` to indicate office-based positions.
# 2. **Fill missing values in the `age` column** with `'لا تفضيل'` to represent no preference regarding age.
# 3. **Fill missing values in the `sex` column** with `'لا تفضيل'` to represent no preference regarding sex.
# 4. **Fill missing values in the `experience_` column** with `'لا تفضيل'` to represent no preference regarding experience.
# 5. **Fill missing values in the `num_of_exp_years` column** with `'لا تفضيل'` to represent no preference regarding years of experience.
#%%
df['remote'].fillna('من المقر', inplace=True)
df['age'].fillna('لا تفضيل', inplace=True)
df['sex'].fillna('لا تفضيل', inplace=True)
df['experience_'].fillna('لا تفضيل', inplace=True)
df['num_of_exp_years'].fillna('لا تفضيل', inplace=True)
df.head(15)
#%% md
# ### Drop Unnecessary Columns
# 
#  * **Remove columns** from the DataFrame that are not needed for further analysis:
#    - `age`, `exp`, `no_exp`, `num_of_exp`, `experience`, `career_level`, `industry`, `location`, `link`, `Unnamed: 0`, `salary`, `nationality`, `residence_area`, `qualification`, `specialization`.
#%%
df.drop(columns=['age', 'exp', 'no_exp', 'num_of_exp', 'exp', 'experience', 'career_level', 'industry', 'location', 'link','Unnamed: 0','salary', 'nationality', 'residence_area', 'qualification', 'specialization'],
        inplace=True)
df.head(15)
#%% md
# ### Analyze Date Data
# 
# * **Call `analyses_date()` function** to analyze the date data in the DataFrame (`df`):
#    - Parameter `num_days=120` specifies the number of days to consider for analysis.
#%%
analyses_date(df, num_days = 120)
df.head(15)
#%% md
# ### Sort and Save Data
# 
# 1. **Sort the DataFrame** by the 'title' column in descending order:
#    - The `ascending=False` argument sorts the data in descending order.
# 
# 2. **Save the DataFrame to an SQLite database** (commented-out code)
# 
#%%
df.sort_values(by=['title'], ascending=False, inplace=True)
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
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
df.sort_values(by=['title'], ascending=False, inplace=True)
apply_translation(df, 'title', rows=df.iloc[:400, :].index.tolist())
# df.to_sql('saudi-arabia', con=conn, if_exists='replace', index=True)
conn.close()
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
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
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
df.drop(columns=['description', 'skills'], inplace=True)
split_num_of_exp_years(df)
conn = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace', index=False)
conn.close()
df
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
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
df['title'] = df['title'].str.replace(r'^\d+\.', '', regex=True).str.strip()
df['title'] = df['title'].str.replace(r'^a\s\b', '', regex=True).str.strip()
df.title = df.title.str.lower()
df.sort_values(by=['title'], inplace=True)
df
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
edite_title_mapping = {
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
    r'sales manager / account manager':'sales manager / account manager',
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
    r'^(?!.*(?:supervisor)).*service sales' : 'service sales engineer',
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
#%%
df.title.value_counts()
#%%
pattern_replace =r'(^((sr(\b|\s)|\ssr(\b|\s))|senior|junior|staff|female|\bmen\b|\bmale\b|women(\'s)|tpe (iv|iii|ii|i|v)(\s)?(-|/)?)( (senior|graduate))?|^graduate|^trainee\b( -)?)(\s)?(\.|-|/|\\)?|(\.|\-|/|\,|\\)$'
df.title = df.title.str.replace(pattern_replace,'',regex=True).str.strip()
#%%
review_matches(df,edite_title_mapping)
#%%
edite_title(df,edite_title_mapping)
df.title.value_counts()
#%%
conn = sqlite3.connect('../database.db')
# df.to_sql('saudi-arabia', con=conn, if_exists='replace', index=False)
conn.close()
df.title