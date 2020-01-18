from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

app.run()
