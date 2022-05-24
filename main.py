# format code in vscode : shift + option + F

from flask import Flask, render_template, request, redirect
from lib.indeed import get_jobs as get_indeed_jobs
from lib.saramin import get_jobs as get_saramin_jobs
# from lib.save import save_to_csv
import time

app = Flask("JobScraper")
jobDB = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/report")
def report():
    start_time = time.time()
    query = request.args.get('query')
    if query:
        query = query.lower()  # 대문자를 입력해도 소문자로 바꿈
    else:
        return redirect("/")
    fromDB = jobDB.get(query)
    if fromDB:
        jobs = fromDB
    else:
        jobs = get_indeed_jobs(70, query) + get_saramin_jobs(40, query)
        jobDB[query] = jobs
    result_num = len(jobs)
    total_time = f"{time.time() - start_time:.5f}"
    return render_template("report.html", search_text=query, result_num=result_num, time=total_time, jobs=jobs)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
