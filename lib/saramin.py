import requests
from bs4 import BeautifulSoup
import re

QUERY = "python"
BASE_URL = "https://www.saramin.co.kr/zf_user"


def get_page_html(page):
    html_doc = requests.get(
        f"{BASE_URL}/search?searchword={QUERY}&recruitPage={page+1}&recruitPageCount=100"
    )
    html_text = BeautifulSoup(html_doc.text, 'html.parser')
    return html_text


def extract_job(html):
    # title, company, location, link
    title_anchor = html.find("h2", {"class": "job_tit"}).find("a")
    title = title_anchor["title"]
    company = html.find("div", {"class": "area_corp"}).find("a").string.strip()
    location = html.find("div", {
        "class": "job_condition"
    }).find("span").get_text(" ", strip=True)
    rec_idx = re.compile('rec_idx=(\d+)').findall(title_anchor["href"])[0]
    link = f"{BASE_URL}/jobs/view?rec_idx={rec_idx}"
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }


def get_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scraping Saramin: Page {page+1}")
        page_html = get_page_html(page)
        job_list_html = page_html.find_all("div", {"class": "item_recruit"})
        for job_html in job_list_html:
            job = extract_job(job_html)
            jobs.append(job)
    return jobs
