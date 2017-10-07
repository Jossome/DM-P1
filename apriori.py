from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time

#Apriori done for now. Independent on the dataframe structure.
def apriori(D, min_sup):
    L = []
    # 1-itemset
    sup_cnt = pd.Series(reduce((lambda x, y: x + y), D)).value_counts()
    L.append([[x] for x in sup_cnt.index if sup_cnt[x] > min_sup])
    while len(L[-1]) > 0:
        Lk = []
        C = apriori_gen(L[-1])
        for c in C:
            count = 0
            for t in df:
                if set(c).issubset(set(t)):
                    count += 1
            if count >= min_sup:
                Lk.append(c)
        L.append(Lk)
    return L
    
def apriori_gen(L):
    C = []
    for l1 in L:
        for l2 in L:
            if all([l1[i] == l2[i] for i in range(len(l1) - 1)]) and str(l1[-1]) < str(l2[-1]):
                c = list(set(l1).union(set(l2)))
                if has_infreq_subset(c, L): pass
                else: C.append(c)
    return C
    
def has_infreq_subset(c, L):
    for s in combinations(c, len(c) - 1):  #generate each subset s of c
        #print(s)
        if list(s) not in L: 
            return True
    return False


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
#    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
#            "marital-status", "occupation", "relationship", "race", "sex",\
#            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]
    
    df = df.values.tolist()  #Convert it to list, saves a lot of time.

    L = apriori(df, min_sup = len(df) * 0.6)[:-1] #The last one is empty set, so drop it.
    print(reduce((lambda x, y: x + y), L))

    print("Runtime:", round(time.time() - start, 2), "seconds.")