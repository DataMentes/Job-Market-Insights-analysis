import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
countries = {
    'saudi-arabia': 276,
    'egypt': 205,
}
# Web scraping logic here
def scrapping(country, total_pages):
    all_jobs = []
    for page in range(1, total_pages + 1):
        url = f"https://www.bayt.com/ar/{country}/jobs/?page={page}"
        print(f"⏳ بيتم معالجة الصفحة: {page} / {total_pages}")

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        job_cards = soup.find_all('li', class_='has-pointer-d')

        for job in job_cards:
            link_tag = job.find('a', {'data-js-aid': 'jobID'})
            if not link_tag or not link_tag.get('href'):
                print("❌ خطأ في الرابط")
                continue
            link = 'https://www.bayt.com' + link_tag.get('href')
            content = requests.get(link).text
            job_soup = BeautifulSoup(content, 'html5lib')

            title_elem = job_soup.find('h1', {'id': 'job_title'})
            title = title_elem.text.strip() if title_elem else None

            company_elem = job_soup.find('a', {'class': 't-default t-bold'})
            company_name = company_elem.text.strip() if company_elem else None

            date_elem = job_soup.find('span', {'id': 'jb-posted-date'})
            date = date_elem.text.strip() if date_elem else None

            salary_elem = job_soup.find('div', {'data-automation-id': 'id_salary_range'})
            salary = salary_elem.text.strip() if salary_elem else None

            career_level_elem = job_soup.find('div', {'data-automation-id': 'id_type_level_experience'})
            career_level = career_level_elem.text.strip() if career_level_elem else None

            location_elem = job_soup.find('span', {'class': 't-mute'})
            location = location_elem.text.strip() if location_elem else None

            num_of_vacancies_elem = job_soup.find('div', {'data-automation-id': 'id_number_of_vacancies'})
            num_of_vacancies = num_of_vacancies_elem.text.strip() if num_of_vacancies_elem else None

            industry_elem = job_soup.find('div', {'data-automation-id': 'id_company_employees_industry'})
            industry = industry_elem.text.strip() if industry_elem else None

            decription_elem = job_soup.find('div', {'class': 'card-content p20t is-spaced'})
            description_header = decription_elem.find_next('h2')
            description_text = description_header.find_next('div')
            description = description_text.text.strip() if description_text else None

            skills_elem = job_soup.find('div', {'class': 'card-content is-spaced t-break print-break-before p20t'})
            skills = skills_elem.text.strip() if skills_elem else None

            remote_elem = job_soup.find('div', {'data-automation-id': 'id_remote_working'})
            remote = remote_elem.text.strip() if remote_elem else None

            num_of_exp_elem = job_soup.find('div', {'data-automation-id': 'data_عدد_سنوات_الخبرة'})
            num_of_exp = num_of_exp_elem.text.strip() if num_of_exp_elem else None

            residence_area_elem = job_soup.find('div', {'data-automation-id': 'data_منطقة_الإقامة'})
            residence_area = residence_area_elem.text.strip() if residence_area_elem else None

            nationality_elem = job_soup.find('div', {'data-automation-id': 'data_الجنسية'})
            nationality = nationality_elem.text.strip() if nationality_elem else None

            sex_elem = job_soup.find('div', {'data-automation-id': 'data_الجنس'})
            sex = sex_elem.text.strip() if sex_elem else None

            qualification_elem = job_soup.find('div', {'data-automation-id': 'data_الشهادة'})
            qualification = qualification_elem.text.strip() if qualification_elem else None

            age_elem = job_soup.find('div', {'data-automation-id': 'data_العمر'})
            age = age_elem.text.strip() if age_elem else None

            specialization_elem = job_soup.find('div', {'data-automation-id': 'data_التخصص'})
            specialization = specialization_elem.text.strip() if specialization_elem else None

            experience_elem = job_soup.find('div', {'data-automation-id': 'data__المستوى_المهني'})
            experience = experience_elem.text.strip() if experience_elem else None

            all_jobs.append({
                'link': link,
                'title': title,
                'company_name': company_name,
                'date': date,
                'salary': salary,
                'career_level': career_level,
                'location': location,
                'num_of_vacancies': num_of_vacancies,
                'industry': industry,
                'description': description,
                'skills': skills,
                'remote': remote,
                'num_of_exp': num_of_exp,
                'residence_area': residence_area,
                'nationality': nationality,
                'sex': sex,
                'qualification': qualification,
                'age': age,
                'specialization': specialization,
                'experience': experience

            })
        time.sleep(1)
    print(f"\n✅ تم سحب {len(all_jobs)} وظيفة من {total_pages} صفحة.")
    return pd.DataFrame(all_jobs)

