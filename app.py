# pip install flask
from flask import Flask, jsonify, render_template
from fetch_data import fetch_data


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    df = fetch_data()
    return jsonify(df)


if __name__ == '__main__':
    app.run(debug=False)