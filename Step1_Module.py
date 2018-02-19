
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string


# IMPORT TARGET FILE / DELIMIT ROWS / REMOVE ROWS PERIOD = NONE

def import_docket_sheet_file(Excel_file):
    '''
    Input      = None
    Operations = Read file, select columns, eliminate time-period = None
    Return     = dataframe. 
    '''
    # Read in Excel File
    df_docket_sheets = pd.read_excel(Excel_file)
    # Select columns
    df_docket_sheets_fit = df_docket_sheets.iloc[:,0:-1]
    # Select rows != None
    TimePeriod_notNone = df_docket_sheets_fit['Time Period'] > 0
    # Return dataframe
    return df_docket_sheets_fit[TimePeriod_notNone]


# CONCATENATE DOCKET SHEET TEXT

def create_Concatenated_text_file(df_docketFile, new_file_name):
    '''
    Input      = doketFile as a dataframe. 
    Operations = Create new file, limit docketfile to 'docket text', iterate rows, write to new file. 
    Output     = Function will write the new file to the current-working-direcotry.  No other return from function.  
    '''
    
    # Create new write file
    New_File = open(str(new_file_name) + '.txt','w')
    
    # Limit Docket Sheet to Text Column
    df_docket_text = df_docketFile['docket_text']
    
    # Create Loop Through List of Directories
    for row in df_docket_text:
        
        # Write files to new file
        New_File.write(str(row))
        New_File.write('\n')
    # Close File
    New_File.close()
    
    return None


# IMPORT CONCATENATED TEXT FILE

def import_concatTxt(filename):
    # Import Concat Text File
    File = filename
    File_open = open(File) 
    return File_open.read()


# CLEAN & TOKENIZE CONCATENATED TEXT FILE

def clean_andTokenize_text(Text_file):
    '''
    Input      = Text File
    Operations = Tokenize, lowercase, strip punctuation/stopwords/nonAlpha
    Return     = Object = Set; Set = cleaned, isalpha only tokens
    '''
    # Strip Lists
    Punct_list = [punct for punct in string.punctuation]
    Stopwords = nltk.corpus.stopwords.words('english')
    # Tokenize Text
    Text_tokenized = nltk.word_tokenize(Text_file)
    # Convert tokens to lowercase
    Text_lowercase = (token.lower() for token in Text_tokenized)
    # Strip Punctuation
    Text_tok_stripPunct = filter(lambda x: (x not in Punct_list), Text_lowercase)
    # Strip Stopwords
    Text_strip_stopWords = filter(lambda x: (x not in Stopwords), Text_tok_stripPunct)
    # Strip Non-Alpha
    Text_strip_nonAlpha = filter(lambda x: x.isalpha(), Text_strip_stopWords)
    # Return cleaned and tokenized text
    return Text_strip_nonAlpha


# FREQUENCY DISTRIBUTION FUNCTION

def get_freq_Dist_setWord_Single_timePeriod(df_docketSheet_single_TimePeriod, df_docketsheet_wordSet):
    '''The purpose of this function is to calculate the frequency with which each setword appears in a single lifecycle time period. 
    Input  = df_docketsheet_wordSet, docket_sheet_dataframe
    Output = List with each value representing the avg that each setWord appears in the text. 
    '''
    
    # List to capture the average count each set_word appears in the docket sheet.  
    List_avg_appearance_set_word = []
    
    # For each word_set in the word_set index:
    for word_set in df_docketsheet_wordSet.index:
        
        # Define your counts to capture. 
        Count_num_rows = 0
        Count_matches = 0
        
        # Iterate over each row in the docket sheet, all of which are part of the same life cycle period.  
        for row in df_docketSheet_single_TimePeriod.itertuples():
            
            # Keep count of each token list we iterate over.  This will be the denominator for calculating our average. 
            Count_num_rows += 1

            # Run clearning and tokenizing function over each row.  Return list of clean tokens. 
            clean_tokenized_text = list(clean_andTokenize_text(row[4]))
            
            # Check to see if in the given row there is a match. 
            if word_set in clean_tokenized_text:
                # Count the match. 
                Count_matches +=1
        
        # Calculate the avg times the set word appears in the text.  
        '''Note that we are now outside of the loop to iterate over the rows, bust still within the word_set loop. 
           Therefore, this will calculate the avg for each setWord'''
        
        Avg = round((Count_matches / Count_num_rows),2)
        
        # Append the average value to the list.  Each value will coinside with a setWord.  
        #Since we are within the loop the order between setWord and value will be kept. 
        List_avg_appearance_set_word.append(Avg)
    
    # Return to the user the List containing the average appearance of each setWord. 
    return List_avg_appearance_set_word




# CREATE A DATAFRAME WHOSE INDEX IS THE SET OF WORDS AND COLUMNS THE FREQ DIST FOR EACH STAGE OF THE LIFE CYCLE

def create_dataframe_setWord_freqDist(df_Master_DocketSheet_File, Set_tokenized_concatText):
    '''The purpose of this function is to create a dataframe whose index is the set of unique words taken from our concatenated text file, and
       whose columns represent each stage of the life cycle time period, and 
       whose values equal the average frequency of that word for the given stage
       
       Input      = Docket Sheet Master Dataframe
       Operations = 1.) Create a set of the Life Cycle Stages from the Master Docket Sheet. These will be our columns. 
                    2.) Create a dataframe whose index is the set of unique words from our concatenated text file. 
                    3.) Iterate over each stage in this set
                    4.) Limit the dataframe to each stage
                    5.) Obtain the set_Word frequency distribution for that stage.  This function cleans and tokenizes the text for the given stage
                        and returns a list of the frequency for the stage for each word in the index.  So the frequencies match up with each word
                        in the index. 
                    6.) For each frequency distribution list return from step 5, create a column in our dataframe whose name is the life cycle stage 
                        in question. 
       
    '''
    
    # Create a set of Life Cycle Time Periods from the Master Docket Sheet File
    List_LC_stages = set(df_Master_DocketSheet_File['Time Period'])
    
    # Create Dataframe whose index is the set of words from our concatenated text file.
    df = pd.DataFrame(Set_tokenized_concatText)
    df_docketsheet_wordSet = df.set_index(0)
    
    # Iterate over Life Cycle Stages
    for stage in List_LC_stages:
        # Limit the Master DocketSheet File to the current stage
        Match_period = df_Master_DocketSheet_File['Time Period'] == stage
        df_docketSheet_stage_N = df_Master_DocketSheet_File[Match_period]
        
        # Get the Frequency Distribution of setWords for the current Stage
        List_setWord_freqDist = dsc_m.get_freq_Dist_setWord_Single_timePeriod(df_docketSheet_stage_N, df_docketsheet_wordSet)
        
        # Create a Column in the Master Dataframe representing the frequency Distribution for each LC Stage
        df_docketsheet_wordSet['Life Cycle Stage: '+str(stage)] = List_setWord_freqDist 
    
    # Return our completed Word Frequency Distribution Dataframe
    return df_docketsheet_wordSet



# WRITE FILE TO EXCEL

def write_to_excel(dataframe, filename):
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()



























