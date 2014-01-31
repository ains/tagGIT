from flask import Flask, request, render_template
import json
import datetime
import os
import subprocess
import uuid
import shutil

app = Flask(__name__)

GENERATED_REPO_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'repos')
ARCHIVE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'repos')
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
    dates = json.loads(dates_json)

    #Create and initialize git repo
    repo_name = str(uuid.uuid4())
    repo_dir = os.path.join(GENERATED_REPO_DIR, repo_name)
    os.mkdir(repo_dir)
    subprocess.call(['git', 'init'], cwd=repo_dir)

    #Add commits for each date
    for (unix_time, strength) in dates.items():
        date = datetime.datetime.utcfromtimestamp(int(unix_time))

        #Stops huge repos being created by a rouge user
        commit_count = min(strength, 4)

        #Increase maximum commit count to 5 to get full colour range from Github
        if commit_count == 4:
            commit_count += 1

        #Commit given number of times for correct colour strength
        for i in range(0, commit_count):
            with open(os.path.join(repo_dir, OUTPUT_FILE), 'a') as f:
                f.write('.')

            subprocess.call(['git', 'add', OUTPUT_FILE], cwd=repo_dir)
            subprocess.call(
                ['git', 'commit', '-a', '--author', commit_email, '--date', date.isoformat(), '-m', '.'],
                cwd=repo_dir
            )

    #Create archive of generated repository
    archive_filename = '{}.tar'.format(repo_name)
    archive_file = os.path.join(ARCHIVE_DIR, archive_filename)
    subprocess.call(['tar', 'cf', archive_file, '-C', GENERATED_REPO_DIR, repo_name])

    #Cleanup and delete repo
    shutil.rmtree(repo_dir)

    return archive_filename


if __name__ == '__main__':
    app.run(debug=True)
