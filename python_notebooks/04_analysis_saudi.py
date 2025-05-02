# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Explanation
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.

# %%
from scripts.analysis import *
import plotly.express as px
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display


# %%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)


# %%
df.head()


# %%
df['title'].nunique()


# %%
df['title'].duplicated().sum()


# %%
titles_df=df[df['title'].duplicated()]


# %%
titles_df['title'].unique().view()


# %%
titles_df.info()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# %% [markdown]
# ### Value Counts Summary
# 
# This code computes the frequency of unique values in a column. It is commonly used to understand how data is distributed across categories (e.g., how many job postings each company has).
# %% [markdown]
# ### 📊 Distribution of Categorical Values
# 
# This code block computes the **frequency distribution** of values in a specific column. It's particularly useful for identifying the **most common categories**, such as top employers, cities, or job titles.
# 
# Key Insight:
# - This helps us **identify dominant categories** which could indicate market leaders or preferred locations.

# %%
titles_df['title'].value_counts().head(10)


# %%
df.loc[:, 'industry_']=df['industry_'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))
df.loc[:, 'city']=df['city'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))


# %%
df[df['city']=='الرياض'].count()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.
# %% [markdown]
# ### 📊 Distribution of Categorical Values
# 
# This code block computes the **frequency distribution** of values in a specific column. It's particularly useful for identifying the **most common categories**, such as top employers, cities, or job titles.
# 
# Key Insight:
# - This helps us **identify dominant categories** which could indicate market leaders or preferred locations.

# %%
new_df=df.drop(df[df['city']=='Unknown'].index)


# %%
get_top_job_titles_with_plot(df,'bar_JobTitles','saudi')

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.
# %% [markdown]
# ### 📊 Distribution of Categorical Values
# 
# This code block computes the **frequency distribution** of values in a specific column. It's particularly useful for identifying the **most common categories**, such as top employers, cities, or job titles.
# 
# Key Insight:
# - This helps us **identify dominant categories** which could indicate market leaders or preferred locations.

# %%
analyze_jobs_by_work_type(df,'typeOfJob','saudi')

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.
# %% [markdown]
# ### 📈 Horizontal Bar Chart Visualization
# 
# This visualization presents the **top categories** (e.g., industries or companies) by their number of job postings using a **horizontal bar chart**.
# 
# Why it's useful:
# - Makes it easier to compare categories.
# - Highlights **which industries or companies dominate** the job market in this dataset.

# %%
plot_job_postings_by_industry(df,'bar_industry_saudi','saudi')

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.
# %% [markdown]
# ### 📊 Distribution of Categorical Values
# 
# This code block computes the **frequency distribution** of values in a specific column. It's particularly useful for identifying the **most common categories**, such as top employers, cities, or job titles.
# 
# Key Insight:
# - This helps us **identify dominant categories** which could indicate market leaders or preferred locations.

# %%
analyze_jobs_by_gender(df,'gendersInSa','saudi')

# %% [markdown]
# ### Explanation
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.
# %% [markdown]
# ### 📈 Horizontal Bar Chart Visualization
# 
# This visualization presents the **top categories** (e.g., industries or companies) by their number of job postings using a **horizontal bar chart**.
# 
# Why it's useful:
# - Makes it easier to compare categories.
# - Highlights **which industries or companies dominate** the job market in this dataset.

# %%
job_distribution_by_city(new_df,'bar_cities','saudi')

# %% [markdown]
# ### Explanation
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Line Plot
# 
# This code produces a line plot, ideal for showing trends over time or ordered categories.
# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.
# %% [markdown]
# ### 📊 Distribution of Categorical Values
# 
# This code block computes the **frequency distribution** of values in a specific column. It's particularly useful for identifying the **most common categories**, such as top employers, cities, or job titles.
# 
# Key Insight:
# - This helps us **identify dominant categories** which could indicate market leaders or preferred locations.

# %%


# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.
# %% [markdown]
# ### 📈 Horizontal Bar Chart Visualization
# 
# This visualization presents the **top categories** (e.g., industries or companies) by their number of job postings using a **horizontal bar chart**.
# 
# Why it's useful:
# - Makes it easier to compare categories.
# - Highlights **which industries or companies dominate** the job market in this dataset.

# %%
analyze_jobs_by_job_level(df,'job_by_level_sa','saudi')

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.
# %% [markdown]
# ### 📈 Horizontal Bar Chart Visualization
# 
# This visualization presents the **top categories** (e.g., industries or companies) by their number of job postings using a **horizontal bar chart**.
# 
# Why it's useful:
# - Makes it easier to compare categories.
# - Highlights **which industries or companies dominate** the job market in this dataset.
# %% [markdown]
# ## Top 10 Industries by Number of Job Postings
# 
# This section visualizes the top 10 industries (represented by company names) with the most job postings using a horizontal bar plot. Instead of using basic `matplotlib`, we use **Seaborn** for enhanced styling and better visual clarity.
# 
# ### Step-by-step:
# - **Step 1**: Count the number of job postings per company.
# - **Step 2**: Take the top 10 companies and sort them for horizontal alignment.
# - **Step 3**: Use `sns.barplot` to create a horizontal bar chart with a clean palette.
# - **Step 4**: Add labels, title, and styling for clarity.
# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.
# %% [markdown]
# ### 📈 Horizontal Bar Chart Visualization
# 
# This visualization presents the **top categories** (e.g., industries or companies) by their number of job postings using a **horizontal bar chart**.
# 
# Why it's useful:
# - Makes it easier to compare categories.
# - Highlights **which industries or companies dominate** the job market in this dataset.

# %%
analyze_jobs_by_company(df,'companies&jobs','saudi')


# %%
plot_job_trend_over_time(df, 'saudi_job_postings_over_time', 'saudi')


