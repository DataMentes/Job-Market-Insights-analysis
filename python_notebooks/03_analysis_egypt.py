# %%
from scripts.analysis import *

# %% [markdown]
# ### Loading data from the SQLite database
# 
# In this cell:
# - A connection is created to the SQLite database file (`database.db`).
# - A SQL query is used to read all data from the table named `EGYPT` into a pandas DataFrame.
# 

# %%
conn = sqlite3.connect('../database.db')
df = pd.read_sql('SELECT * FROM EGYPT', conn)

# %% [markdown]
# ### Viewing the First Few Rows of the DataFrame
# 
# The `df.head()` function is used to display the first 5 rows of the DataFrame `df`

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
print(df['city'])

# %%
print(df['city'].unique())

# %%
print(df['city'].value_counts())


# %%
print(df['title'].value_counts())

# %%
# حذف الصفوف التي تحتوي على قيمة معينة في العمود
df = df[df['city'] != 'Unknown']

# %% [markdown]
# ## 🔹 Visualization 1: Top 10 Cities by Number of Jobs
# 
# ### 🔍 Description:
# A vertical bar chart displaying the number of job listings in the top 10 Egyptian cities.
# 
# ### 📌 Key Insights:
# 
# 1. **Cairo is the Undisputed Hub:**
#    - Cairo alone accounts for the vast majority of job postings (over 2,000).
#    - Reflects its status as the economic and business capital of Egypt.
# 
# 2. **Limited Opportunities in Other Cities:**
#    - Alexandria comes second, but with a significantly lower count (~100+).
#    - All other cities (like New Alamein, Sharm El Sheikh, Luxor, etc.) have minimal job postings.
#    - Suggests a high centralization of employment opportunities in the capital.
# 
# 3. **Implications:**
#    - Indicates potential internal migration toward Cairo for job seekers.
#    - May signal the need for investment in decentralizing job markets and regional development.
# 
# ### 💡 Overall Takeaway:
# > Cairo dominates the job market in Egypt, with a steep drop-off in job availability in other cities, highlighting urban centralization and regional imbalance in employment opportunities.

# %%
top_cities = job_distribution_by_city(df, top_n=10, plot=True)
print(top_cities)

# %% [markdown]
# ## 🔹 Visualization 2: Top 10 Most Frequent Job Titles
# 
# ### 🔍 Description:
# A horizontal bar chart showing the most commonly listed job titles in the dataset based on the number of occurrences.
# 
# ### 📌 Key Insights:
# 
# 1. **Strong Demand for Accounting Roles:**
#    - 5 of the top 10 job titles are finance/accounting-related:
#      - Accountant
#      - Senior Accountant
#      - Finance Manager
#      - Junior Accountant
#      - Chief Accountant
#    - Indicates a significant demand in the job market for financial expertise.
# 
# 2. **Data and Analytics Roles Are Rising:**
#    - Positions like Senior Business Analyst and Data Engineer appear in the top 10.
#    - Shows increasing importance of data-driven decision-making.
# 
# 3. **Support and Creative Roles Are Present:**
#    - Executive Assistant and Graphic Designer made the list.
#    - Suggests administrative and creative skills are still needed, though in smaller volumes.
# 
# ### 💡 Overall Takeaway:
# > The job market is currently dominated by finance-related positions, with a growing interest in data and analytics, and a continuing (but smaller) need for creative and support roles.

# %%
analyze_jobs_by_company(df)

# %% [markdown]
# ## 🔹 Visualization 3: Number of Jobs by Company
# 
# ### 🔍 Description:
# A vertical bar chart illustrating how many job postings come from each company.
# 
# ### 📌 Key Insights:
# 
# 1. **Talent 360 Dominates the Market:**
#    - Over 250 job postings — far ahead of any other company.
#    - Likely a recruitment firm or aggregator serving multiple clients.
# 
# 2. **High Activity from Tech and Telecom Firms:**
#    - Notable companies include Vodafone Egypt, Giza Systems, Orange, and Accenture.
#    - Reflects strong demand for digital and telecom roles.
# 
# 3. **Diverse but Uneven Sector Representation:**
#    - Other sectors also visible:
#      - Real Estate: Palm Hills, Arabia Group
#      - Tourism: Grand Rotana Resort
#      - Industrial: Siemens, Schneider Electric
#    - Shows a variety of industries are hiring, but the majority of roles are concentrated in tech and recruitment.
# 
# ### 💡 Overall Takeaway:
# > Tech and staffing companies are leading job providers, while other sectors like real estate, tourism, and manufacturing contribute modestly to the hiring landscape.

# %%
get_top_job_titles_with_plot(df)

# %% [markdown]
# ## 🔹 Visualization 4: Job Distribution by Work Type
# 
# ### 🔍 Description:
# A pie chart showing the percentage distribution of jobs based on their work format (On-site, Remote, Hybrid).
# 
# ### 📌 Key Insights:
# 
# 1. **Overwhelming Majority are On-site Jobs:**
#    - 88.6% of listings are for on-site positions.
#    - Implies that traditional office presence is still dominant in Egypt.
# 
# 2. **Remote and Hybrid Work Are Very Limited:**
#    - Only 7.4% remote and 4.0% hybrid roles.
#    - Indicates slow adoption of flexible work models.
# 
# 3. **Implications:**
#    - May be due to lack of infrastructure, cultural preferences, or the nature of jobs requiring physical presence.
#    - A gap exists compared to global trends favoring hybrid and remote work, especially post-COVID.
# 
# ### 💡 Overall Takeaway:
# > The job market in Egypt is still heavily reliant on on-site roles, with minimal adoption of remote or hybrid work formats, highlighting a lag in workplace flexibility.

# %%
analyze_jobs_by_work_type(df)

# %% [markdown]
# ## 🔹 Visualization 5: Job Distribution by Month
# 
# ### 📌 Key Insights:
# 
# .April (Month 4) and March (Month 3) show the highest number of job postings, with 839 and 738 jobs respectively.
# 
# .There is a sharp decline after March, with February (403 jobs) and January (228 jobs) showing significantly lower counts.
# 
# .The last three months (December, November) show very low activity, especially November with only 23 job postings.
# 
# ### 💡 Overall Takeaway:
# - Hiring peaks in March and April, indicating a strong seasonal hiring trend during spring. Planning job campaigns or applications in these months could yield better results.

# %%
top_5_months, month_counts = analyze_jobs_by_time(df)

# %% [markdown]
# ## 🔹 Visualization 6: Job Distribution by Month
# 
# ### 📌 Key Insights:
# 
# - A dominant majority (2253 jobs) have no gender preference.
# - Female-targeted roles are 97, while male-targeted roles are just 55.
# 
# ### 💡 Overall Takeaway:
# - The job market is largely gender-neutral in job listings, which may reflect a trend toward inclusivity or a focus on qualifications over demographics

# %%
analyze_jobs_by_gender(df)

# %% [markdown]
# ## 📊  visualization 7 :Job Level Distribution Analysis
# 
# ### 📌 Key Insights:
# 
# **"No Preference" Dominates**  
#   - 1,312 job postings have no specified job level.  
#   - This may indicate flexibility in hiring or a lack of clarity in role definitions.
# 
# - **Strong Demand for Experienced Talent**  
#   - Senior-level: 544 jobs  
#   - Management: 409 jobs  
#   - These figures highlight a clear demand for experienced and leadership-level professionals.
# 
# - **Limited Entry-Level Opportunities**  
#   - Junior: 54  
#   - Graduate: 27  
#   - Mid Level: 21  
#   - Opportunities for early-career candidates are noticeably fewer.
# 
# - **Minimal Executive-Level Roles**  
#   - C-Suite positions: 2  
#   - These roles are naturally scarce due to their seniority and selectiveness.
# 
# ### 💡 Overall Takeaway:
# - The job market is heavily skewed toward senior and management-level positions, with a surprising number of listings having no specified level. This may reflect a broad hiring strategy or incomplete data entry. Entry-level and executive roles are limited, indicating that companies are prioritizing experienced professionals over new graduates or top-tier executives.

# %%
job_level_counts = analyze_jobs_by_job_level(df)

# %% [markdown]
# ## 📈 Visualization 8 : M-Level Job Entries Over Time
# 
# This line chart tracks the number of job postings for **Management-level (M-level)** roles from **November 2024 to April 2025**.
# 
# ### ✅ Key Insights
# 
# - **Consistent Growth**:  
#   The number of M-level job postings increased steadily each month, showing sustained demand.
# 
# - **Sharp Growth Between Feb–Mar 2025**:  
#   - February: ~400 jobs  
#   - March: ~740 jobs  
#   - This marks the most significant month-over-month growth.
# 
# - **Early Acceleration (Nov–Jan)**:  
#   - Job entries started at a low point (~30 in Nov) and grew gradually through Jan (~230), indicating the early stages of hiring momentum.
# 
# - **Stabilization in April**:  
#   - April saw continued growth (~840 jobs), but at a slower rate compared to the March surge.
# 
# 
# ### 🧾 Overall Takeaway
# 
# The hiring trend for management-level roles has shown strong upward momentum over the past six months, particularly peaking in early 2025. This suggests increasing organizational needs for mid-to-senior management talent, likely driven by business expansion or restructuring initiatives.
# 
# 

# %%
plot_job_trend_over_time(df)

# %% [markdown]
# ## 📊 Visualization 9: Distribution of Job Entries by Month
# 
# This boxplot illustrates the **daily distribution of job entries** for each month, highlighting variability, medians, and outliers across time.
# 
# ### ✅ Key Insights
# 
# - **Clear Upward Trend (Jan–Apr)**:
#   - Each month from January to April shows an **increase in the median** number of jobs posted per day.
#   - The interquartile range (IQR) also widens, indicating **greater day-to-day variability** in job postings.
# 
# - **April Stands Out**:
#   - April has the **widest spread** of data and the **highest number of outliers**, including some days with more than **200 jobs posted**.
#   - This suggests a **surge in recruitment activity** or possibly batch job uploads.
# 
# - **Consistent Low Activity (Nov–Dec)**:
#   - Very low median values and tight boxplots indicate **minimal hiring activity** during these months, possibly due to year-end slowdowns.
# 
# - **Outliers as Activity Spikes**:
#   - Multiple months exhibit high outliers, particularly March and April, reflecting **short bursts of high hiring days**.
# 
# ---
# 
# ### 🧾 Overall Takeaway
# 
# - The data reveals a **seasonal hiring pattern**, with job entry volumes **peaking sharply in April** and remaining low in the final months of the year. This suggests that companies significantly ramp up hiring in Q1 and Q2, with April being a strategic month for recruitment efforts.
# 
# 

# %%
plot_monthly_job_boxplot(df)

# %%



