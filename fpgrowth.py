from __future__ import print_function
import pandas as pd
from itertools import combinations
from functools import reduce
import time
from copy import deepcopy
import pickle


class node:
    def __init__(self, cnt=1):
        self.cnt = cnt  # cnt == 0: root
        self.children = {}

    def insert(self, trans):
        head = trans[0]
        tail = trans[1:]
        if head in self.children:
            self.children[head].cnt += 1
            if len(tail):
                self.children[head].insert(tail)

        else:
            self.children[head] = node()

    def contain_single_path(self):
        if self.cnt > 0 and len(self.children) == 0:
            return True

        if len(self.children) == 1:
            return self.children[list(self.children.keys())[0]].contain_single_path()

        return False

    def get_path(self):
        if len(self.children) == 0:
            return []

        key = list(self.children.keys())[0]
        return [(key, self.children[key].cnt)] + self.children[key].get_path()


def find_freq_1_itemset(df):
    tmp = []
    for col in df.columns:
        col_cnt = df[col].value_counts()
        col_cnt.index = [(col, x) for x in col_cnt.index]
        tmp.append(col_cnt)
    return pd.concat(tmp)


def tree_construct(df, min_sup):
    fp_tree = node(cnt=0)

    col = df.columns
    sup_cnt = find_freq_1_itemset(df)
    f = {k: v for k, v in dict(sup_cnt).items() if v >= min_sup}
    l = sorted(f, key=f.get, reverse=True)
    l = {k: i for i, k in enumerate(l)}

    for _, row in df.iterrows():
        trans = [x for x in zip(col, row) if x in l]
        trans = sorted(trans, key=lambda x: l[x])
        fp_tree.insert(trans)

    return fp_tree


def fp_growth(df, min_sup):
    fp_tree = tree_construct(df, min_sup)
    print(fp_tree.children)
    if fp_tree.contain_single_path():
        p = fp_tree.get_path()
        for s in combinations(p, len(p) - 1):
            # generate b U a
    else:












if __name__ == "__main__":

    start = time.time()

    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    min_sup = len(df) * 0.6
    fp = set(fp_growth(df, min_sup))
    # print(len(fp))

    # correct = pickle.load(open('correct.pkl', 'rb'))
    # print(correct - fp)

    print("Runtime:", round(time.time() - start, 2), "seconds.")
