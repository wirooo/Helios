from bs4 import BeautifulSoup
import requests

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
joblisting = input()
joburl = "https://ca.indeed.com/jobs?q=" + joblisting.replace(" ", "+") + "&l=Waterloo%2C+ON"

for i in listofjobs(joburl):
    jobdata = {}
    jobdata['title'] = jobtitle(i)
    jobdata['location'] = joblocation(i)
    jobdata['description'] = jobdescription(i)
    jobdata['url'] = i
    jobs.append(jobdata)

print(jobs)
