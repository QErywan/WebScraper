""" Job Board Aggregator """


# LinkedIn

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import torch
from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time


# Bright Network

base_url = "https://www.brightnetwork.co.uk/search/?content_types=jobs&career_path_sectors=Technology+%26+IT+Infrastructure&job_types=Internship&sort_by=recent"


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    

    # Job Description
    job_section = soup.find('div', class_='row g-0 result-row-with-calendar ps-3 p-lg-0 search-result-row')
    job_description = job_section.find('div', class_='col-10 col-lg-8 description')

    # Company Name
    company_name_tag = soup.find('a', href=re.compile(r"/graduate-employer-company/"))
    company_name = company_name_tag.get_text(strip=True) if company_name_tag else None

    # Deadline
    deadline_tag = soup.find('div', class_='d-none d-lg-block date-container')
    deadline = deadline_tag.get_text(strip=True) if deadline_tag else None

    # Role
    role_tag = soup.find('h3', class_='h3 pt-2 pt-lg-3')
    role = role_tag.get_text(strip=True) if role_tag else None

    return job_description, company_name, deadline, role

def get_next_page(soup):
    pagination_container = soup.find('div', class_='pagination-container')
    if pagination_container:
        next_page_tag = pagination_container.find_all('a')[-1]
        if "Next" in next_page_tag.get_text(strip=True) and next_page_tag['href'] != 'None':
            next_page_url = next_page_tag.find('a')['href']
            return f"{base_url}{next_page_url['href']}"
        
def get_job_links(soup):
    job_links = []
    print(soup.find_all('a', href=re.compile(r"/graduate-jobs/")))
    for link in soup.find_all('a', href=re.compile(r"/graduate-jobs/")):

        job_links.append(f"{base_url}{link['href']}")


current_url = base_url
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
    soup = BeautifulSoup(response.content, 'html.parser')

    job_links = get_job_links(soup)

    for job_link in job_links:
      #storing job descriptions
        job_texts.append(parse_page(job_link)[0])
        roles.append(parse_page(job_link)[3])
        deadlines.append(parse_page(job_link)[2])
        companies.append(parse_page(job_link)[1])
        links.append(job_link)
      
        time.sleep(1)  # Add a delay between requests to avoid overloading the server

    print(f"Scraped page {page}")

    current_url = get_next_page(soup)
    
    page += 1
    time.sleep(1)  # Add a delay between requests to avoid overloading the server

final_df = pd.DataFrame({'Job Description': job_texts, 'URL': links,'Company':companies,'Role':roles,'Deadline':deadlines})