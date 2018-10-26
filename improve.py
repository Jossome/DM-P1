from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time


def find_freq_1_itemset(D):
    tmp = []
    for col in D.columns:
        col_cnt = D[col].value_counts()
        for each in col_cnt.index:
            col_cnt[each] = (col_cnt[each], set(D.index[D.loc[:, col] == each]))
        col_cnt.index = [(col, x) for x in col_cnt.index]
        tmp.append(col_cnt)
    return pd.concat(tmp)


def apriori(D, min_sup):
    L = []
    I = []
    sup_cnt = find_freq_1_itemset(D)

    L.append([(x,) for x in sup_cnt.index if sup_cnt[x][0] >= min_sup])
    k = 1
    I.append([sup_cnt[x][1] for x in sup_cnt.index if sup_cnt[x][0] >= min_sup])
    Last = []
    while L[-1] != Last:
        Last = L[-1]
        C = apriori_gen(L[-1], I[-1], min_sup, k)
        k += 1
        Lk = []
        Ik = []
        for key in C:
            Lk.append(key)
            Ik.append(C[key])

        L.append(Lk)
        I.append(Ik)
    return L


def apriori_gen(L, I, min_sup, k):
    C = {}
    for i in range(len(I)):
        for j in range(len(I)):
            if len(L[i]) != k or len(L[j]) != k: continue
            tmp = I[i].intersection(I[j])
            if len(tmp) >= min_sup:
                c = tuple(sorted(set(L[i]).union(set(L[j])), key = str))
                C[c] = tmp
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

    min_sup = len(df) * 0.6
    L = apriori(df, min_sup = min_sup)
    res = reduce((lambda x, y: x + y), L)
    res = set(res)
    print(len(res))

    import pickle
    pickle.dump(res, open('correct.pkl', 'wb'))

    '''
    #This is test part.
    #If l and res have the same length, then all the frequent pattern generated are correct.

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
