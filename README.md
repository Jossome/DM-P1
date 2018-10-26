# Frequent Patterns

- UCI adult dataset. http://archive.ics.uci.edu/ml/datasets/Adult
- Compatible for python2 and python3, pandas needed.

- Files
    - apriori.py: original apriori
    - fpgrowth.py: fp-growth
    - improve.py: improved apriori
    - demo.ipynb: a demonstration of the three algorithms.

- [X] Apriori(AS94b)
    - Added dinstinguish tags for each column, since they are not the same thing even if they are of the same value. The format is a tuple: (column, value).
    - All the frequent sets are in a list, each set is a tuple.

- [X] FP-growth(HPY00)
    - Finished almost all the functions, logic foundation of the algorithm.
    - The output is incomplete, which is an incident out of my ability. Maybe I will work on this later when I'm free.
    - However, the runtime is still valuable for our reference when comparing algorithms.

- [X] Improved Apriori
    - Only one scan of the whole dataset, which saves a lot of time.
    - At the cost of space to store the line numbers of item occurrance.

Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
Zhu, J. (2013). Improve of data mining Apriori algorithm. Electronic Design Engineering Vol.21, No.15.
