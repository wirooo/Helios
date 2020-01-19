from bs4 import BeautifulSoup
import requests

def indeedscrape(searchterm):
    def listofjobs(indeedurl):
        # 'https://ca.indeed.com/jobs?q=software+developer&l=Waterloo%2C+ON'
        source = requests.get(indeedurl).text
        soup = BeautifulSoup(source, 'lxml')

        listoflinks = []

        for a in soup.find_all('a', href=True):
            if("vjs=3" in a['href']):
                listoflinks.append("https://indeed.com" + a['href'])

        return listoflinks

        # for i in listoflinks:
        #     print(i)

    def jobdescription(pageurl):
        source = requests.get(pageurl).text
        soup = BeautifulSoup(source, 'lxml')
        div = soup.find(id="jobDescriptionText").text
        return div

    def jobtitle(pageurl):
        source = requests.get(pageurl).text
        soup = BeautifulSoup(source, 'lxml')
        div = soup.find('h3', attrs={'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
        return div

    def joblocation(pageurl):
        source = requests.get(pageurl).text
        soup = BeautifulSoup(source, 'lxml')
        div = soup.find('div', attrs={'class': "icl-u-lg-mr--sm icl-u-xs-mr--xs"}).text
        return div

    # ---------------------------------------------------------------------------------
    jobs = []
    joburl = "https://ca.indeed.com/jobs?q=" + searchterm.replace(" ", "+") + "&l=Waterloo%2C+ON"

    for i in listofjobs(joburl):
        jobdata = {}
        jobdata['title'] = jobtitle(i)
        jobdata['location'] = joblocation(i)
        jobdata['description'] = jobdescription(i)
        jobdata['url'] = i
        jobs.append(jobdata)

    return jobs

def monsterscrape(searchterm, city):
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
