from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository


def set_repo():
    try:
        repos = Repository('./repo')
    except:
           url ='https://github.com/shenoyv/Distributed_file_system.git'
           path = './repo'
           repos = clone_repository(url, path)
    return repos

def tot_commits(repo):
    num_commits = []
    for commit in repo.walk(repo.head.target):
        num_commits.append(repo.get(commit.id))
    return num_commits


@app.route('/work' , methods=['GET'])
def  do_work():
    repo = set_repo()
    commits = tot_commits(repo)
    global task_2
    if task_2 < len(commits):
        commit_hash = commits[task_2]
        task_2 += 1
        return jsonify({'commit': str(commit_hash.id), 'id': task_2})
    else:
        return "zero Work"

    if __name__ == '__main__':
        task_2 = 0
        app.run(threaded=True, debug=True)