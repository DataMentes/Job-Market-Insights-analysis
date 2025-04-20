# Data cleaning functions here
from deep_translator import GoogleTranslator
from langdetect import detect


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
