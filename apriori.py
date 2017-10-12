from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time

def apriori(D, min_sup):
    L = []
    # 1-itemset
    tmp = []
    for col in D.columns:
        col_cnt = df[col].value_counts()
        col_cnt.index = [(col, x) for x in col_cnt.index]
        tmp.append(col_cnt)
    sup_cnt = pd.concat(tmp).sort_values(ascending = False)
    
    L.append([(x,) for x in sup_cnt.index if sup_cnt[x] > min_sup])
    while len(L[-1]) > 0:
        Lk = []
        C = apriori_gen(L[-1])
        for _, t in df.iterrows():
            for c in C:
                if set(c).issubset(zip(t.index, list(t))):
                    C[c] += 1
        Lk = [c for c in C if C[c] >= min_sup]
        L.append(Lk)
    return L
    
def apriori_gen(L):
    C = {}
    for l1 in L:
        for l2 in L:
            if all([l1[i] == l2[i] for i in range(len(l1) - 1)]) and str(l1[-1]) < str(l2[-1]):
                c = tuple(set(l1).union(set(l2)))
                if has_infreq_subset(c, L): pass
                else: C[c] = 0
    return C
    
def has_infreq_subset(c, L):
    for s in combinations(c, len(c) - 1):  #generate each subset s of c
        #print(s)
        if s not in L: 
            return True
    return False


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    L = apriori(df, min_sup = len(df) * 0.6)[:-1] #The last one is empty set, so drop it.
    print(reduce((lambda x, y: x + y), L))

    print("Runtime:", round(time.time() - start, 2), "seconds.")
