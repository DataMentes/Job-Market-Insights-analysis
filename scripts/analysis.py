import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
from typing import Literal

sns.set(style="whitegrid")


def job_distribution_by_city(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True, top_n=10):
    """
    Plot and save a bar chart showing the distribution of jobs by city.

    This function generates a bar plot for the top N cities with the highest number
    of job postings. It supports proper display of Arabic text using arabic_reshaper
    and bidi.algorithm libraries.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing job data with at least one 'city' column.

    plot_name : str
        Name of the output image file (without extension).


    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    top_n : int, optional, default=10
        Number of top cities to include in the plot.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Notes:
    ------
    - Expects columns: 'city'
    - Requires importing:
        from bidi.algorithm import get_display
        import arabic_reshaper
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def analyze_jobs_by_company(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True, top_n=20):
    """
    Analyze and visualize the number of job postings per company.

    This function generates a bar chart showing the top N companies with the highest
    number of job postings. It supports saving the generated plot to a specified directory.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'company_name' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    top_n : int, optional, default=20
        Number of top companies to include in the plot.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    ValueError:
        If the 'company_name' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'company_name'
    - Recommended for datasets where company names are consistently formatted.
    """
    # Check if the 'company' column exists in the data
    if 'company_name' not in data.columns:
        raise ValueError("The 'company' column is missing from the data")

    # Count the number of jobs for each company
    company_counts = data['company_name'].value_counts().head(top_n)
    # Reshape Arabic text for proper display
    company_counts.index = [
        get_display(arabic_reshaper.reshape(company)) for company in company_counts.index
    ]
    # Plotting the bar chart inside the function
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=company_counts.index, y=company_counts.values, palette='viridis')

    # Adding titles and labels
    ax.set_title('Number of Jobs by Company', fontsize=16)
    ax.set_xlabel('Company Name', fontsize=12)
    ax.set_ylabel('Number of Jobs', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    # Show the plot
    plt.show()

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def get_top_job_titles_with_plot(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True, top_n=10):
    """
    Generate and visualize the top most frequent job titles from the dataset.

    This function calculates the top N most common job titles and creates a horizontal bar chart
    to display their frequency. The plot is then saved in the specified directory.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'title' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    top_n : int, optional, default=10
        Number of top job titles to include in the analysis and plot.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further customization or display.

    Raises:
    -------
    KeyError:
        If the 'title' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'title'
    - Uses Seaborn for plotting with a horizontal bar layout for better readability of job titles.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def analyze_jobs_by_work_type(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Analyze and visualize the distribution of jobs by work type (e.g., Remote, On-site).

    This function generates a pie chart showing the percentage distribution of job postings
    based on the work type (e.g., remote or on-site). It also returns the figure object
    and saves the plot to the specified directory.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'remote' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    ValueError:
        If the 'remote' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'remote'
    - Assumes that the 'remote' column contains categorical values indicating work type.
    - Uses a muted color palette from seaborn for better visual clarity.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def analyze_jobs_by_gender(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
    """
    Analyze and visualize the distribution of job postings by gender preference.

    This function generates a bar chart showing the number of job postings that specify
    each gender preference (e.g., Male, Female, Unspecified). It includes value labels
    on top of each bar for clarity and saves the plot to the specified directory.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'gender' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    ValueError:
        If the 'gender' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'gender'
    - Assumes the 'gender' column contains categorical values indicating gender preferences.
    - Value labels are added on top of bars for better readability.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def analyze_jobs_by_job_level(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Analyze and visualize the distribution of job postings by job level.

    This function generates a bar chart showing the number of job postings for each job level
    (e.g., Entry Level, Mid-Level, Senior, etc.). Value labels are added on top of each bar
    for better readability. The plot is saved to the specified directory.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'job_level' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    ValueError:
        If the 'job_level' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'job_level'
    - Assumes the 'job_level' column contains categorical values indicating job experience levels.
    - X-axis labels are rotated for better visibility when category names are long.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def plot_job_trend_over_time(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True, freq='M'):
    """
    Plot the trend of job postings over time with a specified frequency (e.g., monthly or daily).

    This function analyzes the temporal distribution of job postings by resampling the data
    based on a specified time frequency (e.g., 'M' for monthly, 'D' for daily), and generates
    a line plot showing the number of jobs over time. The resulting figure is saved to disk.

    Parameters:
    -----------
    data : pd.DataFrame
        Input DataFrame containing job data with at least one 'date' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    freq : str, optional, default='M'
        Resampling frequency for time series analysis. Common values include:
        - 'M' for month-end frequency
        - 'W' for weekly
        - 'D' for daily

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    ValueError:
        If the 'date' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'date'
    - Dates are coerced into valid datetime format; invalid dates are dropped.
    - The plot shows trends using markers and lines for better visual interpretation.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def plot_job_postings_by_industry(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Plot the top 10 industries by number of job postings with support for Arabic text display.

    This function generates a bar chart showing the top 10 industries with the highest number
    of job postings. It supports proper rendering of Arabic text using the arabic_reshaper and
    bidi.algorithm libraries.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing job data with at least one 'industry_' column.

    plot_name : str
        Name of the output image file (without extension).

    folder : Literal['egypt', 'saudi', 'compare']
        Folder name where the plot will be saved.

    save : bool
        Whether to save the output image file (default True).

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated figure object for further use or customization.

    Raises:
    -------
    KeyError:
        If the 'industry_' column is not present in the input DataFrame.

    Notes:
    ------
    - Expects columns: 'industry_'
    - Arabic text is reshaped using arabic_reshaper and get_display for correct display in plots.
    - Value labels are added on top of each bar for clarity.
    - Axis labels and title are displayed in Arabic to match the data context.
    """
    # Prepare data
    top_industries = df['industry_'].value_counts().head(10)
    top_industries = top_industries.reset_index()
    top_industries.columns = ['Industry', 'Number of Jobs']

    # Reshape Arabic text for proper display
    reshaped_industries = [
        get_display(arabic_reshaper.reshape(industry)) for industry in top_industries['Industry']
    ]

    # Plot
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(reshaped_industries, top_industries['Number of Jobs'], color='skyblue')

    # Add value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f'{int(height)}',
            ha='center',
            fontsize=10
        )

    # Formatting with Arabic text
    ax.set_title(get_display(arabic_reshaper.reshape('The highest 10 areas declared for business opportunities')),
                 fontsize=16)
    ax.set_xlabel(get_display(arabic_reshaper.reshape('Domain')), fontsize=14)
    ax.set_ylabel(get_display(arabic_reshaper.reshape('Number of jobs')), fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')

    plt.tight_layout()
    plt.show()

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def analyze_job_type_distribution(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Analyze the distribution of job types and plot a pie chart with a clean legend.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing a 'type' column representing the job type.
    plot_name : str
        The name of the file to save the plot to.
    folder : Literal['egypt', 'saudi', 'compare']
        The subfolder to save the plot in.
    save : bool, optional
        Whether to save the plot to a file. Defaults to True.

    Returns:
    --------
    matplotlib.figure.Figure
        The generated Figure object.
    """
    type_counts = data['type'].value_counts()
    total = type_counts.sum()
    raw_labels = type_counts.index.tolist()
    sizes = type_counts.values
    percentages = [f"{(count / total) * 100:.2f}%" for count in sizes]  # Reduced to 2 decimal places for clarity

    # Labels in legend: JobName (xx.xx%)
    labels_with_pct = [f"{name} ({pct})" for name, pct in zip(raw_labels, percentages)]

    colors = sns.color_palette('pastel', len(labels_with_pct))

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts = ax.pie(
        sizes,
        colors=colors,
        startangle=140,
    )

    # Show legend with name + percentage
    ax.legend(wedges, labels_with_pct, title="Job Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title('Job Distribution by Type', fontsize=14)
    plt.tight_layout()
    plt.show()

    if save:
        path = f'../visualizations/{folder}/{plot_name}.png'
        fig.savefig(path, bbox_inches='tight')

    return fig

def compare_experience_requirements(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Compare minimum and maximum experience requirements for jobs.

    This function generates a boxplot to compare the minimum and maximum years of experience
    required for the jobs in the provided dataset.  It cleans the data by removing
    missing and non-numeric values before plotting.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing 'min_num_of_years' and 'max_num_of_years' columns.
    plot_name : str
        The name of the file to save the plot to.
    folder : Literal['egypt', 'saudi', 'compare']
        The subfolder to save the plot in.  Must be one of 'egypt', 'saudi', or 'compare'.
    save : bool, optional
        Whether to save the plot to a file.  Defaults to True.

    Returns:
    --------
    matplotlib.figure.Figure
        The generated Figure object.
    """
    exp_df = data[['min_num_of_years', 'max_num_of_years']].copy()
    exp_df = exp_df.dropna()
    exp_df = exp_df[(exp_df['min_num_of_years'] != 'Unknown') & (exp_df['max_num_of_years'] != 'Unknown')]

    exp_df['min_num_of_years'] = pd.to_numeric(exp_df['min_num_of_years'], errors='coerce')
    exp_df['max_num_of_years'] = pd.to_numeric(exp_df['max_num_of_years'], errors='coerce')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=exp_df, palette='Set3')
    ax.set_title('Comparison of Min & Max Experience Requirements', fontsize=16)
    ax.set_ylabel('Years of Experience', fontsize=12)
    plt.tight_layout()
    plt.show()

    if save:
        path = f'../visualizations/{folder}/{plot_name}.png'
        fig.savefig(path)

    return fig


def jobs_heatmap_by_city_and_job_level(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save=True):
    """
    Create a heatmap of job counts by city and job type.

    This function generates a heatmap showing the number of available jobs in each city
    for each job type present in the dataset.

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing 'city' and 'type' columns.
    plot_name : str
        The name of the file to save the plot to.
    folder : Literal['egypt', 'saudi', 'compare']
        The subfolder to save the plot in.  Must be one of 'egypt', 'saudi', or 'compare'.
    save : bool, optional
        Whether to save the plot to a file.  Defaults to True.

    Returns:
    --------
    matplotlib.figure.Figure
        The generated Figure object.
    """
    pivot_table = pd.pivot_table(data, index='city', columns='job_level', aggfunc='size', fill_value=0)

    # Convert index and columns to Arabic for display
    reshaped_index = [get_display(arabic_reshaper.reshape(city)) for city in pivot_table.index]
    reshaped_columns = [get_display(arabic_reshaper.reshape(job_type)) for job_type in pivot_table.columns]

    pivot_table.index = reshaped_index
    pivot_table.columns = reshaped_columns

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='d')
    plt.xticks(rotation=-45)
    ax.set_title('Heatmap of Job Count by City and job level')
    plt.tight_layout()
    plt.show()

    if save:
        path = f'../visualizations/{folder}/{plot_name}.png'
        fig.savefig(path)

    return fig


def plot_top_job_titles_wordcloud(data, stopwords_list=[], save=False, plot_name='wordcloud', folder='egypt'):
    """
    Generate a word cloud of the most common job titles.

    This function creates a visual representation (word cloud) of the most frequent job titles
    in the dataset.  You can customize the words to exclude (stopwords).

    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame containing a 'title' column representing the job title.
    stopwords_list : list, optional
        List of words to exclude from the word cloud.  Defaults to an empty list.
    save : bool, optional
        Whether to save the plot to a file.  Defaults to False.
    plot_name : str, optional
        The name of the file to save the plot to.  Defaults to 'wordcloud'.
    folder : str, optional
        The subfolder to save the plot in.  Defaults to 'egypt'.

    Returns:
    --------
    matplotlib.figure.Figure
        The generated Figure object.
    """
    from wordcloud import WordCloud

    text = ' '.join(data['title'].dropna())
    wordcloud = WordCloud(width=1000, height=600, background_color='white',
                          stopwords=set(stopwords_list), colormap='viridis').generate(text)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Most Common Job Titles (Wordcloud)', fontsize=16)
    plt.tight_layout()
    plt.show()

    if save:
        path = f"../visualizations/{folder}/{plot_name}.png"
        fig.savefig(path)

    return fig
