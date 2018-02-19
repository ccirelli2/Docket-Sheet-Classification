
# IMPORT LIBRARIES

import pandas as pd





def get_df_top5words_STDV(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    # Sort the Dataframe col "STDV" Ascending
    df_sorted = dataframe.sort_values(by = 'STDV', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: STDV'] = [row for row in df_sorted_topFive['STDV']]
    
    # Retun the final dataframe
    return df_final


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









