__author__ = 'thorwhalen'



def get_data(dat,data_folder=''):
# input: dat (a csv file, a data file, or the data itself
# output: load data
    import os.path
    import pandas as pd
    from pak.file.name import fileparts,data_file,delim_file
    from pak.util import log
    if isinstance(dat,str): # if input dat is a string
        root,name,ext = fileparts(dat)
        if root: # if root is not empty
            data_folder = root
        dataFile = data_file(dat,data_folder)
        if dataFile:
            df = pd.load(dataFile)
        else:
            delimFile = delim_file(dat)
            if delimFile:
                log.printProgress('csv->DataFrame')
                df = pd.read_csv(delimFile)
            else:
                raise NameError('FileNotFound')
        return df
    else: # assume isinstance(dat,pd.DataFrame) or isinstance(dat,pd.Series)
        return dat

def mk_series(df,indexColName,dataColName):
    df = get_data(df)
    sr = df[dataColName]
    sr.index = df[indexColName].tolist()
    return sr

