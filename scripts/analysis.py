import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
from typing import Literal




def job_distribution_by_city(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True, top_n=10):
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



def analyze_jobs_by_company(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True, top_n=20):
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



def get_top_job_titles_with_plot(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True, top_n=10):
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



def analyze_jobs_by_work_type(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
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




def analyze_jobs_by_time(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
    """
    Analyze and visualize the distribution of job postings over time (by month).

    This function processes a date column to extract monthly trends in job postings,
    then generates a bar chart showing the number of jobs per month. The months are
    sorted based on the number of jobs in descending order for better visualization.

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
    - Converts the 'date' column to datetime format and extracts the month.
    - Assumes dates are valid or can be coerced using errors='coerce'.
    - Months in the plot are ordered by job count (not chronological) for emphasis on peak hiring months.
    """
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



def analyze_jobs_by_job_level(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
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


def plot_job_trend_over_time(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True, freq='M'):
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



def plot_monthly_job_boxplot(data, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
    """
    Generate a boxplot showing the daily distribution of job entries by month.

    This function analyzes the variability of daily job posting counts across months,
    and visualizes the distribution using a boxplot. It shows medians, quartiles,
    and potential outliers for each month, providing insights into seasonal patterns.

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
    - Daily job counts are grouped by month to create the boxplot structure.
    - The x-axis uses abbreviated month names (Jan, Feb, ..., Dec) for clarity.
    """
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

    if save:
        path = '../visualizations/' + folder + '/' + plot_name + '.png'
        fig.savefig(path)

    return fig


def plot_job_postings_by_industry(df, plot_name, folder: Literal['egypt', 'saudi', 'compare'], save = True):
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
    ax.set_title(get_display(arabic_reshaper.reshape('The highest 10 areas declared for business opportunities')), fontsize=16)
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