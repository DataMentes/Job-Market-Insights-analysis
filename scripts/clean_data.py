# Data cleaning functions here
from deep_translator import GoogleTranslator
from langdetect import detect
import pandas as pd

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


def split_column(df : pd.DataFrame, column, index, split_char , names, fill_value='Unknown'):
    col = df[column]
    result = pd.DataFrame(columns=names)
    for row in col:
        string_value = str(row)
        split_list = string_value.split(split_char)
        values = []
        for i in index:
            values.append(split_list[index].strip() if index < len(split_list) else fill_value)
        pd.concat(result, values)

    df = pd.merge(df, result, on=index)