from bs4 import BeautifulSoup
import requests

def indeedscrape(searchterm):
    def listofjobs(indeedurl):
        source = requests.get(indeedurl).text
        soup = BeautifulSoup(source, 'lxml')

        listoflinks = []

        for a in soup.find_all('a', href=True):
            if("vjs=3" in a['href']):
                listoflinks.append("https://indeed.com" + a['href'])

        # for i in listoflinks:
        #     print(i)

        return listoflinks

    # def jobdescription(pageurl):
    #     source = requests.get(pageurl).text
    #     soup = BeautifulSoup(source, 'lxml')
    #     description = soup.find(id="jobDescriptionText").text
    #     return description
    #
    # def jobtitle(pageurl):
    #     source = requests.get(pageurl).text
    #     soup = BeautifulSoup(source, 'lxml')
    #     title = soup.find('h3', attrs={'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
    #     return title

    def jobtitleanddescription(pageurl):
        source = requests.get(pageurl).text
        soup = BeautifulSoup(source, 'lxml')
        description = soup.find(id="jobDescriptionText").text
        title = soup.find('h3', attrs={'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
        answer = [title, description]
        return answer
        # print(answer)


    # def joblocation(pageurl):
    #     source = requests.get(pageurl).text
    #     soup = BeautifulSoup(source, 'lxml')
    #     div = soup.find('span', attrs={'class': "jobsearch-JobMetadataHeader-iconLabel"}).text
    #     # print(div)
    #     return div


    # ---------------------------------------------------------------------------------
    jobs = []
    # url = input()
    joburl = "https://ca.indeed.com/jobs?q=" + searchterm.replace(" ", "+") + "&l=Waterloo%2C+ON"
    # joburl = "https://ca.indeed.com/jobs?q=" + url.replace(" ", "+") + "&l=Waterloo%2C+ON"


    for i in listofjobs(joburl):
        jobdata = {}
        jobdata['title'] = jobtitleanddescription(i)[0]
        jobdata['description'] = jobtitleanddescription(i)[1]
        jobdata['url'] = i
        jobdata['platform'] = "indeed"
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
            jobdata["platform"] = "monster"
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