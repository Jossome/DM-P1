import pandas as pd

df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")

for i in range(10):
    print(df[1][i])
