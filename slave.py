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
