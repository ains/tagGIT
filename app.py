from flask import Flask, request, render_template
import json
import datetime
import os
import subprocess
import uuid

app = Flask(__name__)
GENERATED_REPO_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'repos')
OUTPUT_FILE = 'dates.txt'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create_repo():
    form_author = request.form['committerName']
    form_email = request.form['committerEmail']
    commit_email = '{} <{}>'.format(form_author, form_email)

    dates_json = request.form['dates']
    dates = [datetime.datetime.utcfromtimestamp(int(x)) for x in json.loads(dates_json)]

    repo_dir = os.path.join(GENERATED_REPO_DIR, str(uuid.uuid4()))
    os.mkdir(repo_dir)

    subprocess.call(['git', 'init'], cwd=repo_dir)
    for date in dates:
        date_str = date.strftime('%d-%m-%y')
        with open(os.path.join(repo_dir, OUTPUT_FILE), 'a') as f:
            f.write(date_str)

        subprocess.call(['git', 'add', OUTPUT_FILE], cwd=repo_dir)
        subprocess.call(
            ['git', 'commit', '-a', '--author', commit_email, '--date', date.isoformat(), '-m', date_str],
            cwd=repo_dir
        )

    return request.form['dates']


if __name__ == '__main__':
    app.run(debug=True)
