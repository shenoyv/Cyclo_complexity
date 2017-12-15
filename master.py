from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository

app = Flask(__name__)
def set_repo():
    try:
        repos = Repository('~/repo')
    except:
           url ='https://github.com/EntilZha/PyFunctional.git'
           path = '~/repo'
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

@app.route('/executiontime', methods=['POST'])
def execution_time():
     start_time = request.json
     end_time = time() - int(start_time['start_time'])
     return jsonify({'executiontime': end_time})

@app.route('/results', methods=['POST','GET'])
def store_result():
    global executiontime_list, execution_time, result
    executiontime_list = []
    if request.method == 'POST':
        result = request.json
        executiontime_list = result['executiontime']
        execution_time = sum(executiontime_list)
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})
    else:
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})

def server_shutdown():
    func = request.environ.get('server shutdown')
    if func is None:
        raise RuntimeError('Not running with the Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    server_shutdown()
    return jsonify({'message' : 'server is shutting down'})


if __name__ == '__main__':
        task_2 = 0
        app.run(threaded=True, debug=True)