from flask import Flask, request, render_template
import json
import datetime
import os
import subprocess
import uuid

app = Flask(__name__)
REPO_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'repos')
AUTHOR = "Git Gen <gitgen@dispostable.com>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_repo():
    dates_json = request.form['dates']
    dates = [datetime.datetime.utcfromtimestamp(int(x)) for x in json.loads(dates_json)]

    repo_dir = os.path.join(REPO_DIR, str(uuid.uuid4()))
    os.mkdir(repo_dir)
    os.chdir(repo_dir)
    subprocess.call(["git", "init"])
    for date in dates:
        date_str = date.strftime("%d-%m-%y")
        with open('test.txt','a') as f:
            f.write(date_str)

        subprocess.call(["git", "add", "test.txt"])
        subprocess.call(["git", "commit", "-a", "--author", AUTHOR, "--date", date.isoformat(), "-m", date_str])

    return request.form['dates']

if __name__ == '__main__':
    app.run()
