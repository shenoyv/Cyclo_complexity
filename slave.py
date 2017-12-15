from radon.metrics import mi_visit
from radon.complexity import cc_visit, cc_rank
from pygit2 import Repository, clone_repository
import requests, json
from time import time


# pulls repo from url and stores clone
def set_repo():
    try:
        repo = Repository('~/repo')
    except:
        repo_url = 'https://github.com/EntilZha/PyFunctional.git'
        repo_path = '~/repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

# walk through commits in the given repo and store in list
def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits

#function to calculate codecomplexity
def compute_complexity(source):
    result =[]
    blocks = cc_visit(source)
    for func in blocks:
        result.append(func.name+"- CC Rank:"+cc_rank(func.complexity))
    return result

def tot_data(tree, repo):
    datas = []
    for entry in tree:
        if ".py" in entry.name:
            datas.append(entry)
        if "." not in entry.name:
           if entry.type == 'tree':
                new_tree = repo.get(entry.id)
                datas += (tot_data(new_tree, repo))
    return datas

def extract_files(sources):
    files = []
    for source in sources:
        files.append(repo[source.id].data.decode("utf-8"))
    return files

def tot_work(repo):
    post = requests.post('http://127.0.0.1:5000/executiontime', json={'start_time': time()})
    response = requests.get('http://127.0.0.1:5000/work', params={'key': 'value'})
    while response.status_code == 200:
        response.encoding = 'utf-8'
        json_file = response.json()
        post.encoding = 'utf-8'
        post_file = post.json()
        executiontime = post_file['executiontime']
        id = json_file['id']
        tree = repo.get(json_file['commit']).tree
        sources = tot_data(tree, repo)
        files = extract_files(sources)
        return files, id, executiontime

def num_work(work):
    results = []
    for file in work:
        try:
            results.append(compute_complexity(file))
        except:
            results.append('')
    return results

# post results to the url
def send_results(result):
    requests.post('http://127.0.0.1:5000/results', json=result,  params={'key': 'value'})
    response = requests.get('http://127.0.0.1:5000/results',  params={'key': 'value'})
    return response

if __name__ == '__main__':
    bool = True
    executiontime_list = []
    result_list = []
    id = 0
    while bool: #run until work is finished
        repo = set_repo()
        commits = get_commits(repo)
        try:
            #while id < len(commits):
            work, id, executiontime = tot_work(repo)
            print(id)
            result = num_work(work)
            result_list.append(result)
            executiontime_list.append(executiontime)
        except:
            bool = False
            print("Process Terminated")
    report = {'Result': result_list, 'executiontime': executiontime_list}
    response = send_results(report)
    message = response.json()
    print("complexity_score", message['complexity_score'])
    print("execution_time", message['execution_time'])
