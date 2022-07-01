import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kr.indeed.com"


def get_page_html(page, query):
    html_doc = requests.get(f"{BASE_URL}/jobs?q={query}&start={page*10}")
    html_text = BeautifulSoup(html_doc.text, 'html.parser')
    return html_text


def extract_job(html):
    # title, company, location, link
    title_anchor = html.find("a")
    title = title_anchor.string
    company = html.find("span", {"class": "companyName"})
    if company:
        company = company.string
    else:
        company = ""
    location = html.find("div", {"class": "companyLocation"}).string
    jk = title_anchor["data-jk"]
    link = f"{BASE_URL}/viewjob?jk={jk}"
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }


def get_jobs(max_page, query):
    jobs = []
    for page in range(max_page):
        print(f"Scraping Indeed: Page {page+1}")
        page_html = get_page_html(page, query)
        job_list_html = page_html.find_all("td", {"class": "resultContent"})
        if len(job_list_html) == 0:
            break
        for job_html in job_list_html:
            job = extract_job(job_html)
            jobs.append(job)
    return jobs
