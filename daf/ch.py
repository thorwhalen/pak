__author__ = 'thorwhalen'

import pandas as pd

def ch_col_names(df,new_names=[],old_names=[]):
# changes the names listed in new_names to the names listed in old_names
    if not isinstance(new_names,list): new_names = [new_names]
    if not isinstance(old_names,list): old_names = [old_names]
    assert len(new_names)==len(old_names),"old_names and new_names must be the same length"
    new_column_names = df.columns.tolist()
    new_names_idx = [new_column_names.index(name) for name in old_names]
    for i in range(len(new_names_idx)):
        new_column_names[new_names_idx[i]] = new_names[i]
    df.columns = new_column_names
    return df

