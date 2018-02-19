
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string

import pandas as pd


# FUNCTION TO RENAME COLUMNS TO THEIR INTEGER VALUES. 

df_rename_cols = df_freqDist.rename(index = str, columns = {'Life Cycle Stage: 1.0':1 , 
                                                            'Life Cycle Stage: 2.0': 2, 'Life Cycle Stage: 3.0': 3, 
                                                            'Life Cycle Stage: 4.0': 4,
       'Life Cycle Stage: 5.0': 5, 'Life Cycle Stage: 6.0': 6,
       'Life Cycle Stage: 7.0': 7, 'Life Cycle Stage: 8.0': 8,
       'Life Cycle Stage: 9.0': 9, 'Life Cycle Stage: 10.0': 10,
       'Life Cycle Stage: 11.0': 11})



# ITERATIVE FUNCTION TO SORT COLUMNS ONE FULL ROTATION

for num in range(1,13):
        '''Note that you'l likely need to insert your avg + STDV function in here'''
        # If the first column name is not = 11, which means we haven't reached the end of our rotation yet, then
        if df_rename_cols.columns[0] != 11:
            # Rename the first column to = num + 20.  Num = Original Col1 at each iteration. 
            df_rename_cols = df_rename_cols.rename(index = str, columns = {num:num+20})
            # With the first column renamed, sort ascending.  This will move the first column to the end. 
            df_rename_cols = df_rename_cols.sort_index(axis = 1, ascending = True)

            
# FUNCTION TO CALCULATE THE AVERAGE AND STDV FOR EACH LIFE CYCLE STAGE
            
def get_AVG_STDV_Target_Stage(dataframe):
    
    # Define lists to capture avg and stdv values for each row. 
    List_avg = []
    List_stdv = []
    
    for row in dataframe.itertuples():
        # Get the Average of row for all columns but col 1. 
        AVG = round(sum(row[2:]) / len(row[2:]), 2)
        # Get the Standard Deviation of row[1] / Avg. 
        STDV = row[1] / AVG
        
        #Append Values to the lists
        List_avg.append(AVG)
        List_stdv.append(STDV)
    
    # Create Columns for the AVG and STDV values
    dataframe['AVG'] = List_avg
    dataframe['STDV'] = List_stdv
    
    # Return the dataframe with the calculated avg and stdv values 
    return dataframe
    