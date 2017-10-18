import pandas as pd
import time
import pyfpgrowth


if __name__ == "__main__":
    
    start = time.time()
    
    df = pd.read_csv("adult.data", sep = ", ", header = None, engine = "python")
    df.columns = ["age", "workclass", "fnlwgt", "education", "education-num",\
            "marital-status", "occupation", "relationship", "race", "sex",\
            "capital-gain", "capital-loss", "hours-per-week", "native-country", "divide"]

    df_ = df.values.tolist()
    
    for i in range(len(df_)):
        df_[i] = list(zip(df.columns, df_[i]))
    
    patterns = pyfpgrowth.find_frequent_patterns(df_, len(df_) * 0.8)
    print(patterns)
    
    print("Runtime:", round(time.time() - start, 2), "seconds.")
