# pip install flask
# Flask คือ เฟรมเวิร์ก
# render_template ฟังก์ชันการแสดงผล
from flask import Flask, render_template

# ไว้ดึงข้อมูล
from fetch_data import fetch_data_ListTuple, plot


app = Flask(__name__)

@app.route('/')
def index():
    df = fetch_data_ListTuple()
    return render_template('index.html', data=df)


@app.route('/graph')
def graph():
    return render_template('graph.html' ,data=plot())


if __name__ == '__main__':
    app.run(debug=False)

# python app.py