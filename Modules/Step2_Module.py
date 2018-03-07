
# IMPORT LIBRARIES

import pandas as pd



#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV FREQ WITH LOWEST AVG

def get_AVG_STDV_Target_Stage(dataframe):
       
    # Define lists to capture avg and stdv values for each row. 
    List_avg = []
    List_stdv = []
    List_stdv_times_target = []
    
    for row in dataframe.itertuples():
        # Get the Average of row for all columns but col 1. 
        AVG = (sum(row[2:]) / 10)
        # Get the Standard Deviation of row[1] / Avg. 
        STDV = row[1] / AVG
        # Get the Standard Deviation Times the target time period frequency.  index = 2 is the target column. 
        # This value represents the STDV discounted by the frequency for which the word appears in the target column. 
        STDV_times_freq = STDV * row[1]
        
        #Append Values to the lists
        List_avg.append(AVG)
        List_stdv.append(STDV)
        List_stdv_times_target.append(STDV_times_freq)
    
    # Create Columns for the AVG and STDV values
    dataframe['AVG'] = List_avg
    dataframe['STDV'] = List_stdv
    dataframe['STDV_freq'] = List_stdv_times_target
    
    # Return the dataframe with the calculated avg and stdv values 
    return dataframe

def get_df_top5words_STDV(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    df_limit = dataframe.AVG.between(0.01, .02)
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "STDV_freq" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'STDV_freq', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: STDV_freq'] = [row for row in df_sorted_topFive['STDV_freq']]
    
    # Retun the final dataframe
    return df_final


#### FUNCTIONS TO GET TOP 5 WORDS WITH HIGHEST STDV & AVG > 2%. 

def get_df_top5words_AVG_greater_two_percent(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    df_limit = dataframe.AVG.between(0.021, .10)
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "STDV_freq" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'STDV_freq', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: STDV_freq'] = [row for row in df_sorted_topFive['STDV_freq']]
    
    # Retun the final dataframe
    return df_final





def get_df_top5words_Target_nearZero_highest_AVG(dataframe, Stage):
    '''The purpose of this function is to create a new dataframe that includes the 5 words with the highest STDV
    
    Input      = Dataframe that includes the AVG and STDV calculated for the Life Cycle Stage in Question
    Operations = Sort dataframe on STDV column, limit to top 5 rows, create new dataframe with Index = 1-5, create col for words and STDVs
    Output     = Dataframe with 5 rows, 2 cols, top5 words w/ STDV values. 
    '''
    
    df_limit = dataframe.iloc[:,1] < .05
    df_avg_range = dataframe[df_limit]
    
    # Sort the Dataframe col "STDV_freq" descending = True. 
    df_sorted = df_avg_range.sort_values(by = 'AVG', ascending = False)
    
    # Obtain First 5 Rows
    df_sorted_topFive = df_sorted.iloc[:5,]
    
    # Create New Dataframe Whose Index = 1-5
    df_final = pd.DataFrame({}, index = [1,2,3,4,5])
    
    # Create a Column to capture the top 5 words. 
    df_final['Life Cycle Stage: '+str(Stage)] = df_sorted_topFive.index
    
    # Create a Column to Capture the STDV for each word.
    df_final['Stage 1: STDV_freq'] = [row for row in df_sorted_topFive['STDV_freq']]
    
    # Retun the final dataframe
    return df_final



































