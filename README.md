# DM-P1

- Exercise 6.7(1)&(2) on "Data Mining Concepts and Techniques (3rd Edition)".
- UCI adult dataset. http://archive.ics.uci.edu/ml/datasets/Adult

- [X] Apriori(AS94b)
    - Added dinstinguish tags for each column, since they are not the same thing even if they are of the same value. The format is a tuple: (column, value).
    - All the frequent sets are in a list, each set is a tuple.
    - If we set the min\_sup at 80%, we can have a runtime around 5.6s.
    - If we set the min\_sup at 60%, the runtime will rise to 18s. 
- [ ] FP-growth(HPY00)
- [ ] Improved Apriori of mine


Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
