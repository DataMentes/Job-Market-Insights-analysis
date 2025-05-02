# %% [markdown]
# ### Importing the necessary libraries for data analysis and visualization
# 
# In this cell, we import:
# - `sqlite3`: to interact with SQLite databases.
# - `pandas`: for data manipulation and analysis.
# - `matplotlib.pyplot` and `seaborn`: for creating visualizations.
# - `arabic_reshaper` and `bidi.algorithm`: to correctly display Arabic text in visualizations.
# 

# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
from typing import Literal


# %% [markdown]
# ### Function to analyze job distribution by city
# 
# This function, `job_distribution_by_city`, takes a DataFrame and returns the top `n` cities with the highest number of job postings.
# 
# - `df`: The input DataFrame containing job data.
# - `top_n`: The number of top cities to return (default is 10).
# - `plot`: If `True`, the function will generate a bar chart showing the number of jobs per city.
# 
# If plotting is enabled:
# - Arabic text is reshaped and displayed correctly using `arabic_reshaper` and `bidi.algorithm`.
# - A bar chart is displayed showing the top `n` cities by job count with properly rendered Arabic labels.
# 
# The function returns a DataFrame with two columns: `City` and `Number of Jobs`.
# 

# %%

def job_distribution_by_city(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], top_n=10):
    job_counts = df['city'].value_counts().reset_index()
    job_counts.columns = ['City', 'Number of Jobs']
    top_cities = job_counts.head(top_n)

    fig = None
    # Prepare Arabic text
    reshaped_labels = [get_display(arabic_reshaper.reshape(city)) for city in top_cities['City']]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(reshaped_labels, top_cities['Number of Jobs'], color='#20B2AA')
    ax.set_xticks(rotation=45, ha='right', fontsize=12)
    ax.set_ylabel(get_display(arabic_reshaper.reshape('Number of Jobs')), fontsize=13)
    ax.set_title(get_display(arabic_reshaper.reshape(f'Top {top_n} Cities by Number of Jobs')), fontsize=14)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig


# %% [markdown]
# ### Function to analyze the number of job postings by company
# 
# This function, `analyze_jobs_by_company`, visualizes the top n companies with the highest number of job postings.
# 
# - It first checks if the `company_name` column exists in the DataFrame.
# - Then, it counts the number of job listings for each company and selects the top n (default is 20).
# - A bar chart is generated using Seaborn to visualize the job distribution across these companies.
# 
# The chart includes:
# - Company names on the x-axis.
# - Number of job postings on the y-axis.
# - A title and labeled axes for clarity.
# 
# This function does not return anything; it directly shows the plot.
# 

# %%
# Function to analyze jobs by company with visualization
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


# %% [markdown]
# ### Function to Get and Visualize Top Job Titles
# 
# The `get_top_job_titles_with_plot` function identifies and visualizes the most frequent job titles in the dataset.
# 
# **Key Steps:**
# - It cleans the job titles by:
#   - Removing extra spaces.
#   - Converting all text to lowercase for consistency.
# - It then calculates the frequency of each job title.
# - The top `n` most frequent titles are selected (default is 10).
# - A horizontal bar chart is generated using Seaborn to show the top job titles and how many times they appear.
# 
# **Returns:**
# - A pandas Series containing the top job titles and their counts.

# %%
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


# %% [markdown]
# ### Function to analyze job distribution by work type (remote vs on-site)
# 
# The `analyze_jobs_by_work_type` function visualizes how jobs are distributed based on their work type.
# 
# - It first checks whether the `'remote'` column exists in the DataFrame.
# - Then, it calculates the number of jobs by each work type (e.g., Remote, On-site, Hybrid).
# - It creates a new DataFrame that includes both the count and the percentage of each work type.
# 
# A pie chart is generated showing:
# - Each work type as a slice.
# - The percentage of total jobs in each category.
# - A title for the chart.
# 
# The function returns a DataFrame containing:
# - `Work Type`: The type of work (from the `remote` column).
# - `Count`: Number of job postings for that type.
# - `Percentage`: Share of that type as a percentage of total jobs.
# 

# %%
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


# %% [markdown]
# ### Function to analyze job distribution by month (with top 5 months)
# 
# The `analyze_jobs_by_time` function visualizes the distribution of job postings across months and returns the top 5 months with the highest number of jobs.
# 
# Steps:
# 1. **Date Validation**: The function first checks if the `date` column exists in the DataFrame.
# 2. **Date Conversion**: The `date` column is converted to datetime format if it is not already.
# 3. **Month Extraction**: It extracts the month from the `date` column and creates a new column for the month.
# 4. **Counting Jobs by Month**: The function counts the number of jobs for each month.
# 5. **Sorting and Formatting**: The months are sorted by job count in descending order, and their labels are formatted for better presentation.
# 6. **Plotting**: A bar chart is displayed, showing the number of jobs for each month, with the numbers shown above the bars.
# 
# The function also returns:
# - The **top 5 months** with the highest job postings.
# - The full count of jobs per month for further analysis.
# 
# The output will look like:
# - `month_counts.head(5)`: Top 5 months with the highest number of jobs.
# - `month_counts`: All months with the corresponding job counts.
# 

# %%

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
    ax.set_xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig


# %% [markdown]
# ### Function to analyze job distribution by gender
# 
# The `analyze_jobs_by_gender` function visualizes how job postings are distributed between different genders.
# 
# - It first checks whether the `'gender'` column exists in the dataset.
# - The function counts the number of job postings for each gender category.
# - A bar chart is generated to visualize the job distribution.
# 
# The chart includes:
# - Gender categories on the x-axis (e.g., Male, Female, Other).
# - The number of job postings on the y-axis.
# - The number of job postings displayed on top of each bar.
# 
# The function returns a `gender_counts` Series, which contains the count of job postings for each gender.
# 


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


# %% [markdown]
# ### Function to analyze job distribution by job level
# 
# The `analyze_jobs_by_job_level` function visualizes how job postings are distributed across different job levels.
# 
# - It first checks whether the `'job_level'` column exists in the dataset.
# - The function counts the number of job postings for each job level.
# - A bar chart is generated to show the distribution of job postings across the various job levels.
# 
# The chart includes:
# - Job levels on the x-axis (e.g., Entry, Mid-level, Senior, etc.).
# - The number of job postings on the y-axis.
# - The count of job postings is displayed above each bar.
# 
# The function returns a `job_level_counts` Series, containing the number of job postings for each job level.
# 


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
    ax.set_xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    path = '../visualizations/' + folder + '/' + plot_name + '.png'
    fig.savefig(path)

    return fig


# %% [markdown]
# ### 📈 Job Trend Over Time
# 
# This function visualizes the trend of job postings over time by resampling the data at a chosen frequency (daily, monthly, or yearly). It helps in understanding how the job market fluctuates across different time periods. The chart uses a line plot with time on the x-axis and the number of job postings on the y-axis.

# %%

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
