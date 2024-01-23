import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


class BrightNetworkScraper():

    def __init__(self):
        self.base_url = "https://www.brightnetwork.co.uk"
        self.url = "https://www.brightnetwork.co.uk/search/?content_types=jobs&career_path_sectors=Technology+%26+IT+Infrastructure&job_types=Internship&sort_by=recent"


    def parse_page(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        

        # Job Description
        job_section = soup.find('section', class_='section__description')
        job_description = job_section.get_text(strip=True) if job_section else None


        # Company Name
        company_name_tag = soup.find('div', class_='field-related-company')
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

        # Deadline
        deadline_tag = soup.find('div', class_='field-deadline')
        deadline = deadline_tag.get_text(strip=True) if deadline_tag else None
        if deadline != "Rolling deadline":
            deadline = deadline.split("DEADLINE ")[1]
        

        # Role
        role_tag = soup.find('h1')
        role = role_tag.get_text(strip=True) if role_tag else None

        return (job_description, deadline, company_name, role)


    def get_next_page(self, soup):
        pagination_container = soup.find('div', class_='pagination-container')
        if pagination_container:
            next_page_tag = pagination_container.find_all('a')[-1]
            if "Next" in next_page_tag.get_text(strip=True) and next_page_tag.has_attr('href'):
                next_page_url = next_page_tag['href']
                return f"{self.base_url}{next_page_url}"
            
    def get_job_links(self, soup):
        job_links = []
        for link in soup.find_all('a', class_="read-more-arrow"):
            job_links.append(f"{self.base_url}{link['href']}")
        
        return job_links

    # Creates Excel hyperlinks
    def make_hyperlink(self, name, link):
        return '=HYPERLINK("%s", "%s")' % (link, name)

    def scrape(self):
        current_url = self.url
        original_url = self.base_url
        base_url = original_url.split("/search")[0]

        # Scrape job listings from all pages
        job_texts = []
        companies=[]
        roles=[]
        deadlines=[]
        page = 1

        while current_url:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'lxml')

            job_links = self.get_job_links(soup)

            for job_link in job_links:
            #storing job descriptions
                page_parts = self.parse_page(job_link)
                job_texts.append(page_parts[0])
                roles.append((page_parts[3], job_link))
                deadlines.append(page_parts[1])
                companies.append(page_parts[2])

                time.sleep(1)  # Add a delay between requests to avoid overloading the server
            
            print(f"Scraped page {page}")

            current_url = self.get_next_page(soup)
            
            page += 1
            time.sleep(1)

        # Create dataframe and export to Excel
        df = pd.DataFrame({'Company': companies, 'Role': roles, 'Deadline': deadlines})
        df['Role'] = df['Role'].apply(lambda x: self.make_hyperlink(x[0], x[1]))
        df.to_excel("bright_network.xlsx", index=False)