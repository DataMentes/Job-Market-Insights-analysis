import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
from typing import Literal




def job_distribution_by_city(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], top_n=10):

    job_counts = df['city'].value_counts().reset_index()
    job_counts.columns = ['City', 'Number of Jobs']
    top_cities = job_counts.head(top_n)

    fig = None
    # Prepare Arabic text
    reshaped_labels = [get_display(arabic_reshaper.reshape(city)) for city in top_cities['City']]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(reshaped_labels, top_cities['Number of Jobs'], color='#20B2AA')
    ax.tick_params(axis='x', labelsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel(get_display(arabic_reshaper.reshape('Number of Jobs')), fontsize=13)
    ax.set_title(get_display(arabic_reshaper.reshape(f'Top {top_n} Cities by Number of Jobs')), fontsize=14)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def analyze_jobs_by_company(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], top_n=20):
    # Check if the 'company' column exists in the data
    if 'company_name' not in data.columns:
        raise ValueError("The 'company' column is missing from the data")

    # Count the number of jobs for each company
    company_counts = data['company_name'].value_counts().head(top_n)

    # Plotting the bar chart inside the function
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=company_counts.index, y=company_counts.values, palette='viridis')

    # Adding titles and labels
    ax.set_title('Number of Jobs by Company', fontsize=16)
    ax.set_xlabel('Company Name', fontsize=12)
    ax.set_ylabel('Number of Jobs', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Show the plot
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def get_top_job_titles_with_plot(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], top_n=10):
    # حساب التكرارات
    top_titles = data['title'].value_counts().head(top_n)

    # تحويل البيانات لإطار بيانات مناسب لـ Seaborn
    plot_data = top_titles.reset_index()
    plot_data.columns = ['job_title', 'count']

    # رسم المخطط باستخدام Seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=plot_data, y='job_title', x='count', palette='magma')
    ax.set_title(f"Top {top_n} Most Frequent Job Titles")
    ax.set_xlabel("Number of Occurrences")
    ax.set_ylabel("Job Title")
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def analyze_jobs_by_work_type(data, plot_name, folder: Literal['egypt', 'saudi', 'compare']):
    if 'remote' not in data.columns:
        raise ValueError("The 'remote' column is missing from the data")

    # Count jobs by work type
    work_type_counts = data['remote'].value_counts()
    total = work_type_counts.sum()

    # Create DataFrame with percentage
    work_df = work_type_counts.reset_index()
    work_df.columns = ['Work Type', 'Count']
    work_df['Percentage'] = (work_df['Count'] / total * 100).round(1)

    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.pie(work_df['Count'], labels=work_df['Work Type'], autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('muted'))

    # Add title
    ax.set_title('Job Distribution by Work Type', fontsize=16)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig




def analyze_jobs_by_time(data, plot_name, folder: Literal['egypt', 'saudi', 'compare']):
    if 'date' not in data.columns:
        raise ValueError("The 'date' column is missing from the data")

    # Convert 'date' to datetime format if it's not already
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Extract the month from the 'date' column
    data['month'] = data['date'].dt.month

    # Count the number of jobs for each month
    month_counts = data['month'].value_counts()

    # Sort months by job count descending
    month_counts = month_counts.sort_values(ascending=False)

    # Convert index to string for better x-axis labels (optional)
    month_counts.index = month_counts.index.astype(str)

    # ترتيب شهور العرض يدوياً حسب القيم
    ordered_months = month_counts.index.tolist()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=month_counts.index, y=month_counts.values, palette="Blues", order=ordered_months)

    # Add numbers on top
    for i, value in enumerate(month_counts.values):
        plt.text(i, value + 10, str(value), ha='center', fontsize=12, color='black')

    ax.set_title('Job Distribution by Month', fontsize=16)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of Jobs', fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def analyze_jobs_by_gender(data, plot_name, folder: Literal['egypt', 'saudi', 'compare']):
    if 'gender' not in data.columns:
        raise ValueError("The 'gender' column is missing from the data")

    # Count the number of jobs for each gender
    gender_counts = data['gender'].value_counts()

    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=gender_counts.index, y=gender_counts.values, palette='Set2')

    # Add count labels on top of the bars
    for i, count in enumerate(gender_counts.values):
        plt.text(i, count + 0.5, f'{count}', ha='center', fontsize=12, color='black')

    # Titles and labels
    ax.set_title('Job Distribution by Gender', fontsize=16)
    ax.set_xlabel('Gender', fontsize=12)
    ax.set_ylabel('Number of Jobs', fontsize=12)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def analyze_jobs_by_job_level(data, plot_name, folder: Literal['egypt', 'saudi', 'compare']):
    if 'job_level' not in data.columns:
        raise ValueError("The 'job_level' column is missing from the data")

    # Count the number of jobs for each job level
    job_level_counts = data['job_level'].value_counts()

    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=job_level_counts.index, y=job_level_counts.values, palette='Set2')

    # Add count labels on top of the bars
    for i, count in enumerate(job_level_counts.values):
        plt.text(i, count + 0.5, f'{count}', ha='center', fontsize=12, color='black')

    # Titles and labels
    ax.set_title('Job Distribution by Job Level', fontsize=16)
    ax.set_xlabel('Job Level', fontsize=12)
    ax.set_ylabel('Number of Jobs', fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def plot_job_trend_over_time(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], freq='M'):
    df = data.copy()

    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Drop missing dates
    df = df.dropna(subset=['date'])

    # Set the date column as index
    df.set_index('date', inplace=True)

    # Resample and count entries
    job_counts = df.resample(freq).size()

    # Ensure chronological order
    job_counts = job_counts.sort_index()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    job_counts.plot(marker='o', linestyle='-')
    ax.set_title(f'Number of Job Entries Over Time ({freq}-level)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Jobs')
    # Removed grid lines
    # plt.grid(True)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig



def plot_monthly_job_boxplot(data, plot_name, folder: Literal['egypt', 'saudi', 'compare']):
    df = data.copy()
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # Extract month from date
    df['month'] = df['date'].dt.month

    # Count jobs per day (or any lower-level granularity), grouped by month
    daily_counts = df.groupby(['month', df['date'].dt.date]).size().reset_index(name='count')

    # Prepare boxplot data
    boxplot_data = [daily_counts[daily_counts['month'] == m]['count'] for m in range(1, 13)]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.boxplot(boxplot_data, labels=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ])
    ax.set_title('Distribution of Job Entries by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Jobs per Day')
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig
