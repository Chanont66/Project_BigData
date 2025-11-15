# pip install flask
from flask import Flask, render_template
from fetch_data import fetch_data


app = Flask(__name__)

@app.route('/')
def index():
    result = fetch_data()

    return render_template('index.html', data=result)

