# Data cleaning functions here
from deep_translator import GoogleTranslator
from langdetect import detect
import numpy as np
import pandas as pd
from datetime import datetime


def translate_if_arabic(text, no_detect=False):
    if not text or not isinstance(text, str):
        return text

    if not no_detect:
        try:
            lang = detect(text)
            if lang == 'ar':
                return GoogleTranslator(source='ar', target='en').translate(text)
            else:
                return text
        except:
            return text
    else:
        try:
            return GoogleTranslator(source='ar', target='en').translate(text)
        except:
            return text


def apply_translation(data, column, rows='all'):
    if rows == 'all':
        data[column] = data[column].apply(translate_if_arabic)
    else:
        for row in rows:
            data.at[row, column] = translate_if_arabic(data.at[row, column], no_detect=True)


def split_column(df, column, index: list, split_char: str, names: list, fill_value='Unknown', reverse=False):
    df[column].fillna('Unknown', inplace=True)
    reverse = -1 if reverse else 1
    for i, name in zip(index, names):
        df[name] = df[column].str.split(split_char).apply(
            lambda x: x[::reverse][i].strip() if i < len(x) else fill_value)


def split_career_level(df):
    split_column(df, 'career_level', [0, 1, 2], '·', ['type', 'exp', 'no_exp'], reverse=False)
    type_error = df[df['type'].str.len() > 10].index
    df['exp'][type_error] = df['type'][type_error]
    df['type'][type_error] = 'Unknown'
    exp_error = df[df['exp'].str.len() > 15].index
    df['no_exp'][exp_error] = df['exp'][exp_error]
    df['exp'][exp_error] = 'Unknown'


def split_industry(df):
    split_column(df, 'industry', [0, 1], '·', ['industry_', 'company_size'], fill_value='Unknown', reverse=True)
    index = df[df['industry_'].str.contains("موظف", na=False)].index
    df['industry_'][index] = df['company_size'][index]
    df['company_size'][index] = 'Unknown'


def split_num_of_exp_years(df):

    df['num_of_exp_years'].fillna(np.nan, inplace=True)

    def extract_years(text):
        if pd.isna(text):
            return None, None
        matches = pd.Series(str(text)).str.findall(r'(\d+)').iloc[0]
        if matches:
            if len(matches) == 1:
                return int(matches[0]), 'Unknown'
            elif len(matches) >= 2:
                return int(matches[0]), int(matches[1])

        return 'Unknown', 'Unknown'
    df[['min_num_of_years', 'max_num_of_years']] = df['num_of_exp_years'].apply(lambda x: pd.Series(extract_years(x)))

    df.drop(columns=['num_of_exp_years'], inplace=True)


def analyses_date(df, num_days):
    df.dropna(subset=['date'], inplace=True)

    df.loc[df['date'].str.contains(r'اليوم'), 'date'] = '0'
    df.loc[df['date'].str.contains(r'في الامس'), 'date'] = '1'
    df.loc[df['date'].str.findall(r'قبل يومين'), 'date'] = '2'
    index_plus = df['date'].str.contains(r'\+')

    df['date'].str.extract(r'([0-9]+)').astype(float).astype('Int64')

    number_jobs = index_plus.sum()
    initial_value = 2 * number_jobs / num_days
    daily_jobs = np.linspace(initial_value, 0, num_days)
    daily_jobs = np.round(daily_jobs).astype(int)
    np.random.seed(42)
    random_jobs = [max(0, job + np.random.randint(-10, 10)) for job in daily_jobs]
    random_jobs = np.array(random_jobs)

    difference = number_jobs - random_jobs.sum()
    if difference != 0:
        random_jobs[:abs(difference)] += np.sign(difference)

    days_list = list(range(1, num_days + 1))
    jobs_distribution = list(zip(days_list, daily_jobs))

    final_list = []
    for day, jobs in jobs_distribution:
        if jobs != 0:
            final_list.extend([day] * jobs)

    if len(final_list) < number_jobs:
        final_list.extend([0] * (number_jobs - len(final_list)))
    elif len(final_list) > number_jobs:
        final_list = final_list[:number_jobs]

    df['date'][index_plus] = df['date'][index_plus] + final_list
    df.sort_values(by=['date'], inplace=True)

    reference_date = datetime(2025, 4, 15)
    df['date'] = reference_date - pd.to_timedelta(df['date'], unit='D')


def extract_job_grade(df, column='title'):
    df[column].fillna('Unknown', inplace=True)

    mapping_dict0 = {'Graduate': 'i', 'Junior': 'ii', 'Mid Level':'iii', 'Senior':'iv',
                     'Management':'v', 'Senior Management':'vi', 'C-Suite':'vii'}
    mapping_dict = {
        'Graduate': ['trainee', 'intern', 'entry-level', 'graduate', 'internship', 'interns', 'تمهير', 'تدريب'],
        'Junior': ['junior'],
        'Mid Level': ['mid-level'],
        'Senior': ['senior','supervisor','section head',r'(^sr(\b|\s)|\ssr(\b|\s))','senior associate'],
        'Management': ['manager', 'principal', 'assistant director'],
        'Senior Management': ['director', 'vice president', 'svp', 'group manager'],
        'C-Suite': ['c-suite', 'ceo', 'chief executive officer', 'cfo', 'chief financial officer',
                    'cio', 'chief information officer', 'coo', 'chief operating officer',
                    'cto', 'chief technology officer', 'cmo', 'chief marketing officer']
    }
    list = [
        mapping_dict0,
        mapping_dict
    ]
    for i in [0,1]:
        for key in list[i]:
            regex = r'\b|'.join(list[i][key]) + r'\b' if i else rf'(\s|-){list[i][key]}($|\s|\,|- )'
            if key == 'Senior Management' and i:
                regex = r'(?<!\bassistant\s)\bdirector\b|' + r'\b|'.join(list[i][key][1:]) + r'\b'
            mask = df[column].str.contains(regex, regex=True)
            if key == 'Graduate':
                df.loc[mask, 'type'] = 'Intern'
            if key == 'Management' or key == 'Senior Management' or key == 'C-Suite':
                df.loc[mask, 'type'] = 'Management'
            df.loc[mask, 'job_level'] = key


def extract_gender(df, column):
    df[column].fillna('Unknown', inplace=True)
    index_male = df[column].str.contains(r'(m|M)ale|\b(m|M)en\b|\b(m|M)an\b', regex=True)
    df.loc[index_male, 'gender'] = 'Male'
    index_Female = df[column].str.contains('(f|F)emale|(w|W)omen')
    df.loc[index_Female, 'gender'] = 'Female'


def extract_remotely(df, column):
    df[column].fillna('Unknown', inplace=True)
    data = {
        'Remote': r'remote\b|remotely',
        'Hybrid': r'hybrid\b'
    }
    for key, value in data.items():
        index = df[column].str.contains(value)
        df.loc[index, 'remote'] = key


def translate_experience(df):
    df['job_level'] = df['experience_']
    df.drop(columns=['experience_'], inplace=True)
    dict = {
        'لا تفضيل': 'No Preference',
        'خريج جديد': 'Graduate',
        'متوسط الخبرة': 'Mid Level',
        'مبتدئ الخبرة': 'Junior',
        'إدارة عليا': 'Senior Management',
        'إدارة عليا تنفيذية': 'C-Suite',
        'إدارة': 'Management'
    }

    df['job_level'] = df['job_level'].replace(dict)


def translate_type(df):
    dict = {
        'دوام كامل': 'Full-Time',
        'إدارة': 'Management',
        'تدريب': 'Intern',
        'دوام جزئي': 'Part-Time',
        'عقود': 'Contracts',
        'مؤقت': 'Temporary'
    }

    df['type'] = df['type'].replace(dict)


def translate_sex(df):
    df['gender'] = df['sex']
    df.drop(columns=['sex'], inplace=True)
    dict = {
        'لا تفضيل': 'No Preference',
        'ذكر': 'Male',
        'انثي': 'Female',
        'أنثى': 'Female',
    }

    df['gender'] = df['gender'].replace(dict)


def translate_remote(df):
    dict = {
        'من المقر': 'On-site',
        'عن بُعد': 'Remote',
        'هجين': 'Hybrid'
    }

    df['remote'] = df['remote'].replace(dict)
