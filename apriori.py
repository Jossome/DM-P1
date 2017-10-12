from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time

def find_freq_1_itemset(D):
    tmp = []
    for col in D.columns:
        col_cnt = df[col].value_counts()
        col_cnt.index = [(col, x) for x in col_cnt.index]
        tmp.append(col_cnt)
    return pd.concat(tmp)

def apriori(D, min_sup):
    L = []
    sup_cnt = find_freq_1_itemset(D)
    
    L.append([(x,) for x in sup_cnt.index if sup_cnt[x] >= min_sup])
    while len(L[-1]) > 0:
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
                #Tuple is hashable as index in dict, but there are sequence issues.
                c = tuple(sorted(set(l1).union(set(l2)), key = str))
                if has_infreq_subset(c, L): pass
                else: C[c] = 0
    return C
    
def has_infreq_subset(c, L):
    for s in combinations(c, len(c) - 1):  #generate each subset s of c
        if s not in L:
            return True
    return False


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    L = apriori(df, min_sup = len(df) * 0.8)
    print(reduce((lambda x, y: x + y), L))

    print("Runtime:", round(time.time() - start, 2), "seconds.")
