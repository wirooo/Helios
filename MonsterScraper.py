from bs4 import BeautifulSoup
import requests

def scrape(searchterm, city):
    searchterm = searchterm.replace(" ", "-")
    city = city.replace(" ", "-")
    request_url = "https://www.monster.ca/jobs/search/?q=" + searchterm + "&where=" + city + "__2C-ON"
    response = requests.get(request_url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    links = content.findAll('a', href=True)
    listings = []
    for a in links:
        if "job-openings.monster.ca" in a["href"]:
            listings.append(a['href'])
    jobs = []
    for job_url in listings:
        jobdata = {}
        jobresponse = requests.get(job_url, timeout=5)
        jobcontent = BeautifulSoup(jobresponse.content, "html.parser")
        description = jobcontent.find("div", attrs={"id": "JobDescription"}).text
        jobdata["description"] = description
        jobdata["url"] = job_url
        title = jobcontent.find("h1", attrs={"class": "title"}).text.split(" at ")
        jobdata["title"] = title[0]
        jobdata["company"] = title[1].rstrip("\n")
        jobs.append(jobdata)
    return jobs

if __name__ == "__main__":
    scrape("Software Engineer", "Toronto")