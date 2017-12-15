from radon.metrics import mi_visit
from radon.complexity import cc_visit, cc_rank
from pygit2 import Repository, clone_repository
import requests, json
from time import time
from gitrepo import set_repo, get_commits




def compute_complexity(source) #function to calculate codecomplexity
    result =[]
    blocks = cc_visit(source)
    for func in blocks:
        result.append(func.name+"- CC Rank:"+cc_rank(func.complexity))
    return result

def tot_data(tree, repo):
      datas = []
    for x in tree:
        if ".py" in x.name:
             datas.append(x)
        if "." not in x.name:
           if x.type == 'tree':
                new_tree = repo.get(x.id)
                datas += (tot_data(new_tree, repo))
    return datas

