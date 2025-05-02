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

# %%
titles_df['title'].value_counts().head(10)


# %%
df.loc[:, 'remote']=df['remote'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))
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

# %%
titles_df['title'].value_counts().head(10).plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=90,
    title='Top 10 Job Titles Distribution'
)
plt.ylabel('')
plt.show()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.

# %%
df['remote'].value_counts().plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=180,
    title='Remote Work Distribution'
)
plt.ylabel('')  # Remove the y-axis label for better aesthetics
plt.show()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.

# %%
plt.figure(figsize=(14, 8))
df['industry_'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Industries by Number of Job Postings', fontsize=16)
plt.xlabel('Industry', fontsize=14)
plt.ylabel('Number of Job Postings', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.show()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.

# %%
df['gender'].value_counts().plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=180,
)


# %%
grouped_df = df.groupby(['city', 'industry_'])['title'].count().reset_index()

# %% [markdown]
# ### Explanation
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.

# %%
plt.figure(figsize=(14, 8))
grouped_df.groupby('city')['title'].sum().sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Cities by Number of Job Titles', fontsize=16)
plt.xlabel('City', fontsize=14)
plt.ylabel('Number of Job Titles', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.show()

# %% [markdown]
# ### Explanation
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Line Plot
# 
# This code produces a line plot, ideal for showing trends over time or ordered categories.

# %%
# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Group by date and count the number of job postings
date_counts = df.groupby('date').size()

# Plot the data
plt.figure(figsize=(14, 8))
date_counts.plot(kind='line', color='blue', marker='o')
plt.title('Job Postings Over Time', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Job Postings', fontsize=14)
plt.grid(True)
plt.show()


# %%
unique_types_count = df['type'].nunique()


# %%
unique_types_count

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Data Visualization
# 
# This code creates a visualization to help interpret the data. Visualization is key to discovering patterns, outliers, and trends.

# %%
# Create an explode list with the same length as the unique job types
explode = [0.1] * unique_types_count

# Plot the pie chart
df['type'].value_counts().plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=180,
    explode=explode,
    title='Job Type Distribution',
    textprops={'fontsize': 9},
    legend=True,
)

plt.ylabel('')  # Remove the y-axis label for better aesthetics
plt.show()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.

# %%
#distribution of job level 
plt.figure(figsize=(14, 8))
df['job_level'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Job Level Distribution', fontsize=16)
plt.xlabel('Job Level', fontsize=14)
plt.ylabel('Number of Job Postings', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.show()

# %% [markdown]
# ### Explanation
# This code summarizes the frequency of values in a column, which is useful for understanding the distribution of categorical data.
# This code generates a plot to visualize data, aiding in analysis and communication of trends.
# %% [markdown]
# ### Bar Plot Visualization
# 
# This code generates a bar chart to visualize the count of items (e.g., job postings per company). Bar plots are excellent for comparing categorical data.

# %%
# Prepare data
top_companies = df['company_name'].value_counts().head(10).sort_values()

# Plot
plt.figure(figsize=(14, 8))
sns.barplot(x=top_companies.values, y=top_companies.index, palette='mako')

# Titles and labels
plt.title('Top 10 Industries by Number of Job Postings', fontsize=18)
plt.xlabel('Number of Job Postings', fontsize=14)
plt.ylabel('Company Name', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()

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

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
top_companies = df['company_name'].value_counts().head(10).sort_values()

# Plot
plt.figure(figsize=(14, 8))
sns.barplot(x=top_companies.values, y=top_companies.index, palette='mako')

# Titles and labels
plt.title('Top 10 Industries by Number of Job Postings', fontsize=18)
plt.xlabel('Number of Job Postings', fontsize=14)
plt.ylabel('Company Name', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()


