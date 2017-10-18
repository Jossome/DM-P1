from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time
from copy import deepcopy

class tree:
    def __init__(self, name, trace):
        self.name = name    #the name of item
        self.trace = trace  #the prefix path
        self.count = 1      #the count on this node
        self.children = {}  #the children
        
def traverse(T):
    if len(T.children) == 0:
        print(T.name, " : ", T.count, T.trace)
        return 
    else:
        print(T.name, " : ", T.count, T.trace)
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

def insert_tree(row, T, node_link):
    if len(row) == 0: return T, node_link
    
    if row[0] not in T.children:
        T.children[row[0]] = tree(row[0], T.trace + "->" + str(T.name))
        tag = T.children[row[0]] # Make a reference
        try:
            node_link[T.children[row[0]].name].append(tag)
        except Exception:
            node_link[T.children[row[0]].name] = [tag]
    else:
        T.children[row[0]].count += 1
        
    return insert_tree(row[1:], T.children[row[0]], node_link), node_link

def tree_gen(D, min_sup, sort_key):
    node_link = {}
    fp_tree = tree("null", "")
    for _, t in D.iterrows():
        row = sorted(zip(t.index, list(t)), key = lambda x: sort_key[x], reverse = True)
        insert_tree(row, fp_tree, node_link)
    return fp_tree, node_link


def have_single_path(T):
    tmp = T
    while 1:
        if len(tmp.children) > 1: return False, tmp.name
        elif len(tmp.children) == 1: tmp = tmp.children[list(tmp.children.keys())[0]]
        else: return True, tmp.name
    #return True

def insert_CFP(row, T, node_link, cnt):
    if len(row) == 0: return T, node_link
    
    if row[0] not in T.children:
        T.children[row[0]] = tree(row[0], T.trace + "->" + str(T.name))
        tag = T.children[row[0]] # Make a reference
        T.children[row[0]].count = cnt
        try:
            node_link[T.children[row[0]].name].append(tag)
        except Exception:
            node_link[T.children[row[0]].name] = [tag]
    else:
        T.children[row[0]].count += cnt
        
    return insert_CFP(row[1:], T.children[row[0]], node_link, cnt), node_link

def get_CFP(CPB, min_sup):
    node_link = {}
    CFP = tree("null", "")
    for each in CPB:
        #print(each)
        row = [eval(x) for x in each[0].split('->')]
        insert_CFP(row, CFP, node_link, each[1])
    return CFP, node_link

def recursive(freq1, node_link, min_sup, first = False):
    res = []

    if len(freq1) <= 1:
        res.append(tuple(freq1))
    else:
        for item in freq1[:-1]:
            CPB = [(x.trace[8:], x.count) for x in node_link[item] if x.trace != '->null']
            CFP, local_link = get_CFP(CPB, min_sup)
            have, name = have_single_path(CFP)
            
            if have:
                res.append((name,))
            
            #local de sup_cnt
            local_cnt = [(each, reduce((lambda x, y: x + y), [i.count for i in local_link[each]])) for each in local_link]
            #up is right
            #down dont know what it is.
            
            local_key = {name: cnt for name, cnt in local_cnt}
            local_freq = sorted([x[0] for x in local_cnt if x[1] >= min_sup], key = lambda x: local_key[x])
            tmp = recursive(local_freq, local_link, min_sup)
            if len(tmp) == 0:
                res.append((item,))
            else: 
                for each in tmp:
                    res.append((item,) + each) 
    
    for i in range(len(res)):
        res[i] = tuple(sorted(res[i], key = str))
    
    return res
 
def fp_growth(df, min_sup):
    sup_cnt = find_freq_1_itemset(df)
    sort_key = {name: sup_cnt[name] for name in sup_cnt.index}
    fp_tree, node_link = tree_gen(df, min_sup, sort_key)
    freq1 = sorted([x for x in sup_cnt.index if sup_cnt[x] >= min_sup], key = lambda x: sort_key[x])
    L = [(x,) for x in freq1]
    L += recursive(freq1, node_link, min_sup, first = True)
    return L


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    min_sup = len(df) * 0.6
    fp = set(fp_growth(df, min_sup))
    print(len(fp))
    
    '''
    #if l and res have the same length, then all the frequent pattern generated are correct.
    
    l = 0
    for each in res:
        cnt = 0
        for _, t in df.iterrows():
            if all([t[x[0]] == x[1] for x in each]):
                cnt += 1
        if cnt > min_sup: l += 1
    
    print(l)
    '''
    
    print("Runtime:", round(time.time() - start, 2), "seconds.")
