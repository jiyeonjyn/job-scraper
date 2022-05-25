# format code in vscode : shift + option(alt) + F

from flask import Flask, render_template, request, redirect, send_file
from lib.indeed import get_jobs as get_indeed_jobs
from lib.saramin import get_jobs as get_saramin_jobs
from lib.save import save_to_csv
import time
import re

app = Flask(__name__)
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
    result_num = format(len(jobs), ",")
    total_time = f"{time.time() - start_time:.5f}"
    return render_template("report.html", search_text=query, result_num=result_num, time=total_time, jobs=jobs)


@app.route("/export")
def export():
    try:
        query = request.args.get('query')
        if not query:
            raise Exception()
        query = query.lower()
        jobs = jobDB.get(query)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        char_extract = re.compile('\w+').findall(query)
        char_only_filename = ''.join(char_extract)
        return send_file("jobs.csv", attachment_filename=f"{char_only_filename}_jobs.csv", as_attachment=True)
    except:
        return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
