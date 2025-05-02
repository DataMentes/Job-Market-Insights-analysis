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
df.drop(columns=['age', 'description', 'skills', 'qualification', 'specialization', 'level_0', 'index'], axis=1,
        inplace=True)
#%%
# df.to_sql('EGYPT', con=conn, if_exists='replace')
conn.close()
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
df.title.value_counts()
#%%
df = df[~df['title'].str.contains('saudi', na=False)]
pattern_replace = r'^((sr(\b|\s)|\ssr(\b|\s))|senior|junior|staff|female|\bmen\b|\bmale\b|women(\'s)|tpe (iv|iii|ii|i|v)(\s)?(-|/)?)( (senior|graduate))?|graduate|trainee\b( -)?'
df.title = df.title.str.replace(pattern_replace, '', regex=True).str.strip()
df.title = df.title.str.replace(r'^(\.|\-|/|\,|\\)', '', regex=True).str.strip()
df.title = df.title.str.replace(r'(\.|\-|/|\,|\\)+$', '', regex=True).str.strip()
df = df.sort_values(by="title", ascending=False, key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
final_mapping_title = {
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
#%%
# ^(?!.*(?:manager)).*
# (?=.*(logistics))
regex = r'(?=.*(Account))(?=.*(Manager))(?=.*(Sale))'
df[df.title.str.contains(regex, regex=True) == True][
    ['title', 'job_level', 'min_num_of_years', 'max_num_of_years']]
#%%
for pattern, replacement in final_mapping_title.items():
    df.title[df.title.str.contains(pattern, regex=True)] = replacement.lower()
#%%
df.title.str.lower().value_counts()
#%%
df = df.sort_values(by="title", key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
unique = pd.DataFrame(df.title.value_counts()).reset_index().rename(
    columns={'index': 'title', 'count': 'count'}).sort_values(by="title",
                                                              key=lambda col: col.str.lower()).reset_index(drop=True)
#%%
df.title = df.title.str.title()
df.drop('index', axis=1, inplace=True)
#%%
conn = sqlite3.connect('../database.db')
df.to_sql('EGYPT', con=conn, if_exists='replace')
conn.close()
#%%
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def review_matches(df, title_mapping):
    """
    البحث عن الأنماط المحددة في القاموس `title_mapping` داخل عمود `title` في DataFrame `df`.

    المدخلات:
        df (pd.DataFrame): الجدول الذي يحتوي على البيانات.
        title_mapping (dict): قاموس يحتوي على الأنماط المراد البحث عنها.

    المخرجات:
        قائمة بالنتائج التي تم العثور عليها.
    """
    for pattern, label in title_mapping.items():
        matches = df.title[df.title.str.contains(pattern.lower(), regex=True)]
        print(label.center(120, '~'))
        print(pattern.center(120, '='))
        print(str(len(matches)).center(120, '-'))
        print(matches)
        print('#' * 120)
#%%
test_title_mapping = {}
review_matches(df, test_title_mapping)
#%%
