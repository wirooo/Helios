from flask import Flask, request, jsonify, render_template, redirect,url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

app.run()
