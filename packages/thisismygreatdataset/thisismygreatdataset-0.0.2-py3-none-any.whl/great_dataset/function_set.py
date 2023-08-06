import os
import pandas as pd

def load_dataset(name):
    path = os.path.dirname(__file__) + '/dataset/'
    catalogue = pd.read_excel(path+'catalogue.xlsx')
    file_type = catalogue[name].values[0]
    file = path + name + '.' + file_type
    if file_type == "xlsx":
        df = pd.read_excel(file)
    elif file_type == "csv":
        df = pd.read_csv(file)
    else:
        pass
    return df
