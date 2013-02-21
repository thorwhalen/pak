__author__ = 'thorwhalen'


# input: a (element or list) and b (list)
# output: True iff a is in b
def ismember(a,b):
    import numpy as np
    if isinstance(a,list):
        return not not np.intersect1d(a,b)
    else:
        return not not np.intersect1d([a],b)



