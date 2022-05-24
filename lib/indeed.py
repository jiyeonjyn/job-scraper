# https://docs.python-requests.org/en/master/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from bs4 import BeautifulSoup

QUERY = "python"
BASE_URL = "https://kr.indeed.com"


def get_page_html(page):
    html_doc = requests.get(
        f"{BASE_URL}/jobs?q={QUERY}&start={page*10}")
    html_text = BeautifulSoup(html_doc.text, 'html.parser')
    return html_text


def extract_job(html):
    # title, company, location, link
    title_anchor = html.find("a")
    title = title_anchor.string
    company = html.find("span", {"class": "companyName"})
    if company :
        company = company.string
    else :
        company = ""
    location = html.find("div", {"class": "companyLocation"}).string
    a_href = title_anchor["href"]
    link = f"{BASE_URL}{a_href}"
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }


def get_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scraping Indeed: Page {page+1}")
        page_html = get_page_html(page)
        job_list_html = page_html.find_all("td", {"class": "resultContent"})
        for job_html in job_list_html:
            job = extract_job(job_html)
            jobs.append(job)
    return jobs
