# Data cleaning functions here
from deep_translator import GoogleTranslator
from langdetect import detect
import numpy as np
import pandas as pd
from datetime import datetime


def translate_if_arabic(text, no_detect=False):
    """
    Translates the given text to English if it is in Arabic.

    Args:
        text (str): The text to translate.
        no_detect (bool, optional): If True, skips language detection and always attempts to translate. Defaults to False.

    Returns:
        str: The translated text (if Arabic) or the original text (if not Arabic or if translation fails).
    """
    if not text or not isinstance(text, str):  # Check if the text is empty or not a string.  If so, return it unchanged.
        return text

    if not no_detect:  # If no_detect is False (the default), perform language detection.
        try:
            lang = detect(text)  # Detect the language of the text.
            if lang == 'ar':  # If the language is Arabic ('ar'), translate it to English.
                return GoogleTranslator(source='ar', target='en').translate(text)  # Use Google Translate to translate from Arabic to English.
            else:
                return text  # If the language is not Arabic, return the original text.
        except:
            return text  # If any error occurs during language detection, return the original text.
    else:  # If no_detect is True, skip language detection and attempt to translate directly.
        try:
            return GoogleTranslator(source='ar', target='en').translate(text)  # Use Google Translate to translate from Arabic to English.
        except:
            return text  # If any error occurs during translation, return the original text.



def apply_translation(data, column, rows='all'):
    """
    Applies the translate_if_arabic function to a specified column in a DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing the column to translate.
        column (str): The name of the column to translate.
        rows (str or list, optional):  Specifies which rows to translate.
            - 'all': Translate all rows in the column.
            - list: A list of row indices to translate. Defaults to 'all'.
    """
    if rows == 'all':  # If rows is 'all', apply the translation to the entire column.
        data[column] = data[column].apply(translate_if_arabic)  # Apply the translate_if_arabic function to each element of the column.
    else:  # If rows is a list, translate only the specified rows.
        for row in rows:  # Iterate over the specified row indices.
            data.at[row, column] = translate_if_arabic(data.at[row, column], no_detect=True)  # Translate the text in the specified row and column.  no_detect is set to True here.



def split_column(df, column, index: list, split_char: str, names: list, fill_value='Unknown', reverse=False):
    """
    Splits a column in a DataFrame into multiple columns based on a delimiter.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to split.
        column (str): The name of the column to split.
        index (list): A list of indices indicating which part of the split string to use for each new column.
        split_char (str): The character used to split the column's values.
        names (list): A list of names for the new columns.
        fill_value (str, optional): The value to use if a split string does not have enough parts. Defaults to 'Unknown'.
        reverse (bool, optional): If True, the split parts are taken from the end of the string. Defaults to False.
    """
    df[column].fillna('Unknown', inplace=True)  # Fill any missing values in the specified column with 'Unknown'.
    reverse = -1 if reverse else 1  # Determine the direction of indexing based on the 'reverse' parameter.
    for i, name in zip(index, names):  # Iterate over the indices and new column names.
        df[name] = df[column].str.split(split_char).apply(  # Split the column's values by 'split_char' and apply a lambda function.
            lambda x: x[::reverse][i].strip() if i < len(x) else fill_value)  # Extract the i-th part of the split string (from the start or end), or use fill_value if the string doesn't have enough parts, and remove leading/trailing spaces.



def split_career_level(df):
    """
    Splits the 'career_level' column in a DataFrame into 'type', 'exp', and 'no_exp' columns.
    Handles errors where 'type' or 'exp' might be incorrectly assigned.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'career_level' column.
    """
    split_column(df, 'career_level', [0, 1, 2], '·', ['type', 'exp', 'no_exp'], reverse=False)  # Split the 'career_level' column.
    type_error = df[df['type'].str.len() > 10].index  # Find rows where 'type' has an unusually long value (likely an error).
    df['exp'][type_error] = df['type'][type_error]  # Move the value from 'type' to 'exp' for these rows.
    df['type'][type_error] = 'Unknown'  # Set 'type' to 'Unknown' for these rows.
    exp_error = df[df['exp'].str.len() > 15].index  # Find rows where 'exp' has an unusually long value (likely an error).
    df['no_exp'][exp_error] = df['exp'][exp_error]  # Move the value from 'exp' to 'no_exp' for these rows.
    df['exp'][exp_error] = 'Unknown'  # Set 'exp' to 'Unknown' for these rows.



def split_industry(df):
    """
    Splits the 'industry' column in a DataFrame into 'industry_' and 'company_size' columns.
    Handles errors where 'industry_' and 'company_size' might be incorrectly assigned.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'industry' column.
    """
    split_column(df, 'industry', [0, 1], '·', ['industry_', 'company_size'], fill_value='Unknown', reverse=True)  # Split the 'industry' column.
    index = df[df['industry_'].str.contains("موظف", na=False)].index  # Find rows where 'industry_' contains "موظف" (likely an error).
    df['industry_'][index] = df['company_size'][index]  # Move the value from 'company_size' to 'industry_' for these rows.
    df['company_size'][index] = 'Unknown'  # Set 'company_size' to 'Unknown' for these rows.



def split_num_of_exp_years(df):
    """
    Splits the 'num_of_exp_years' column into 'min_num_of_years' and 'max_num_of_years'.
    Extracts numeric values representing the minimum and maximum years of experience.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'num_of_exp_years' column.
    """
    df['num_of_exp_years'].fillna(np.nan, inplace=True)  # Fill missing values in 'num_of_exp_years' with NaN.

    def extract_years(text):
        """
        Extracts the minimum and maximum number of years from a text string.

        Args:
            text (str): The text string containing the years of experience.

        Returns:
            tuple: A tuple containing the minimum and maximum years of experience (or 'Unknown' if not found).
        """
        if pd.isna(text):  # If the text is NaN, return None, None.
            return None, None
        matches = pd.Series(str(text)).str.findall(r'(\d+)').iloc[0]  # Find all sequences of digits in the text.
        if matches:  # If any digits were found.
            if len(matches) == 1:  # If only one number was found, it's the minimum.
                return int(matches[0]), 'Unknown'
            elif len(matches) >= 2:  # If two or more numbers were found, they are min and max.
                return int(matches[0]), int(matches[1])

        return 'Unknown', 'Unknown'  # If no numbers were found, return 'Unknown' for both.
    df[['min_num_of_years', 'max_num_of_years']] = df['num_of_exp_years'].apply(lambda x: pd.Series(extract_years(x)))  # Apply the extract_years function to the column and create two new columns.

    df.drop(columns=['num_of_exp_years'], inplace=True)  # Drop the original 'num_of_exp_years' column.



def analyses_date(df, num_days):
    """
    Analyzes and transforms the 'date' column in a DataFrame.  This function appears to normalize date information.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'date' column.
        num_days (int):  An integer representing number of days.
    """
    df.dropna(subset=['date'], inplace=True)  # Remove rows where the 'date' column has missing values.

    df.loc[df['date'].str.contains(r'اليوم'), 'date'] = '0'  # Replace "اليوم" (today) with '0'.
    df.loc[df['date'].str.contains(r'في الامس'), 'date'] = '1'  # Replace "في الامس" (yesterday) with '1'.
    df.loc[df['date'].str.contains(r'قبل يومين'), 'date'] = '2'  # Replace "قبل يومين" (two days ago) with '2'.
    index_plus = df['date'].str.contains(r'\+')  # Identify rows where 'date' contains '+'.

    df['date'] = df['date'].str.extract(r'([0-9]+)').astype(float).astype('Int64')  # Extract the first number from the 'date' string, convert to float, then to integer.

    number_jobs = index_plus.sum() # Calculate the number of jobs which has '+' in their date
    initial_value = 2 * number_jobs / num_days # calculate initial value
    daily_jobs = np.linspace(initial_value, 0, num_days) # Create an array of evenly spaced values
    daily_jobs = np.round(daily_jobs).astype(int) # Round the values to integers
    np.random.seed(42)
    random_jobs = [max(0, job + np.random.randint(-10, 10)) for job in daily_jobs] # Add some randomness
    random_jobs = np.array(random_jobs)

    difference = number_jobs - random_jobs.sum() # calculate the difference
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

    df['date'][index_plus] = df['date'][index_plus] + np.array(final_list)  # Add the values from `final_list` to the 'date' column for the selected rows.
    df.sort_values(by=['date'], inplace=True)  # Sort the DataFrame by the 'date' column.

    reference_date = datetime(2025, 4, 15)  # Define a reference date.
    df['date'] = reference_date - pd.to_timedelta(df['date'], unit='D')  # Calculate the date by subtracting a timedelta from the reference date.  This converts the 'date' column to actual dates.



def extract_job_grade(df, column='title'):
    """
    Extracts job grade information from a specified column (default: 'title') in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the job title column.
        column (str, optional): The name of the column containing job titles. Defaults to 'title'.
    """
    df[column].fillna('Unknown', inplace=True)  # Fill missing values in the specified column with 'Unknown'.

    mapping_dict0 = {'Graduate': 'i', 'Junior': 'ii', 'Mid Level':'iii', 'Senior':'iv',
                     'Management':'v', 'Senior Management':'vi', 'C-Suite':'vii'}
    mapping_dict = {
        'Graduate': ['trainee', 'intern', 'entry-level', 'graduate', 'internship', 'interns', 'تمهير', 'تدريب'],
        'Junior': ['junior'],
        'Mid Level': ['mid-level','intermediate'],
        'Senior': ['senior','supervisor','section head',r'(^sr(\b|\s)|\ssr(\b|\s))','senior associate'],
        'Management': ['manager', 'principal', 'assistant director'],
        'Senior Management': ['senior manager','director', 'vice president', 'svp', 'group manager'],
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
    """
    Extracts gender information from a specified column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the gender information.
        column (str): The name of the column containing gender-related text.
    """
    df[column].fillna('Unknown', inplace=True)  # Fill missing values in the specified column with 'Unknown'.
    index_male = df[column].str.contains(r'(m|M)ale|\b(m|M)en\b|\b(m|M)an\b', regex=True)  # Find rows containing male-related terms.
    df.loc[index_male, 'gender'] = 'Male'  # Assign 'Male' to the 'gender' column for these rows.
    index_Female = df[column].str.contains('(f|F)emale|(w|W)omen')  # Find rows containing female-related terms.
    df.loc[index_Female, 'gender'] = 'Female'  # Assign 'Female' to the 'gender' column for these rows.



def extract_remotely(df, column):
    """
    Extracts remote work information from a specified column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the remote work information.
        column (str): The name of the column containing remote work-related text.
    """
    df[column].fillna('Unknown', inplace=True)  # Fill missing values in the specified column with 'Unknown'.
    data = {
        'Remote': r'remote\b|remotely',  # Define patterns for 'Remote' and 'Hybrid'.
        'Hybrid': r'hybrid\b'
    }
    for key, value in data.items():  # Iterate over the patterns.
        index = df[column].str.contains(value)  # Find rows matching the pattern.
        df.loc[index, 'remote'] = key  # Assign the corresponding key ('Remote' or 'Hybrid') to the 'remote' column.



def translate_experience(df):
    """
    Translates experience-related values in the 'job_level' column of a DataFrame and renames the column.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'experience_' column.
    """
    df['job_level'] = df['experience_']  # Copy the values from 'experience_' to 'job_level'.
    df.drop(columns=['experience_'], inplace=True)  # Drop the original 'experience_' column.
    dict = {  # Define a dictionary to map Arabic experience levels to English.
        'لا تفضيل': 'No Preference',
        'خريج جديد': 'Graduate',
        'متوسط الخبرة': 'Mid Level',
        'مبتدئ الخبرة': 'Junior',
        'إدارة عليا': 'Senior Management',
        'إدارة عليا تنفيذية': 'C-Suite',
        'إدارة': 'Management'
    }

    df['job_level'] = df['job_level'].replace(dict)  # Replace the Arabic values with English values.



def translate_type(df):
    """
    Translates job type values in the 'type' column of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'type' column.
    """
    dict = {  # Define a dictionary to map Arabic job types to English.
        'دوام كامل': 'Full-Time',
        'إدارة': 'Management',
        'تدريب': 'Intern',
        'دوام جزئي': 'Part-Time',
        'عقود': 'Contracts',
        'مؤقت': 'Temporary'
    }

    df['type'] = df['type'].replace(dict)  # Replace the Arabic values with English values.



def translate_sex(df):
    """
    Translates gender-related values in the 'gender' column of a DataFrame and renames the column

    Args:
        df (pd.DataFrame): The DataFrame containing the 'sex' column.
    """
    df['gender'] = df['sex']  # Copy the values from 'sex' to 'gender'.
    df.drop(columns=['sex'], inplace=True)  # Drop the original 'sex' column.
    dict = {  # Define a dictionary to map Arabic gender values to English.
        'لا تفضيل': 'No Preference',
        'ذكر': 'Male',
        'انثي': 'Female',
        'أنثى': 'Female',
    }

    df['gender'] = df['gender'].replace(dict)  # Replace the Arabic values with English values.



def translate_remote(df):
    """
    Translates remote work values in the 'remote' column of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the 'remote' column.
    """
    dict = {  # Define a dictionary to map Arabic remote work values to English.
        'من المقر': 'On-site',
        'عن بُعد': 'Remote',
        'هجين': 'Hybrid'
    }

    df['remote'] = df['remote'].replace(dict)  # Replace the Arabic values with English values.



def review_matches(df, title_mapping):
    """
    Prints the job titles from the DataFrame that match the keys in the title_mapping.

    Args:
        df (pd.DataFrame): The DataFrame containing the job titles.
        title_mapping (dict): A dictionary where keys are patterns to search for in job titles.
    """

    pd.set_option('display.max_rows', None)  # Set pandas to display all rows without truncation.
    pd.set_option('display.max_colwidth', None)  # Set pandas to display the full width of the column.

    for pattern in title_mapping.keys():  # Iterate over the keys (patterns) in the title_mapping dictionary.

        matches = df.title[df.title.str.contains(pattern.lower(), regex=True, na=False)]  # Find job titles that contain the pattern (case-insensitive).
        print(pattern.center(120,'-'))  # Print the pattern, centered and padded with dashes.
        print(matches)  # Print the matching job titles.
        print('#'*120)  # Print a separator line.



def edite_title(df,title_mapping):
    """
    Edits job titles in a DataFrame based on a provided mapping.

    Args:
        df (pd.DataFrame): The DataFrame containing the job titles.
        title_mapping (dict): A dictionary where keys are patterns to search for and values are the replacements.
    """

    for pattern, replacement in title_mapping.items():  # Iterate over the key-value pairs in the title_mapping dictionary.
        df.title[df.title.str.contains(pattern, regex=True)] = replacement.lower()  # Replace titles matching the pattern with the lowercase replacement.

    df.title = df.title.str.title()  # Convert the first letter of each word in the title to uppercase, and the rest to lowercase.
