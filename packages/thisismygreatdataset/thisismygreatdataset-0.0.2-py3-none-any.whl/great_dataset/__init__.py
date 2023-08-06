import os
import pandas as pd

list_file_path = os.path.dirname(__file__)+'/dataset'
catalogue = list_file_path+'/catalogue.xlsx'
if not os.path.exists(catalogue):
        the_file_list_in_module = os.listdir(list_file_path)
        the_file_dic_in_module = dict()
        for file in the_file_list_in_module:
                name = file.split('.')
                the_file_dic_in_module[name[0]] = name[1]
        print(the_file_dic_in_module)
        df = pd.DataFrame(the_file_dic_in_module,index=[0])
        print(df)
        df.to_excel(catalogue)
