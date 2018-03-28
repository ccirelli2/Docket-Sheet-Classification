
# IMPORT LIBRARIES

import os
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
import graphviz
from sklearn.tree import export_graphviz    
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV


#   Classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier

# CREATE DATAFRAMES FOR THE FEATURES AND TARGETS


def get_feature_target_dataframes(File, dataset = 'Features'):
    '''Documentation
    
    Input      = i.)  Raw file from hard drive. 
                 ii.) Choose whether to returnthe Feature or target dataset. 
                 
    Operations = i.)   Read in the file as a dataframe
                 ii.)  Reset the index as it contains the docket sheet names, which are not needed. 
                 iii.) Drop the index. 
                 iv.)  Create the feature dataset
                 v.)   Create the target dataset.     
    '''
    
    Return_df = ''
    
    # Read in file as a dataframe
    df = pd.read_excel(File)
    # Reset Index as it currently contains the docket sheet names. 
    df_reset_index = df.reset_index()
    # Drop Col 0
    df_drop_col = df_reset_index.drop('index', axis = 1)
    # Create our feature columns
    if dataset == 'Features':
        Return_df = df_drop_col.drop('Life Cycle Stage', axis = 1)
    elif dataset == 'Targets':
        Return_df = df_drop_col['Life Cycle Stage']
    else:
        print('You must chose either Features or Targets')
    
    return Return_df


# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()

    # BREAK

























