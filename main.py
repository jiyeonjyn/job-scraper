from lib.indeed import get_jobs as get_indeed_jobs
from lib.saramin import get_jobs as get_saramin_jobs
from lib.save import save_to_csv

jobs = get_indeed_jobs(66) + get_saramin_jobs(33)
save_to_csv(jobs)