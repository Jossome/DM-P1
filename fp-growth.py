from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time

node_link = {}

class tree:
    def __init__(self, name, trace):
        self.name = name
        self.trace = trace
        self.count = 1
        self.children = {}
        
def traverse(T):
    if len(T.children) == 0:
        print(T.name, " : ", T.trace)
        return 
    else:
        print(T.name, " : ", T.trace)
        for each in T.children:
            print("Parent: ", T.name)
            traverse(T.children[each])
        print("===========")

# not quite the name, because we return all the freq.
def find_freq_1_itemset(D):
    tmp = []
    for col in D.columns:
        col_cnt = D[col].value_counts()
        col_cnt.index = [(col, x) for x in col_cnt.index]
        tmp.append(col_cnt)
    return pd.concat(tmp)

def insert_tree(row, T):
    if len(row) == 0: return T
    
    if row[0] not in T.children:
        T.children[row[0]] = tree(row[0], T.trace + "->" + str(T.name))
        tag = T.children[row[0]] # Make a reference
        try:
            node_link[T.children[row[0]].name].append(tag)
        except Exception:
            node_link[T.children[row[0]].name] = [tag]
    else:
        T.children[row[0]].count += 1
        
    insert_tree(row[1:], T.children[row[0]])

def get_CFP(item):
    for each in item:
        return
    
def fp_gen(CPB, CFP):
    return


def fp_growth(D, min_sup):
    sup_cnt = find_freq_1_itemset(D)
    sort_key = {name: sup_cnt[name] for name in sup_cnt.index} 
    fp_tree = tree("null", "")
    for _, t in D.iterrows():
        row = sorted(zip(t.index, list(t)), key = lambda x: sort_key[x], reverse = True)
        insert_tree(row, fp_tree)

    #----------fp-tree constructed-----------------
    freq1 = sorted([x for x in sup_cnt.index if sup_cnt[x] >= min_sup], key = lambda x: sort_key[x])
    L = freq1[:]
    for item in freq1[:-1]:
        CPB = [(x.trace.split('->')[2:], x.count) for x in node_link[item]]
        print(CPB)
        CFP = get_CFP(item)
        FPG = fp_gen(CPB, CFP)
        L += FPG
    return L


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    ttt = fp_growth(df, len(df) * 0.8)
    #traverse(ttt)
    print("Runtime:", round(time.time() - start, 2), "seconds.")
