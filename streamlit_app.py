# ---------------------------
# Import Libraries & Packages
# ---------------------------
from scripts.analysis import *
import sqlite3
import pandas as pd
import streamlit as st

# ---------------------------
# Import Data
# ---------------------------
df_egypt_before = pd.read_csv('data/raw/egypt_raw.csv')
df_saudi_before = pd.read_csv('data/raw/saudi-arabia_raw.csv')

# Assuming 'database.db' is in the same directory or accessible
conn = sqlite3.connect('data/database.db')
df_egypt = pd.read_sql('SELECT * FROM EGYPT', conn)

df_saudi = pd.read_sql('SELECT * FROM [saudi-arabia]', conn)

# ---------------------------
# Import Plots
# ---------------------------
fig1_egypt = job_distribution_by_city(df_egypt[df_egypt['city'] != 'Unknown'],
                                      plot_name="job_distribution_by_city_egypt", folder='egypt',
                                      top_n=10, save=False)
fig2_egypt = analyze_jobs_by_company(df_egypt, plot_name="analyze_jobs_by_company_egypt", folder='egypt',
                                     save=False)
fig3_egypt = get_top_job_titles_with_plot(df_egypt, plot_name="get_top_job_titles_with_plot_egypt",
                                          folder='egypt', save=False)
fig4_egypt = analyze_jobs_by_work_type(df_egypt, plot_name="analyze_jobs_by_work_type_egypt",
                                       folder='egypt', save=False)
fig5_egypt = analyze_jobs_by_gender(df_egypt, plot_name="analyze_jobs_by_gender_egypt", folder='egypt',
                                    save=False)
fig6_egypt = analyze_jobs_by_job_level(df_egypt[df_egypt['job_level'] != 'No Preference'],
                                       plot_name="analyze_jobs_by_job_level_egypt",
                                       folder='egypt', save=False)
fig7_egypt = plot_job_trend_over_time(df_egypt, plot_name="plot_job_trend_over_time_egypt", folder='egypt',
                                      save=False)
fig8_egypt = plot_job_postings_by_industry(df_egypt, plot_name="plot_job_postings_by_industry_egypt",
                                           folder='egypt', save=False)
fig9_egypt = analyze_job_type_distribution(df_egypt, plot_name="analyze_job_type_distribution_egypt",
                                           folder='egypt', save=False)
fig10_egypt = compare_experience_requirements(df_egypt, plot_name="compare_experience_requirements_egypt",
                                              folder='egypt', save=False)
fig11_egypt = jobs_heatmap_by_city_and_job_level(df_egypt, plot_name="jobs_heatmap_by_city_and_job_level_egypt",
                                                 folder='egypt', save=False)
fig12_egypt = plot_top_job_titles_wordcloud(df_egypt, plot_name="plot_top_job_titles_wordcloud_egypt",
                                            folder='egypt', save=False)

fig1_saudi = job_distribution_by_city(df_saudi[df_saudi['city'] != 'Unknown'],
                                      plot_name="job_distribution_by_city_saudi", folder='saudi',
                                      top_n=10, save=False)
fig2_saudi = analyze_jobs_by_company(df_saudi, plot_name="analyze_jobs_by_company_saudi", folder='saudi',
                                     save=False)
fig3_saudi = get_top_job_titles_with_plot(df_saudi, plot_name="get_top_job_titles_with_plot_saudi",
                                          folder='saudi', save=False)
fig4_saudi = analyze_jobs_by_work_type(df_saudi, plot_name="analyze_jobs_by_work_type_saudi",
                                       folder='saudi', save=False)
fig5_saudi = analyze_jobs_by_gender(df_saudi, plot_name="analyze_jobs_by_gender_saudi", folder='saudi',
                                    save=False)
fig6_saudi = analyze_jobs_by_job_level(df_saudi[df_saudi['job_level'] != 'No Preference'],
                                       plot_name="analyze_jobs_by_job_level_saudi",
                                       folder='saudi', save=False)
fig7_saudi = plot_job_trend_over_time(df_saudi, plot_name="plot_job_trend_over_time_saudi", folder='saudi',
                                      save=False)
fig8_saudi = plot_job_postings_by_industry(df_saudi, plot_name="plot_job_postings_by_industry_saudi",
                                           folder='saudi', save=False)
fig9_saudi = analyze_job_type_distribution(df_saudi, plot_name="analyze_job_type_distribution_saudi",
                                           folder='saudi', save=False)
fig10_saudi = compare_experience_requirements(df_saudi, plot_name="compare_experience_requirements_saudi",
                                              folder='saudi', save=False)
fig11_saudi = jobs_heatmap_by_city_and_job_level(df_saudi, plot_name="jobs_heatmap_by_city_and_job_level_saudi",
                                                 folder='saudi', save=False)
fig12_saudi = plot_top_job_titles_wordcloud(df_saudi, plot_name="plot_top_job_titles_wordcloud_saudi",
                                            folder='saudi', save=False)


# ---------------------------
# Streamlit App
# ---------------------------
def main():
    # ---------------------------
    # Sidebar Navigation
    # ---------------------------
    plot_names = [
        "Job Distribution by City",
        "Jobs by Company",
        "Top Job Titles",
        "Jobs by Work Type",
        "Jobs by Gender",
        "Jobs by Job Level",
        "Job Trend Over Time",
        "Job Postings by Industry",
        "Job Type Distribution",
        "Experience Requirements",
        "Heatmap by City and Job Level",
        "Top Job Titles Word Cloud"
    ]
    egypt_figs = [fig1_egypt, fig2_egypt, fig3_egypt, fig4_egypt, fig5_egypt, fig6_egypt,
                  fig7_egypt, fig8_egypt, fig9_egypt, fig10_egypt, fig11_egypt, fig12_egypt]
    saudi_figs = [fig1_saudi, fig2_saudi, fig3_saudi, fig4_saudi, fig5_saudi, fig6_saudi,
                  fig7_saudi, fig8_saudi, fig9_saudi, fig10_saudi, fig11_saudi, fig12_saudi]

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Home", "Egypt Market", "Saudi Market", "Comparison"])

    # ---------------------------
    # Page Content
    # ---------------------------
    st.title("Job Market Analysis")

    if page == "Home":
        st.header("Welcome to the Job Market Analysis App")
        st.write(
            """**Home section displays Data Cleaning and Transformation related to the Egyptian & Saudi Arabia Datasets.**""")
        st.markdown("Egypt Dataset Before Preprocessing")
        st.dataframe(df_egypt_before)
        st.markdown("Saudi Arabia Dataset Before Preprocessing")
        st.dataframe(df_saudi_before)
        st.write("""## Data Cleaning and Transformation Summary
            
            ### 1. **Initial Column Splitting**
               - **Location**: Extracted `city` by splitting the `location` column using the separator `·`.
               - **Career Level**: Divided `career_level` into `type`, `exp`, and `no_exp` columns.
            
            ### 2. **Handling Missing Values**
               - Replaced "Unknown" values in `exp` and `no_exp` with `NaN`.
               - Combined similar columns (`experience` & `exp`, `num_of_exp` & `no_exp`) into new columns (`experience_`, `num_of_exp_years`).
               - Filled missing values in categorical columns (`remote`, `age`, `sex`, etc.) with default values like "لا تفضيل" (no preference).
            
            ### 3. **Dropping Unnecessary Columns**
               - Removed irrelevant columns such as `age`, `salary`, `qualification`, and others that were not needed for analysis.
            
            ### 4. **Standardizing Job Titles**
               - Removed leading numbers, periods, and unwanted terms (e.g., "sr", "junior") from job titles.
               - Mapped job titles to standardized names using predefined mappings.
            
            ### 5. **Manual Adjustments and Translation**
               - Manually cleaned and translated the `title` column for consistency.
               - Removed rows containing specific keywords like "سعودية", "saudi".
            
            ### 6. **Updating Experience Information**
               - Updated rows where `type` included "تدريب" to set `experience_` to "خريج جديد" (New Graduate).
            
            ### 7. **Extracting Additional Information**
               - Extracted gender and remote work information from text columns (`title`, `description`, `skills`).
            
            ### 8. **Final Adjustments**
               - Dropped unnecessary columns like `description` and `skills`.
               - Processed and cleaned the `num_of_exp_years` column.""")

        st.markdown("Egypt Dataset After Preprocessing")
        st.dataframe(df_egypt)
        st.markdown("Saudi Arabia Dataset After Preprocessing")
        st.dataframe(df_saudi)

    elif page == "Egypt Market":
        st.header("Egypt Job Market")
        st.write("**This section displays analysis related to the Egyptian job market.**")
        egypt_explanations = [
            "- Bar chart showing the top 10 cities in Egypt based on the number of jobs available.\n"
            "- Cairo dominates with over 2,000 jobs, followed by Alexandria (~100 jobs) and other cities like New Cairo and Sharm El-Sheikh with fewer than 50 jobs each.\n",

            "- Bar chart displaying job availability by company in Egypt.\n"
            "- Talent 360 leads with over 290 jobs, followed by SSC - Egypt (~180 jobs) and Vodafone - Egypt (100-120 jobs).\n",

            "- Horizontal bar chart showing the most frequent job titles in Egypt.\n"
            "- Accountant is the most common title (80+ occurrences), followed by Business Analyst (~65) and Account Manager (~60).\n",

            "- Pie chart representing work types in Egypt (On-site, Remote, Hybrid).\n"
            "- On-site jobs dominate (86.5%), while remote (9.9%) and hybrid (3.6%) roles are less common.\n",

            "- Bar chart illustrating job distribution by gender in Egypt.\n"
            "- Most job postings have 'No Preference' (3,815 jobs), while Female (130) and Male (64) roles are significantly lower.\n",

            "- Bar chart showing job levels in Egypt (Senior, Management, Junior, etc.).\n"
            "- Senior roles dominate (843 jobs), followed by Management (679) and Junior (79).\n",

            "- Line chart showing job entries over time (Nov 2025 - Apr 2025).\n"
            "- Significant growth observed between January and March 2025, peaking around 1,200 jobs in March.\n",

            "- Bar chart displaying top 10 domains for business opportunities in Egypt.\n"
            "- 'Other Commercial Support Services' leads (3,240 jobs), followed by 'General Engineering Consultancy' (97) and 'Management Consultancy' (85).\n",

            "- Pie chart representing job types in Egypt.\n"
            "- 'Unknown' dominates (76.48%), followed by 'Management' (18.68%) and 'Full-Time' (3.14%).\n",

            "- Box plot comparing minimum and maximum experience requirements for jobs in Egypt.\n"
            "- Median min experience is 3 years, while max experience is around 8 years, with significant variability.\n",

            "- Heatmap showing job distribution by city and job level in Egypt.\n"
            "- Cairo leads in all levels, particularly in 'No Preference' (1,160 jobs) and 'Mid Level' (509 jobs).\n",

            "- Word cloud visualizing the most frequent job titles in Egypt.\n"
            "- Common titles include 'Account Manager', 'Manager', 'Senior', 'Lead', and 'Accountant'.\n"
        ]

        for i in range(len(egypt_figs)):
            st.subheader(f"Egypt: {plot_names[i]}")
            st.write(f"{egypt_explanations[i]}")
            st.pyplot(egypt_figs[i])


    elif page == "Saudi Market":
        st.header("Saudi Arabia Job Market")
        st.write("**This section displays analysis related to the Saudi Arabian job market.**")
        saudi_explanations = [
            "- Bar chart showing the top 10 cities in Saudi Arabia based on the number of jobs available.\n"
            "- Riyadh dominates with over 2,000 jobs, followed by Jeddah (~500 jobs) and other cities like Dammam and Khobar with moderate numbers (100-300 jobs).\n",

            "- Bar chart displaying job availability by company in Saudi Arabia.\n"
            "- Saudi Aramco leads with over 200 jobs, followed by InterContinental Hotels Group (~180 jobs) and Jobs for Humanity (120-170 jobs).\n",

            "- Horizontal bar chart showing the most frequent job titles in Saudi Arabia.\n"
            "- Sales Manager is the most common title (85+ occurrences), followed by Account Manager (~85) and Accountant (~80).\n",

            "- Pie chart representing work types in Saudi Arabia (On-site, Remote, Hybrid).\n"
            "- On-site jobs dominate (93.0%), while remote (3.4%) and hybrid (3.5%) roles are less common.\n",

            "- Bar chart illustrating job distribution by gender in Saudi Arabia.\n"
            "- Most job postings have 'No Preference' (4,986 jobs), while Male (274) and Female (245) roles are significantly lower.\n",

            "- Bar chart showing job levels in Saudi Arabia (Mid Level, Management, Junior, etc.).\n"
            "- Mid Level roles dominate (138 jobs), followed by Management (69) and Junior (28).\n",

            "- Line chart showing job entries over time (Nov 2025 - Apr 2025).\n"
            "- Significant growth observed between January and March 2025, peaking around 1,600 jobs in March.\n",

            "- Bar chart displaying top 10 domains for business opportunities in Saudi Arabia.\n"
            "- 'Other Commercial Support Services' leads (3,835 jobs), followed by 'Management Consultancy' (109) and 'Construction' (94).\n",

            "- Pie chart representing job types in Saudi Arabia.\n"
            "- 'Unknown' dominates (76.77%), followed by 'Full-Time' (21.82%) and 'Management' (0.73%).\n",

            "- Box plot comparing minimum and maximum experience requirements for jobs in Saudi Arabia.\n"
            "- Median min experience is 3 years, while max experience is around 9 years, with significant variability.\n",

            "- Heatmap showing job distribution by city and job level in Saudi Arabia.\n"
            "- Riyadh leads in all levels, particularly in 'No Preference' (1,970 jobs) and 'Mid Level' (2,020 jobs).\n",

            "- Word cloud visualizing the most frequent job titles in Saudi Arabia.\n"
            "- Common titles include 'Consultant', 'Supervisor', 'Specialist', 'Engineer', 'Lead', and 'Manager'.\n"
        ]
        for i in range(len(saudi_figs)):
            st.subheader(f"Saudi Arabia: {plot_names[i]}")
            st.write(f"{saudi_explanations[i]}")
            st.pyplot(saudi_figs[i])


    elif page == "Comparison":
        st.header("Comparison: Egypt vs Saudi Arabia")
        st.write("This section compares the two job markets side by side.")

        # Create a list of plot figures for easier iteration
        comparison_explanations = [
            "- **Top Cities by Job Availability**:\n"
            "  - Similarities: Both countries show dominance of capital cities (Cairo in Egypt, Riyadh in Saudi Arabia) with skewed distributions.\n"
            "  - Differences: Saudi Arabia has broader job distribution across cities like Jeddah, Dammam, and Khobar, while Egypt’s jobs are heavily centralized in Cairo.\n"
            "  - Conclusion: Riyadh and Cairo dominate their respective job markets, but Saudi Arabia exhibits slightly more diversified opportunities beyond the capital.\n",

            "- **Jobs by Company**:\n"
            "  - Similarities: A few leading companies dominate job markets in both countries (e.g., Talent 360 in Egypt, Saudi Aramco in Saudi Arabia).\n"
            "  - Differences: Saudi Arabia shows more diversity among mid-tier companies, while Egypt's job market is concentrated in fewer large employers.\n"
            "  - Conclusion: While both markets rely on major employers, Saudi Arabia offers more balanced opportunities across various companies.\n",

            "- **Most Frequent Job Titles**:\n"
            "  - Similarities: Both emphasize accounting and sales roles (e.g., Accountant, Sales Manager).\n"
            "  - Differences: Saudi Arabia focuses more on engineering roles, whereas Egypt leans toward technology and creative roles.\n"
            "  - Conclusion: Industry priorities differ; Saudi Arabia prioritizes industrial development, while Egypt emphasizes tech and innovation.\n",

            "- **Work Type Distribution**:\n"
            "  - Similarities: On-site jobs dominate in both countries (>85%).\n"
            "  - Differences: Saudi Arabia has a higher proportion of on-site jobs (93%) and slightly more hybrid roles, while Egypt offers marginally more remote work options.\n"
            "  - Conclusion: Both favor traditional workplace settings, though Egypt provides slightly more flexibility for remote work.\n",

            "- **Job Distribution by Gender**:\n"
            "  - Similarities: 'No Preference' dominates in both countries, indicating gender-neutral hiring practices.\n"
            "  - Differences: Saudi Arabia has slightly more gender-specific postings (Male and Female), but these remain low overall.\n"
            "  - Conclusion: Both prioritize inclusive hiring, but Saudi Arabia shows a marginal increase in gender-specific opportunities.\n",

            "- **Job Levels**:\n"
            "  - Similarities: Higher-level positions dominate, with limited C-Suite/Senior Management roles.\n"
            "  - Differences: Egypt favors Senior roles (843 jobs), while Saudi Arabia emphasizes Mid Level roles (138 jobs).\n"
            "  - Conclusion: Egypt focuses on experienced professionals, while Saudi Arabia targets mid-career individuals.\n",

            "- **Job Entries Over Time**:\n"
            "  - Similarities: Both show upward trends from November 2025 to March 2025, peaking in March before slight declines in April.\n"
            "  - Differences: Saudi Arabia consistently outperforms Egypt in total job entries, reaching 1,600 vs. 1,200 at peak.\n"
            "  - Conclusion: Saudi Arabia demonstrates stronger growth and larger job market size compared to Egypt.\n",

            "- **Top Domains for Business Opportunities**:\n"
            "  - Similarities: 'Other Commercial Support Services' leads in both countries.\n"
            "  - Differences: Saudi Arabia includes Construction, Oil and Gas, and Healthcare prominently, reflecting economic diversification efforts.\n"
            "  - Conclusion: Shared focus on commercial support services, but Saudi Arabia's broader sectoral spread reflects its strategic initiatives.\n",

            "- **Job Types**:\n"
            "  - Similarities: 'Unknown' dominates in both countries (~76%), highlighting incomplete job descriptions.\n"
            "  - Differences: Saudi Arabia emphasizes Full-Time roles (21.82% vs. 3.14% in Egypt), while Egypt prioritizes Management roles (18.68% vs. 0.73%).\n"
            "  - Conclusion: Saudi Arabia leans toward permanent employment, whereas Egypt seeks leadership talent.\n",

            "- **Experience Requirements**:\n"
            "  - Similarities: Median min experience ~3 years; max experience ~8-9 years; outliers exist for senior roles.\n"
            "  - Differences: Saudi Arabia shows slightly higher max experience requirements (median 9 years vs. 8 in Egypt).\n"
            "  - Conclusion: Both cater to mid-career professionals, but Saudi Arabia demands slightly more experienced candidates.\n",

            "- **Heatmap of Jobs by City and Level**:\n"
            "  - Similarities: Major cities (Cairo, Riyadh) dominate; 'No Preference' is prevalent.\n"
            "  - Differences: Saudi Arabia has higher overall job counts and more prominent secondary cities (e.g., Dammam).\n"
            "  - Conclusion: Concentration in urban centers persists, but Saudi Arabia offers greater geographic diversity.\n",

            "- **Word Cloud of Job Titles**:\n"
            "  - Similarities: Managerial, specialized, and sales roles dominate.\n"
            "  - Differences: Egypt highlights Accounting and Sales roles, while Saudi Arabia emphasizes Consulting, Engineering, and Leadership roles.\n"
            "  - Conclusion: Role prominence reflects differing industry priorities—Egypt focuses on services, while Saudi Arabia leans toward engineering and strategy.\n"
        ]

        # Use st.columns to create two columns for each comparison
        for i in range(len(egypt_figs)):
            st.subheader(f"Comparison: {plot_names[i]}")
            st.write(f"{comparison_explanations[i]}")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"Egypt: {plot_names[i]}")
                st.pyplot(egypt_figs[i])
            with col2:
                st.markdown(f"Saudi Arabia: {plot_names[i]}")
                st.pyplot(saudi_figs[i])
    elif page == 'Team Members Profile':
        st.header(f"Team Members Profile")

    # ---------------------------
    # Footer or Credits
    # ---------------------------
    st.markdown("---")
    st.markdown("Created by DataMentes Team | Job Market Analysis Tool")
    st.page_link('https://team-portfolio.streamlit.app', label='Team Members Profile')


if __name__ == "__main__":
    main()
