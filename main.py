from flask import Flask, request, render_template, redirect, url_for, jsonify
import resume_scraper
from WebScraper import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        if request.files:
            resume = request.files["resume"]
            jobtitle = request.form["jobtitle"]
            save_name = "resumes/"+resume.filename
            resume.save(save_name)
            keywords = resume_scraper.match_keywords(save_name)
            return jsonify(runsearches(keywords, jobtitle))

def findmatches(jobs, keywords):
    matches=[]
    for job in jobs:
        suitability = 0
        for kwd in keywords:
            if kwd in job["description"]:
                suitability += 1
        if(suitability > 0):
            newmatch = {}
            for key in job:
                if key != "description":
                    newmatch[key] = job[key]
            newmatch["suitability"] = suitability
            matches.append(newmatch)

    return matches

def runsearches(keywords, jobtitle):
    print("finding jobs")
    # indeedjobs = indeedscrape(jobtitle)
    monsterjobs = monsterscrape(jobtitle, "Toronto")
    print("matching jobs")
    # indeedmatches = findmatches(indeedjobs, keywords)
    monstermatches = findmatches(monsterjobs, keywords)
    # return indeedmatches + monstermatches
    print("finished matching")
    return monstermatches


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

app.run()
