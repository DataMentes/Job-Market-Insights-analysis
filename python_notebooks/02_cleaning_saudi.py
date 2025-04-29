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
conn = sqlite3.connect('../database.db')
df2 = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
df2
#%%
from scripts.clean_data import *
import sqlite3
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
#%%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
df.title = df.title.str.lower().str.strip()
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
    for pattern in title_mapping.keys():

        matches = df.title[df.title.str.contains(pattern.lower(), regex=True, na=False)]
        print(pattern.center(80,'-'))
        print(matches)
        print('#'*80)
#%% md
# r"^(?!.*(?:cofounder|other)).*test"
#%%
test_title_mapping = {


}

review_matches(df, test_title_mapping)
#%%
delete_title_mapping1 = [
    'waiter and barista',
    'accountant and payroll specialist',
    'financial and administrative manager',
    'co-op 2025'

]

pattern1 = "|".join(delete_title_mapping1)
df = df[~df['title'].str.contains(pattern1, regex=True, na=False)]
df.title = df.title.str.replace(r'^((sr(\b|\s)|\ssr(\b|\s))|senior|junior|staff)','',regex=True).str.strip()
df.title = df.title.str.replace(r'^(\.|-|/)','',regex=True).str.strip()
df.title = df.title.str.replace(r'(\.|\-|/|\,)$', '', regex=True).str.strip()

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
    r'assistant manager': 'assistant director',
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
    r"consultant plastic": "consultant plastic surgeon"






    # r'^treasurer$': 'treasury specialist',
    # r'^treasur(y|er)\s?(specialist|senior specialist|and| - emea).*': 'treasury specialist',
    # r'^treasury senior accountant': 'treasury accountant',
    # r'^treasury (section|head).*': 'treasury lead',
    # r'technical support': 'Support Engineer',
    # r'technical support &': 'Support manager',
    # r'service manager': 'service manager',
    # r'(?<!assistant )sales manager': 'sales manager',
    # r'(?<!ai )product manager': 'product manager',
    # r'ai product manager': "AI Product Manager",
    # r'office manager': 'office manager',
    # r'^(?!.*\b(architecture|electrical|mechanical)\b).*office engineer.*': 'office engineer',
    # r'(?i)(?=.*\b(?:mechanical)\b).*\boffice engineer\b.*': 'mechanical office engineer',
    # r'(?i)(?=.*\b(?:electrical)\b).*\boffice engineer\b.*': 'electrical office engineer',
    # r'(?i)(?=.*\b(?:architecture)\b).*\boffice engineer\b.*': 'architecture office engineer',
    # r'it operations': 'IT Support',
    # r'(?<!ai )engineering manager': 'engineering manager',
    # r'^technical consulting.*': 'technical consulting',
    # r'training manager': 'training manager',
    # r'^tech lead \(ai/ml\)': "AI/ML Lead",
    # r'data scientist': 'data scientist',
    # r'^team lead data scientist': "data scientist Lead",
    # r'^tax accountant.*': 'Accountant',
    # r'^tax & legal.*': 'Accountant',
    # r'talent acquisition (specialist|partner|&).*': 'Talent Acquisition Specialist',
    # r'^talent acquisition and learning and development specialist': 'Talent Acquisition Specialist',
    # r'^talent acquisition .*(manager|head).*': 'Talent Acquisition Manager',
    # r'system(s)? engineer.*': 'system engineer',
    # r'^(?!.*manager).*supply (chain|planning|demand|analyst).*': 'supply chain analyst',
    # r'(?i)(?=.*\b(?:(manager|management))\b).*\bsupply (chain|planning|demand|analyst)\b.*': 'supply chain manager',
    # r'supply chain executive': 'supply chain lead',
    # r'^technical|tech lead': 'Technical Lead',
    # r'store manager.*': 'store manager',
    # r'(?!.*\b(backend|frontend|mobile|lead|.net)\b).*^software engineer.*': 'software engineer',
    # r'testing engineer|tester': 'testing engineer',
    # r'quality engineer': 'quality engineer',
}


for pattern, replacement in edite_title_mapping.items():
    df.title[df.title.str.contains(pattern, regex=True)] = replacement.lower()




#delete_title_mapping2 = []
#
#pattern2 = "|".join(delete_title_mapping2)
#df = df[~df['title'].str.contains(pattern2, regex=True, na=False)]


df.sort_values(by=['title'], ascending=True, inplace=True)
df