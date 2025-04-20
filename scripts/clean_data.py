# Data cleaning functions here
from deep_translator import GoogleTranslator
from langdetect import detect
import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta


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
            return GoogleTranslator(source='auto', target='en').translate(text)
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
    split_column(df, 'career_level', [0, 1, 2], '·', ['type', 'exp', 'no_exp'], reverse=True)
    index = df[df['exp'].str.len() > 15].index
    df['no_exp'][index] = df['exp'][index]
    df['exp'][index] = 'Unknown'


def split_industry(df):
    split_column(df, 'industry', [0, 1], '·', ['industry_', 'company_size'], fill_value='Unknown', reverse=True)
    index = df[df['industry_'].str.contains("موظف", na=False)].index
    df['industry_'][index] = df['company_size'][index]
    df['company_size'][index] = 'Unknown'


def analyses_date(df, num_days):
    df.dropna(subset=['date'], inplace=True)

    df.loc[df['date'].str.contains(r'اليوم'), 'date'] = '0'
    df.loc[df['date'].str.contains(r'في الامس'), 'date'] = '1'
    df.loc[df['date'].str.contains(r'قبل يومين'), 'date'] = '2'
    index_plus = df['date'].str.contains(r'\+')

    df['date'] = df['date'].apply(lambda x: int(re.findall(r'[0-9]+', str(x))[0]))

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