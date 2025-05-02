# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
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


# %%
titles_df['title'].value_counts().head(10)


# %%
df.loc[:, 'remote']=df['remote'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))
df.loc[:, 'industry_']=df['industry_'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))
df.loc[:, 'city']=df['city'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))


# %%
df[df['city']=='الرياض'].count()


# %%
titles_df['title'].value_counts().head(10).plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=90,
    title='Top 10 Job Titles Distribution'
)

plt.show()


# %%
df['remote'].value_counts().plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=180,
    title='Remote Work Distribution'
)
plt.ylabel('')  # Remove the y-axis label for better aesthetics
plt.show()


# %%
plt.figure(figsize=(14, 8))
df['industry_'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Industries by Number of Job Postings', fontsize=16)
plt.xlabel('Industry', fontsize=14)
plt.ylabel('Number of Job Postings', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.show()


# %%
df['gender'].value_counts().plot.pie(
    figsize=(8, 8),
    autopct='%1.1f%%',
    startangle=180,
)


# %%
grouped_df = df.groupby(['city', 'industry_'])['title'].count().reset_index()


# %%
plt.figure(figsize=(14, 8))
grouped_df.groupby('city')['title'].sum().sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Cities by Number of Job Titles', fontsize=16)
plt.xlabel('City', fontsize=14)
plt.ylabel('Number of Job Titles', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.show()


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


# %%



