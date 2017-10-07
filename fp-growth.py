from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time

class tree:
    def __init__(self， name, children = []):
        self.name = name
        self.count = 1
        self.children = list(children)
    

def fp_growth(tree, D):
    return L

def tree_gen(D):
    sup_cnt = pd.Series(reduce((lambda x, y: x + y), D)).value_counts()
    sort_key = {name: i for i, name in enumerate(sup_cnt.index)}  #Generating the key is too costy
    root = {"node": None, "count": 0, "child": []}
    for t in D:
        this = sorted(t, key = sort_key)
        root["child"].append()
        
    return sort_key
    

if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df = df.values.tolist()

    print(tree_gen(df))
    
#    L = fp_growth(tree_gen(df), None) 
#    print(reduce((lambda x, y: x + y), L))

    print("Runtime:", round(time.time() - start, 2), "seconds.")