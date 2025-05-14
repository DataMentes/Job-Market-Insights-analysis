#%% md
# ### Import required libraries
# - Import `all analysis functions` module from `scripts`.
# - Import `sqlite3` for database interaction.
# - Import `warnings` and disable warnings.
# - Import `pandas` for data manipulation.
#%%
from scripts.analysis import *
import sqlite3
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
#%% md
# # Analysis and Explanation of Plots
#%%
conn = sqlite3.connect('../data/database.db')
df_egy = pd.read_sql('SELECT * FROM EGYPT', conn)
df_saudi = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)
#%%
df_egy.head()
#%%
df_saudi.head()
#%%
df_egy['title'].nunique()
#%%
df_saudi['title'].nunique()
#%%
df_egy['city'].unique()
#%%
df_saudi['city'].unique()
#%%
df_egy['city'].value_counts().head()
#%%
df_saudi['city'].value_counts().head()
#%%
df_egy['title'].value_counts().head()
#%%
df_saudi['title'].value_counts().head()
#%% md
# ### **Comparison Between the Two Plots**
# #### **Similarities**
# 1. **Dominance of Capital Cities**:
#    - In both countries, the capital cities (Riyadh for Saudi Arabia and Cairo for Egypt) have the highest number of jobs, highlighting their central role in the economy.
# 2. **Skewed Distribution**:
#    - Both plots show a highly skewed distribution, where a few cities dominate job availability, while the majority have very low numbers.
# 3. **Economic Hubs**:
#    - Major economic hubs (e.g., Jeddah in Saudi Arabia and Alexandria in Egypt) offer significant job opportunities but are still far behind the capital cities.
# #### **Differences**
# 1. **Second-Largest City Job Availability**:
#    - In Saudi Arabia, Jeddah offers around 500 jobs, which is a substantial number.
#    - In Egypt, Alexandria offers only about 100 jobs, indicating a much lower secondary hub compared to Saudi Arabia.
# 2. **Overall Job Distribution**:
#    - Saudi Arabia has a broader distribution of jobs across multiple cities (e.g., Dammam, Khobar, Sharqia), whereas Egypt's job market is heavily centralized in Cairo.
# 3. **Smaller Cities**:
#    - In Saudi Arabia, smaller cities like Qatif, Jizan, and Tabuk still have some job availability, albeit low.
#    - In Egypt, smaller cities like Sharm El-Sheikh, Matrouh, and Aswan have almost negligible job opportunities.
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong concentration of jobs in their capital cities, reflecting their economic and political significance.
# - However, Saudi Arabia shows a slightly more diversified job market across multiple cities, while Egypt's job market is heavily centralized in Cairo, with minimal opportunities elsewhere.
#%%
fig11 = job_distribution_by_city(df_egy[df_egy['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_egypt", folder='egypt',
                                 top_n=10, save=False)
fig12 = job_distribution_by_city(df_saudi[df_saudi['city'] != 'Unknown'],
                                 plot_name="job_distribution_by_city_saudi", folder='saudi',
                                 top_n=10, save=False)
#%% md
# ### **Plot 2: Number of Jobs by Company**
# #### **Similarities**
# 1. **Dominance of Leading Employers**:
#    - In both countries, a few leading companies dominate the job market. For example, **Saudi Aramco** in Saudi Arabia and **Talent 360** in Egypt have significantly higher job counts compared to other companies.
# 2. **Skewed Distribution**:
#    - Both plots show a highly skewed distribution, where a few companies offer the majority of jobs, while the rest have relatively low job availability.
# 3. **Presence of International Companies**:
#    - Both countries have international companies (e.g., Bechtel Corporation in Saudi Arabia and Vodafone in Egypt) contributing to the job market.
# #### **Differences**
# 1. **Leading Employer Job Availability**:
#    - In Saudi Arabia, **Saudi Aramco** offers over 200 jobs, which is substantial but not as high as **Talent 360** in Egypt, which offers over 290 jobs.
#    - The second-largest employer in Saudi Arabia (**InterContinental Hotels Group**) offers around 180 jobs, while in Egypt, **SSC - Egypt** offers around 180 jobs.
# 2. **Overall Job Distribution**:
#    - Saudi Arabia has a more diversified job market with several companies offering moderate job opportunities (e.g., NEOM, Eram Talent).
#    - Egypt has a more concentrated job market, with a few large employers (e.g., Talent 360, SSC - Egypt) dominating, while smaller companies have very limited job availability.
# 3. **Smaller Companies**:
#    - In Saudi Arabia, smaller companies like **Arthur Lawrence** and **WorleyParsons** still have some job availability, albeit low.
#    - In Egypt, smaller companies like **RAWAJ** and **Delivery Hero SE** have almost negligible job opportunities, indicating a more fragmented job market.
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong concentration of jobs in a few leading companies, reflecting their economic significance.
# - However, Saudi Arabia shows a slightly more diversified job market across multiple companies, while Egypt's job market is heavily centralized in a few large employers, with minimal opportunities elsewhere.
#%%
fig21 = analyze_jobs_by_company(df_egy, plot_name="analyze_jobs_by_company_egypt", folder='egypt',
                                save=False)
fig22 = analyze_jobs_by_company(df_saudi, plot_name="analyze_jobs_by_company_saudi", folder='saudi',
                                save=False)
#%% md
# ### **Plot 3: Top 10 Most Frequent Job Titles**
# #### **Similarities**
# 1. **Dominance of Accounting Roles**:
#    - In both countries, **Accountant** and **Account Manager** are among the top job titles, highlighting the importance of financial roles in both markets.
# 2. **Presence of Sales Roles**:
#    - Both plots show significant occurrences of sales-related roles (e.g., Sales Manager, Account Manager).
# 3. **Moderate Frequency of Technical Roles**:
#    - Both countries have moderate occurrences of technical roles, such as engineers (Mechanical Engineer, Civil Engineer in Saudi Arabia; Support Engineer, Software Engineer in Egypt).
# #### **Differences**
# 1. **Most Frequent Job Title**:
#    - In Saudi Arabia, **Sales Manager** is the most frequent job title, emphasizing a strong focus on sales.
#    - In Egypt, **Accountant** is the most frequent job title, indicating a greater emphasis on financial roles.
# 2. **Focus on Specific Industries**:
#    - Saudi Arabia shows a stronger focus on engineering roles (e.g., Mechanical Engineer, Civil Engineer), reflecting its industrial and infrastructure development.
#    - Egypt has a higher prevalence of roles related to technology and creativity (e.g., Business Analyst, Graphic Design, Software Engineer).
# 3. **Variation in Secondary Roles**:
#    - In Saudi Arabia, secondary roles include **Account Manager**, **Accountant**, and **Mechanical Engineer**.
#    - In Egypt, secondary roles include **Business Analyst**, **Account Manager**, and **Support Engineer**.
# #### **Conclusion**
# - Both Saudi Arabia and Egypt exhibit a strong demand for accounting and sales roles, reflecting their importance across various industries.
# - However, Saudi Arabia shows a more pronounced focus on engineering and sales, likely due to its industrial and economic structure.
# - Egypt, on the other hand, demonstrates a greater emphasis on technology, analytics, and creative roles, indicating a different set of industry priorities.
#%%
fig31 = get_top_job_titles_with_plot(df_egy, plot_name="get_top_job_titles_with_plot_egypt",
                                     folder='egypt', save=False)
fig32 = get_top_job_titles_with_plot(df_saudi, plot_name="get_top_job_titles_with_plot_saudi",
                                     folder='saudi', save=False)
#%% md
# ### **Plot 4: Job Distribution by Work Type**
# #### **Similarities**
# 1. **Dominance of On-site Jobs**:
#    - Both countries exhibit a strong preference for **on-site** jobs, with over 85% of jobs requiring physical presence.
# 2. **Low Remote Jobs**:
#    - Both countries have a very low percentage of **remote** jobs, indicating limited opportunities for fully remote work.
# 3. **Minimal Hybrid Jobs**:
#    - Both countries show a small share of **hybrid** jobs, reflecting limited adoption of flexible work models.
# #### **Differences**
# 1. **Proportion of On-site Jobs**:
#    - In Saudi Arabia, **on-site** jobs account for **93.0%**, which is significantly higher than Egypt's **86.5%**.
#    - This suggests a stronger emphasis on traditional workplace settings in Saudi Arabia.
# 2. **Proportion of Remote Jobs**:
#    - Egypt has a slightly higher percentage of **remote** jobs (9.9%) compared to Saudi Arabia (3.4%), indicating more opportunities for remote work in Egypt.
# 3. **Proportion of Hybrid Jobs**:
#    - Saudi Arabia has a slightly higher percentage of **hybrid** jobs (3.5%) compared to Egypt (3.6%), although both are minimal.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia heavily favor **on-site** jobs, reflecting a traditional approach to work arrangements.
# - However, Egypt shows a slightly higher prevalence of **remote** jobs, while Saudi Arabia demonstrates a marginally higher adoption of **hybrid** work models.
# - Overall, both countries have limited flexibility in work arrangements, with a strong reliance on physical workplace attendance.
#%%
fig41 = analyze_jobs_by_work_type(df_egy, plot_name="analyze_jobs_by_work_type_egypt",
                                  folder='egypt', save=False)
fig42 = analyze_jobs_by_work_type(df_saudi, plot_name="analyze_jobs_by_work_type_saudi",
                                  folder='saudi', save=False)
#%% md
# ### **Plot 5: Job Distribution by Gender**
# #### **Similarities**
# 1. **Dominance of No Preference**:
#    - In both countries, the majority of job postings fall under the **No Preference** category, reflecting a strong trend toward gender-neutral job advertisements.
# 2. **Low Gender-Specific Jobs**:
#    - Both countries have very few job postings that specify a preference for either **Male** or **Female** candidates.
# #### **Differences**
# 1. **Proportion of No Preference Jobs**:
#    - In Saudi Arabia, **No Preference** jobs account for **4,986 jobs**, which is significantly higher than Egypt's **3,815 jobs**.
#    - This suggests that Saudi Arabia has a larger overall job market or more gender-neutral job postings.
# 2. **Gender-Specific Jobs**:
#    - Egypt has very low numbers for both **Female** (130 jobs) and **Male** (64 jobs).
#    - Saudi Arabia shows slightly higher numbers for **Male** (274 jobs) and **Female** (245 jobs), indicating a marginal increase in gender-specific job opportunities compared to Egypt.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong preference for gender-neutral job postings, with the majority of jobs falling under the **No Preference** category.
# - However, Saudi Arabia shows a slightly higher prevalence of gender-specific job postings (both Male and Female) compared to Egypt, although these numbers remain relatively low overall.
# - This indicates a general trend toward inclusive hiring practices in both countries, with Saudi Arabia showing a marginally higher level of gender-specific job opportunities.
#%%
fig51 = analyze_jobs_by_gender(df_egy, plot_name="analyze_jobs_by_gender_egypt", folder='egypt',
                               save=False)
fig52 = analyze_jobs_by_gender(df_saudi, plot_name="analyze_jobs_by_gender_saudi", folder='saudi',
                               save=False)
#%% md
# ### **Plot 6: Job Distribution by Job Level**
# #### **Similarities**
# 1. **Dominance of Higher-Level Positions**:
#    - Both countries show a strong preference for higher-level positions such as **Senior** (in Egypt) and **Mid Level** (in Saudi Arabia).
# 2. **Low Representation of C-Suite and Senior Management**:
#    - Both countries have very few job openings for **C-Suite** and **Senior Management** roles, indicating a limited number of top-tier executive positions.
# 3. **Moderate Presence of Entry-Level Jobs**:
#    - Both countries have a moderate number of **Junior** and **Graduate** positions, suggesting opportunities for early-career professionals.
# #### **Differences**
# 1. **Most Common Job Level**:
#    - In Egypt, **Senior** positions are the most common, with **843 jobs**.
#    - In Saudi Arabia, **Mid Level** positions dominate with **138 jobs**.
# 2. **Distribution of Mid-Level Roles**:
#    - Egypt has a relatively low number of **Mid Level** jobs (**28 jobs**), while Saudi Arabia has a significantly higher number (**138 jobs**).
# 3. **Representation of Senior Roles**:
#    - Egypt has a much higher number of **Senior** jobs (**843 jobs**) compared to Saudi Arabia (**11 jobs**).
# 4. **Management Roles**:
#    - Egypt has more **Management** jobs (**679 jobs**) than Saudi Arabia (**69 jobs**).
# #### **Conclusion**
# - Both Egypt and Saudi Arabia prioritize hiring experienced professionals, with Egypt focusing more on **Senior** roles and Saudi Arabia emphasizing **Mid Level** positions.
# - There is a general scarcity of **C-Suite** and **Senior Management** roles in both countries, indicating a limited number of top executive opportunities.
# - While entry-level positions exist in both countries, they are not as dominant as higher-level roles, reflecting a stronger demand for experienced talent.
#%%
fig61 = analyze_jobs_by_job_level(df_egy[df_egy['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_egypt",
                                  folder='egypt', save=False)
fig62 = analyze_jobs_by_job_level(df_saudi[df_saudi['job_level'] != 'No Preference'],
                                  plot_name="analyze_jobs_by_job_level_saudi",
                                  folder='saudi', save=False)
#%% md
# ### **Plot 7: Number of Job Entries Over Time**
# #### **Similarities**
# 1. **Overall Trend**:
#    - Both countries show a consistent upward trend in job entries from November 2025 to March 2025, indicating increasing job opportunities.
# 2. **Rapid Growth Period**:
#    - In both countries, the most significant growth occurs between January and March 2025, suggesting a common factor influencing job market dynamics during this period.
# 3. **Slight Decline in April**:
#    - Both countries experience a minor decline in job entries in April 2025, although the numbers remain high compared to earlier months.
# #### **Differences**
# 1. **Magnitude of Job Entries**:
#    - Saudi Arabia consistently has a higher number of job entries compared to Egypt throughout the entire period.
#    - For example, in March 2025, Saudi Arabia reaches **1,600 jobs**, while Egypt reaches **1,200 jobs**.
# 2. **Initial Starting Point**:
#    - Both countries start with a very low number of job entries in November 2025, but Saudi Arabia appears to have a slightly higher initial baseline.
# 3. **Peak Values**:
#    - Saudi Arabia's peak in March 2025 is significantly higher (**1,600 jobs**) compared to Egypt's peak (**1,200 jobs**).
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit positive trends in job entries over the six-month period, reflecting improving job markets.
# - However, Saudi Arabia demonstrates a stronger job market overall, with consistently higher job entry numbers and a more pronounced peak in March 2025.
# - The slight declines in April 2025 for both countries suggest potential temporary adjustments or seasonal fluctuations, but the overall upward trajectory remains strong.
#%%
fig71 = plot_job_trend_over_time(df_egy, plot_name="plot_job_trend_over_time_egypt", folder='egypt',
                                 save=False)
fig72 = plot_job_trend_over_time(df_saudi, plot_name="plot_job_trend_over_time_saudi", folder='saudi',
                                 save=False)
#%% md
# ### **Plot 8: The Highest 10 Areas Declared for Business Opportunities**
# #### **Similarities**
# 1. **Dominance of Other Commercial Support Services**:
#    - Both countries show **Other Commercial Support Services** as the leading domain, indicating a strong demand for services that support commercial activities.
# 2. **Presence of Professional Services**:
#    - Both plots highlight domains such as **Management Consultancy** and **General Engineering Consultancy**, reflecting a focus on professional services.
# 3. **Moderate Presence of Retail and Hospitality**:
#    - Both countries have moderate job opportunities in **Retail** and **Hospitality and Accommodation**, showing the importance of these sectors in both economies.
# #### **Differences**
# 1. **Magnitude of Job Opportunities**:
#    - In Saudi Arabia, **Other Commercial Support Services** has **3,835 jobs**, which is significantly higher than Egypt's **3,240 jobs**.
#    - This suggests a larger overall job market or more diverse opportunities in Saudi Arabia.
# 2. **Prominence of Construction**:
#    - **Construction** is a significant domain in Saudi Arabia (**94 jobs**) but does not appear in the top 10 for Egypt, indicating a stronger focus on infrastructure development in Saudi Arabia.
# 3. **Oil and Gas Sector**:
#    - **Oil and Gas** is a notable domain in Saudi Arabia (**46 jobs**) but is not present in Egypt, reflecting the importance of the oil industry in Saudi Arabia.
# 4. **Healthcare Services**:
#    - **Other Healthcare Services** appears in the top 10 for Saudi Arabia (**39 jobs**) but is not present in Egypt, suggesting a stronger emphasis on healthcare opportunities in Saudi Arabia.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong demand for **Other Commercial Support Services**, indicating a common trend in the need for services that support commercial activities.
# - However, Saudi Arabia shows a larger overall job market and a stronger focus on sectors like **Construction**, **Oil and Gas**, and **Healthcare Services**, reflecting its economic diversification efforts.
# - Egypt, on the other hand, has a more balanced distribution of opportunities across domains such as **General Engineering Consultancy**, **Management Consultancy**, and **Retail**, highlighting a different set of priorities in its economy.
#%%
fig81 = plot_job_postings_by_industry(df_egy, plot_name="plot_job_postings_by_industry_egypt",
                                      folder='egypt', save=False)
fig82 = plot_job_postings_by_industry(df_saudi, plot_name="plot_job_postings_by_industry_saudi",
                                      folder='saudi', save=False)
#%% md
# ### **Plot 9: Job Distribution by Type**
# #### **Similarities**
# 1. **Dominance of Unknown Jobs**:
#    - Both countries show a high percentage of **Unknown** job types, with Egypt at **76.48%** and Saudi Arabia at **76.77%**. This suggests a common issue of incomplete job descriptions across both markets.
# 2. **Low Occurrence of Part-Time, Contracts, and Temporary Jobs**:
#    - Both countries have very low percentages for part-time, contract, and temporary jobs, indicating that these job types are not widely available in either market.
# 3. **Moderate Presence of Internships**:
#    - Both countries have a small but present number of internship opportunities, with Egypt at **1.47%** and Saudi Arabia at **0.31%**.
# #### **Differences**
# 1. **Full-Time Jobs**:
#    - In Saudi Arabia, **Full-Time** jobs account for **21.82%**, which is significantly higher than Egypt's **3.14%**. This suggests a stronger emphasis on permanent employment in Saudi Arabia.
# 2. **Management Roles**:
#    - Egypt has a much higher percentage of **Management** roles (**18.68%**) compared to Saudi Arabia (**0.73%**). This indicates a substantial difference in the demand for leadership positions between the two countries.
# 3. **Distribution of Other Job Types**:
#    - While both countries have low percentages for internships, part-time roles, contracts, and temporary jobs, the specific percentages differ slightly. For example, Saudi Arabia has a slightly higher percentage for internships (**0.31%**) compared to Egypt (**1.47%**).
# #### **Conclusion**
# - Both Egypt and Saudi Arabia face a challenge with a large proportion of job listings being categorized as **Unknown**, highlighting a need for more detailed job descriptions.
# - Saudi Arabia shows a stronger focus on **Full-Time** employment compared to Egypt, while Egypt has a significantly higher demand for **Management** roles.
# - Overall, both countries exhibit a limited availability of part-time, contract, and temporary jobs, with internships also being relatively rare but more prevalent in Egypt.
#%%
fig91 = analyze_job_type_distribution(df_egy, plot_name="analyze_job_type_distribution_egypt",
                                      folder='egypt', save=False)
fig92 = analyze_job_type_distribution(df_saudi, plot_name="analyze_job_type_distribution_saudi",
                                      folder='saudi', save=False)
#%% md
# ### **Plot 10: Comparison of Min & Max Experience Requirements**
# #### **Similarities**
# 1. **Median Minimum Experience**:
#    - Both countries show a median minimum experience requirement of around **3 years**, indicating that most entry-level or mid-level roles do not require extensive prior experience.
# 2. **Range of Minimum Experience**:
#    - Both countries have a similar IQR for minimum experience, ranging from **0 to 6 years**, suggesting a comparable distribution of low-experience roles.
# 3. **Presence of Outliers**:
#    - Both plots show outliers with higher minimum experience requirements (up to **10 years**), indicating that specialized or senior roles exist in both markets.
# 4. **Median Maximum Experience**:
#    - Both countries have a median maximum experience requirement of around **8–9 years**, suggesting that most job postings target professionals with moderate experience levels.
# 5. **Range of Maximum Experience**:
#    - Both countries have a wide range of maximum experience requirements, with IQRs spanning from **5 to 15–17 years**, reflecting diverse job opportunities across different experience levels.
# 6. **High Outliers for Maximum Experience**:
#    - Both plots show outliers with very high maximum experience requirements (up to **20 years**), indicating that senior-level or highly specialized roles exist in both markets.
# #### **Differences**
# 1. **Median Maximum Experience**:
#    - Saudi Arabia has a slightly higher median maximum experience requirement (**9 years**) compared to Egypt (**8 years**), suggesting that Saudi Arabia may have a slightly higher demand for experienced professionals.
# 2. **Range of Maximum Experience**:
#    - Saudi Arabia has a slightly wider IQR for maximum experience (**5 to 17 years**) compared to Egypt (**5 to 15 years**), indicating a broader range of experience requirements in Saudi Arabia.
# 3. **Outliers for Maximum Experience**:
#    - Saudi Arabia has more pronounced outliers for maximum experience, with values reaching **20 years**, compared to Egypt, which also has outliers but at a similar level.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit similar patterns in terms of minimum and maximum experience requirements, with most job postings targeting professionals with 3–9 years of experience.
# - However, Saudi Arabia shows a slightly higher demand for experienced professionals, as indicated by the higher median maximum experience requirement and the broader range of experience levels.
# - Both countries have a mix of entry-level, mid-level, and senior-level roles, with some specialized positions requiring significantly more experience.
#%%
fig101 = compare_experience_requirements(df_egy, plot_name="compare_experience_requirements_egypt",
                                         folder='egypt', save=False)
fig102 = compare_experience_requirements(df_saudi, plot_name="compare_experience_requirements_saudi",
                                         folder='saudi', save=False)
#%% md
# ### **Plot 11: Heatmap of Job Count by City and Job Level**
# #### **Similarities**
# 1. **Dominance of Major Cities**:
#    - In both countries, a few major cities (Cairo in Egypt and Riyadh in Saudi Arabia) dominate the job market, offering the majority of job opportunities.
# 2. **High Count of No Preference Jobs**:
#    - Both countries show a strong preference for **No Preference** jobs, indicating that many employers are flexible regarding job level requirements.
# 3. **Concentration of Opportunities**:
#    - Both countries exhibit a concentration of job opportunities in major urban centers, with smaller cities having very limited job availability.
# 4. **Mid Level and Management Roles**:
#    - Both countries show significant demand for **Mid Level** and **Management** roles in major cities.
# #### **Differences**
# 1. **Magnitude of Job Counts**:
#    - Saudi Arabia has significantly higher job counts overall, especially in major cities like Riyadh, where the **No Preference** category reaches 1,970 jobs.
#    - Egypt's highest job count is 1,160 jobs in Cairo, which is lower than Saudi Arabia's numbers.
# 2. **Number of Prominent Cities**:
#    - Egypt has two prominent cities (Cairo and Alexandria), while Saudi Arabia has more prominent cities (Riyadh, Dammam, etc.), although Riyadh dominates the job market.
# 3. **Distribution Across Job Levels**:
#    - In Egypt, **No Preference** jobs are highly dominant across all cities.
#    - In Saudi Arabia, **Mid Level** jobs also show high counts in major cities, contributing significantly to the job market.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong concentration of job opportunities in major urban centers, with Cairo and Riyadh being the primary hubs for employment.
# - The high count of **No Preference** jobs in both countries reflects a trend toward flexible hiring practices.
# - Saudi Arabia shows a larger overall job market, with higher job counts across major cities, while Egypt has a more focused job market centered around Cairo and Alexandria.
#%%
fig111 = jobs_heatmap_by_city_and_job_level(df_egy, plot_name="jobs_heatmap_by_city_and_job_level_egypt",
                                            folder='egypt', save=False)
fig112 = jobs_heatmap_by_city_and_job_level(df_saudi, plot_name="jobs_heatmap_by_city_and_job_level_saudi",
                                            folder='saudi', save=False)
#%% md
# ### **Plot 12: Most Common Job Titles (Wordcloud)t**
# #### **Similarities**
# 1. **Dominance of Managerial Roles**:
#    - Both countries show a strong emphasis on **managerial positions**, with words like **Manager**, **Lead**, and **Supervisor** appearing prominently.
# 2. **Presence of Specialized Roles**:
#    - Both word clouds include terms like **Specialist**, **Engineer**, and **Analyst**, indicating a demand for specialized skills.
# 3. **Focus on Sales and Customer-Facing Roles**:
#    - Words like **Sales Manager**, **Account Manager**, and **Customer Service** appear in both plots, reflecting a common need for sales and client-facing roles.
# 4. **Technical and Analytical Roles**:
#    - Both countries have a mix of technical and analytical roles, with terms like **Software Engineer**, **Data Analyst**, and **Business Analyst** appearing in both word clouds.
# #### **Differences**
# 1. **Prominent Job Titles**:
#    - In Egypt, **Account Manager** and **Accountant** are highly prominent, indicating a strong focus on accounting and sales roles.
#    - In Saudi Arabia, **Consultant** and **Engineer** stand out, reflecting a greater emphasis on consulting and engineering roles.
# 2. **Industry-Specific Roles**:
#    - Egypt has more prominent roles in **customer service** and **design engineering**, while Saudi Arabia shows a stronger presence of **civil engineering** and **security** roles.
# 3. **Leadership Roles**:
#    - Saudi Arabia has a higher prominence of **Director** and **Business Development** roles, suggesting a stronger focus on leadership and strategic roles compared to Egypt.
# #### **Conclusion**
# - Both Egypt and Saudi Arabia exhibit a strong demand for **managerial** and **specialized roles**, with a focus on **technical** and **analytical** skills.
# - However, Egypt shows a stronger emphasis on **accounting** and **sales**, while Saudi Arabia highlights **consulting**, **engineering**, and **leadership** roles.
# - The differences reflect variations in industry priorities and economic structures between the two countries, with Egypt leaning toward services and sales, and Saudi Arabia focusing on engineering and strategic development.
#%%
fig121 = plot_top_job_titles_wordcloud(df_egy, plot_name="plot_top_job_titles_wordcloud_egypt",
                                       folder='egypt', save=False)
fig122 = plot_top_job_titles_wordcloud(df_saudi, plot_name="plot_top_job_titles_wordcloud_saudi",
                                       folder='saudi', save=False)
