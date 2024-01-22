""" Job Board Aggregator """


# LinkedIn

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup, Comment
import torch
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time


# Bright Network
base_url = "https://www.brightnetwork.co.uk"
url = "https://www.brightnetwork.co.uk/search/?offset=30&content_types=jobs&job_types=Internship&sort_by=recent"


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    

    # Job Description
    job_section = soup.find('section', class_='section__description')
    job_description = job_section.get_text(strip=True) if job_section else None


    # Company Name
    company_name_tag = soup.find('a', href=re.compile(r"/graduate-employer-company/"))
    company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

    # Deadline
    # comment = soup.find(text=lambda text: isinstance(text, Comment) and 'Deadline' in text)
    # print(comment)
    # deadline_tag = comment.find_next('div')
    # deadline = deadline_tag.get_text(strip=True) if deadline_tag else None
    

    # Role
    role_tag = soup.find('h1')
    role = role_tag.get_text(strip=True) if role_tag else None

    return job_description, company_name, role
    # return company_name, role


def get_next_page(soup):
    pagination_container = soup.find('div', class_='pagination-container')
    if pagination_container:
        next_page_tag = pagination_container.find_all('a')[-1]
        if "Next" in next_page_tag.get_text(strip=True) and next_page_tag['href'] != 'None':
            next_page_url = next_page_tag.find('a')['href']
            return f"{base_url}{next_page_url['href']}"
        
def get_job_links(soup):
    job_links = []
    # print(soup.find_all('a', class_="read-more-arrow"))
    for link in soup.find_all('a', class_="read-more-arrow"):
        job_links.append(f"{base_url}{link['href']}")
    
    return job_links


current_url = url
original_url = base_url
base_url = original_url.split("/search")[0]

# Scrape job listings from all pages
job_texts = []
companies=[]
roles=[]
links=[]
deadlines=[]
page = 1

while current_url:
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'lxml')

    job_links = get_job_links(soup)

    for job_link in job_links:
      #storing job descriptions
        job_texts.append(parse_page(job_link)[0])
        roles.append(parse_page(job_link)[2])
        # deadlines.append(parse_page(job_link)[2])
        companies.append(parse_page(job_link)[1])
        links.append(job_link)
      
        time.sleep(1)  # Add a delay between requests to avoid overloading the server
    
    current_url = get_next_page(soup)


df = pd.DataFrame({'Company': companies, 'Role': roles, 'Link': links, 'Job Description': job_texts})
df.to_excel("bright_network.xlsx")


# print(parse_page("https://www.brightnetwork.co.uk/graduate-jobs/jacobs/project-support-summer-internship-bristol-2024?search_id=2b969117f6450052b7978ae982c05a65&search_position=6"))