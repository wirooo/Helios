from bs4 import BeautifulSoup
import requests

def indeedscrape(searchterm):
    def listofjobs(indeedurl):
        source = requests.get(indeedurl).text
        soup = BeautifulSoup(source, 'lxml')

        listoflinks = []

        for a in soup.find_all('a', href=True):
            if("vjs=3" in a['href']):
                listoflinks.append("https://www.indeed.com" + a['href'])

        return listoflinks

    def jobtitleanddescription(pageurl):
        source = requests.get(pageurl).text
        soup = BeautifulSoup(source, 'lxml')
        description = soup.find(id="jobDescriptionText").text
        title = soup.find('h3', attrs={'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
        company = soup.find('div', attrs={'class': 'jobsearch-CompanyInfoWithoutHeaderImage'}).text
        answer = [title, description, company]
        return answer
        # print(answer)

    # ---------------------------------------------------------------------------------
    jobs = []
    joburl = "https://ca.indeed.com/jobs?q=" + searchterm.replace(" ", "+") + "&l=Waterloo%2C+ON"

    for i in listofjobs(joburl):
        jobdata = {}
        jobresults = jobtitleanddescription(i)
        jobdata['title'] = jobresults[0]
        jobdata['description'] = jobresults[1]
        jobdata['url'] = i
        jobdata['platform'] = "Indeed"
        jobdata['company'] = jobresults[2]
        jobs.append(jobdata)

    return jobs

def monsterscrape(searchterm, city):
    searchterm = searchterm.replace(" ", "-")
    city = city.replace(" ", "-")
    request_url = "https://www.monster.ca/jobs/search/?q=" + searchterm + "&where=" + city + "__2C-ON"
    response = requests.get(request_url, timeout=5)
    content = BeautifulSoup(response.content, "lxml")
    links = content.findAll('a', href=True)
    listings = []
    for a in links:
        if "job-openings.monster.ca" in a["href"]:
            listings.append(a['href'])
    jobs = []
    for job_url in listings:
        jobdata = {}
        jobresponse = requests.get(job_url, timeout=5)
        jobcontent = BeautifulSoup(jobresponse.content, "lxml")
        description = jobcontent.find("div", attrs={"id": "JobBody"})
        if description is None:
            description = jobcontent.find("div", attrs={"id": "JobDescription"})
        if description is not None:
            description = description.text
            jobdata["description"] = description
            jobdata["url"] = job_url
            title = jobcontent.find("h1", attrs={"class": "title"}).text
            jobdata["platform"] = "Monster"
            if " at " in title:
                title = title.split(" at ")
                jobdata["title"] = title[0]
                jobdata["company"] = title[1].rstrip("\n")
                jobs.append(jobdata)
            elif " from " in title:
                title = title.split(" from ")
                jobdata["title"] = title[0]
                jobdata["company"] = title[1].rstrip("\n")
                jobs.append(jobdata)
            else:
                jobdata["title"] = title
                jobs.append(jobdata)
    return jobs