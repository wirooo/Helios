from flask import Flask, request, render_template, redirect, url_for
import resume_scraper
import WebScraper

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
            print(jobtitle)
            save_name = "resumes/"+resume.filename
            resume.save(save_name)
            keywords = resume_scraper.match_keywords(save_name)
            print(keywords)
            return redirect(url_for("search"))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

app.run()
