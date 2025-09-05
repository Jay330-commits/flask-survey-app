from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
from filelock import FileLock

app = Flask(__name__)

CSV_FILE = "response.csv"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    gender = request.form.get('gender')
    services = request.form.getlist('services')  # returns a list
    feedback = request.form.get('feedback')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append to CSV
    lock = FileLock("responses.csv.lock")
    with lock:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, name, gender, ";".join(services), feedback])
            
    return "<h3>Thank you for submitting the survey!</h3><p><a href='/'>Submit another</a></p>"

if __name__ == '__main__':
    app.run()
