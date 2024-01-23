import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


class LinkedInScraper():
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com"
        self.url = "https://www.linkedin.com/jobs/search?keywords=software%20summer%20intern&location=United%20Kingdom&geoId=101165590&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"


    def parse_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Role
        role_tag = soup.find('h1', class_='top-card-layout__title')
        role = role_tag.get_text(strip=True) if role_tag else None

        # Company Name
        company_name_tag = soup.find('a', class_='topcard__org-name-link')
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

        # Number of Applicants
        num_applicants_tag = soup.find('figcaption', class_='num-applicants__caption')
        if not num_applicants_tag:
            num_applicants_tag = soup.find('span', class_='num-applicants__caption')
        num_applicants = num_applicants_tag.get_text(strip=True) if num_applicants_tag else None

        return (role, company_name, num_applicants)

    def get_job_links(self, soup):
        job_links = []
        for link in soup.find_all('a', class_="base-card__full-link"):
            job_links.append(link['href'])
        
        return job_links
    
    def make_hyperlink(self, name, link):
        return '=HYPERLINK("%s", "%s")' % (link, name)
    
    def scrape(self):
        current_url = self.url
        original_url = self.url

        job_links = []
        roles = []
        companies = []
        num_applicants = []
        page = 1
        
        while current_url:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            job_links = self.get_job_links(soup)

            for job_link in job_links:
                role, company_name, num_applicant = self.parse_page(job_link)
                roles.append((role, job_link))
                companies.append(company_name)
                num_applicants.append(num_applicant)
                time.sleep(1)
            
            break
            # current_url = self.get_next_page(soup)
        
        df = pd.DataFrame({'Company': companies, 'Role': roles, 'Number of Applicants': num_applicants})
        df['Role'] = df.apply(lambda x: self.make_hyperlink(x['Role'][0], x['Role'][1]), axis=1)
        df.to_excel('linkedin.xlsx', index=False)
