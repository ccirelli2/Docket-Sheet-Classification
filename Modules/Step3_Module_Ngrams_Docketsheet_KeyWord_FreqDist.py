
# IMPORT LIBRARIES

import os
import re
import nltk
import pandas as pd
import string
from nltk.stem import *
stemmer = PorterStemmer()
from nltk import corpus

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


# CREATE A SET OF ALL HUMAN NAMES FROM THE NLTK CORPUS LIBRARY

def get_set_human_names():
    '''
    Purpose:  obtain a set of all human names
    Input:    none
    Output:   Set of of both female and male names
    '''
    # Create a lise of Male names, convert to lower case, split on '\n' as the text reads in a string as unicode
    Male_names = corpus.names.open('male.txt').read().lower().split('\n')
    # Create a lise of female names, convert to lower case, split on '\n' as the text reads in a string as unicode
    Female_names = corpus.names.open('female.txt').read().lower().split('\n')
    # Return to the user a set of the concatenation of both lists. 
    return set(Male_names + Female_names)


# CLEAN & TOKENIZE CONCATENATED TEXT FILE & RETURN SET

def clean_andTokenize_text(Text_file):
    '''
    Input      = Text File
    Operations = Tokenize, lowercase, strip punctuation/stopwords/nonAlpha
    Return     = Object = Set; Set = cleaned, isalpha only tokens
    '''
    # Strip Lists
    Punct_list = set((punct for punct in string.punctuation))
    Stopwords = nltk.corpus.stopwords.words('english')
    Set_names = get_set_human_names()
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
    # Strip 2 letter words
    Text_strip_2letter_words = filter(lambda x: len(x)>3, Text_strip_nonAlpha)
    # Strip names
    Text_strip_names_2 = filter(lambda x: x not in Set_names, Text_strip_2letter_words)
    # Take Stem of Each Token 
    Text_stem = [stemmer.stem(x) for x in Text_strip_names_2]
    # Note that we are not returning a set here as with Ngrams we are looking for patters which could be altered materially by using
    # a set function, which is better used outside the function if need be. 
    return Text_stem


# TURN CLEAN TOKENIZED TEXT INTO NGRAMS

def get_Ngrams(Clean_tokenized_text, Ngram_selection):
    # Create a list to capture Ngrams
    List_Ngrams = []
    
    # If Bigrams selected
    
    if Ngram_selection == 'Nograms':
        [List_Ngrams.append(x) for x in Clean_tokenized_text]
        
    elif Ngram_selection == 'Bigrams':
        [List_Ngrams.append((x,y)) for x,y in zip(Clean_tokenized_text, 
                                               Clean_tokenized_text[1:])]  
    # If Trigrams selected
    elif Ngram_selection == 'Trigrams':
        [List_Ngrams.append((x,y,z)) for x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:])]
    # If Quadgrams selected. 
    elif Ngram_selection == 'Quadgrams':
        [List_Ngrams.append((w,x,y,z)) for w,x,y,z in zip(Clean_tokenized_text, 
                                                    Clean_tokenized_text[1:], 
                                                    Clean_tokenized_text[2:], 
                                                    Clean_tokenized_text[3:])]
    # Return Ngrams list
    return List_Ngrams


# STEP 3: CREATE NGRAMS OF DOCKETSHEET ENTRIES

def get_docketsheet_ngrams(Tokenized_text):
    # Define the object Ngrams_text as an empty string
    Ngrams_text = ''
    # Check the length of the first key word in our Dict
    if len(DictKeyWords.values()[0]) == 1:
    # Use our get_Ngrams function to create the Ngrams.
        Ngrams_text = stp1.get_Ngrams(clean_tokenize_row, 'Nograms')
    elif len(Dict_key_words[key][0]) == 2:
        Ngrams_text = stp1.get_Ngrams(clean_tokenize_row, 'Bigrams')
    elif len(Dict_key_words[key][0]) == 3:
        Ngrams_text = stp1.get_Ngrams(clean_tokenize_row, 'Trigrams')
    elif len(Dict_key_words[key][0]) == 4:
        Ngrams_text = stp1.get_Ngrams(clean_tokenize_row, 'Quadgrams')
    # Return to the user the Ngram_text
    return Ngrams_text



# CODE TO OBTAIN KEY WORD APPEARANCE FOR DOCKETSHEETS 

def get_KeyWordAppearance_DocketsheetEntries(Docketsheet, List_DictKeyWords):
    '''
    Purpose     = The purpose of this code is to generate a dataframe whose rows are the docketsheet entries, columns
                  the key ngrams and the values the appearance of these ngrams in each docketsheet entry. 
    Input       = 1.) A dataframe representing the docketsheet limited to only those applicable rows and columns. 
                  2.) A single list of key words.  You may input a single list or loop over multiple lists of key words. 
                      The important point is that the object must be input as a list. 
    Operations  = 1.) Create a dataframe to house the rows and columns 
                  2.) Since the names of each docketsheet entry do not indicate their position in the dataframe, create
                      and object to keep the count of the num of rows that we iterate over, which will later be used in
                      the naming of the rows in the new dataframe returned to the user. 
                  3.) Create a list to capture the values 0/1 that will represent the appearance or not of each of the
                      Ngrams.  This list is the row of values for each docketsheet entry. 
                  4.) Clean and tokenize the text in the same manner as was done in Stage1. 
                  5.) Create Ngrams of the docketsheet rows in the same manner as was done in Stage1. 
                  6.) Iterate over each Ngram in the List of Ngrams input into this function. 
                  7.) Determine if the Ngram is present and add values to the List_word_matches defined earlier .
                  8.) Define our row. 
                  9.) Append the row to our dataframe. 
    
    '''
    
    # Create New Dataframe
    df_DAT = pd.DataFrame({}, index = List_DictKeyWords)
    
    # Count of Rows
    Count = 0
    
    # Iterate over row of the docketsheet df as an enumerated tuple. 
    for row in Docketsheet.itertuples():

        # Star the Count of the rows
        Count += 1
        
        # List to capture each row.  List will reset on each iteration of the code. 
        List_word_matches_single_row = []
        
        # Clean row[4], which is the text column of the docketsheet. 
        clean_tokenize_row = clean_andTokenize_text(row[4])                
            
        # Once the text of the row is tokenized, we need to create the Ngrams
        docketsheet_ngrams = get_docketsheet_ngrams(clean_tokenize_row)
            
        # So iterate every word in key_word_list for each rows 
        for Ngram in List_DictKeyWords:
            
            # Check to see if the word is in the clean text
            if Ngram in docketsheet_ngrams:
                # If there is a match, append 1 to the list
                List_word_matches_single_row.append(1)
            else: 
                # If not, append 0
                List_word_matches_single_row.append(0)
        
        # Create a string from the counter to add to your column name. 
        Row_num = 'row' + str(Count) + ' ' 
        
        # Create a column in your new datafrmae to capture the case number and list of matches. 
        df_DAT[Row_num + row[1] + ' ' + str(row[2])] = List_word_matches_single_row        

        # Return our dataframe w/ an index as the list of key words, columns as each case. 
    
    return df_DAT
            

# FUNCTION TO CREATE AN NGRAM COLUMN
    
def create_Ngram_column(dataframe, Ngrams):
    '''
    Purpose:    The purpose of this code is to:
                1.) to adjust our dataframe to account for the fact that the pandas multiindex merges the 
                cells that contain the same words.     
                2.) Create a single column that includes a tuple of the Ngrams.
                3.) Remove the old columns. 
                
    Input:      Output from our FreqDist function
    Output:     The same dataframe but withou the individual word columns, which is replaced with a single column 
                representing our Ngrams. 
    '''
    
    
    
    
    
    # Create lists to capture each word in the target column. 
    List_level_0 = []
    List_level_1 = []
    List_level_2 = []
    
    # Create a list to capture our new column where where the none values are converted to the last actual word.
    New_column_0 = []
    New_column_1 = []
    New_column_2 = []
    
    # Lists to capture tuples
    List_tuple_bigrams = []
    List_tuple_trigrams = []
    List_tuple_quadgrams = []

    
    # Reset the index
    dataframe_reset_index = dataframe.reset_index()
    
    # For each word in the target column
    
    if Ngrams == 'Nograms':
        print('Because you selected Nograms, no adjustment is required.', 'Function is returning the original dataframe.','\n', '\n')
        
        
    # BIGRAMS
    
    elif Ngrams == 'Bigrams':
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
    
        # Drop old column and append new columne to dataframe. 
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        # Iterate over the new dataframe 
        for row in dataframe_reset_index.itertuples():
            # Create a tuple of the bigram
            Col_tuples = (row[1], row[2])
            # Append the bigram tuple to our List. 
            List_tuple_bigrams.append(Col_tuples)
        
        # Drop the individual columns. 
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1'], axis = 1)
        # Append the bigram column to the dataframe with a col name of 0. 
        dataframe_reset_index[int('0')] = List_tuple_bigrams
        dataframe_reset_index = dataframe_reset_index.sort_index(ascending = True, axis = 1)
    
    
    # TRIGRAMS
    
    elif Ngrams == 'Trigrams':
        
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        for word in dataframe_reset_index['level_1']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_1.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_1.append(List_level_1[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_1.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_1'], axis = 1)
        dataframe_reset_index['level_1'] = New_column_1
    
        # Creat a single column for the quadgram tuple and remove the old ones. 
        for row in dataframe_reset_index.itertuples():
            Col_tuples = (row[1], row[2], row[3])
            List_tuple_quadgrams.append(Col_tuples)
        
        # Drop old columns
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1', 'level_2'], axis = 1)
        dataframe_reset_index[int('0')] = List_tuple_quadgrams            
        dataframe_reset_index = dataframe_reset_index.sort_index(ascending = True, axis = 1)
    
    
    # QUADGRAMS
    
    elif Ngrams == 'Quadgrams':
        # Iterate over each row of the dataframe. 
        for word in dataframe_reset_index['level_0']:
        # Append each word to the list. 
            if isinstance(word, str):
                List_level_0.append(word)
        
        # And if present row in the column == None
            if isinstance(word, float):
                New_column_0.append(List_level_0[-1])
            else:
                # If the last word is not == to None, then append the present word. 
                New_column_0.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_0'], axis = 1)
        dataframe_reset_index['level_0'] = New_column_0
        
        for word in dataframe_reset_index['level_1']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_1.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_1.append(List_level_1[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_1.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_1'], axis = 1)
        dataframe_reset_index['level_1'] = New_column_1

        for word in dataframe_reset_index['level_2']:
            # Append each word to the list. 
                if isinstance(word, str):
                    List_level_2.append(word)
                    
            # And if present row in the column == None
                if isinstance(word, float):
                    New_column_2.append(List_level_2[-1])
                else:
                    # If the last word is not == to None, then append the present word. 
                    New_column_2.append(word)
        
        # Append new column to the dataframe
        dataframe_reset_index.drop(['level_2'], axis = 1)
        dataframe_reset_index['level_2'] = New_column_2
        
        # Creat a single column for the quadgram tuple and remove the old ones. 
        for row in dataframe_reset_index.itertuples():
            Col_tuples = (row[1], row[2], row[3], row[4])
            List_tuple_quadgrams.append(Col_tuples)
                
        dataframe_reset_index = dataframe_reset_index.drop(['level_0', 'level_1', 'level_2', 'level_3'], axis = 1)
        dataframe_reset_index[int('0')] = List_tuple_quadgrams            
        dataframe_reset_index = dataframe_reset_index.sort_index(ascending = True, axis = 1)
    
    
    # Return the new column list to the user. 
    return dataframe_reset_index


# WRITE FILE TO EXCEL

def write_to_excel(dataframe, location, filename):
    os.chdir(location)
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()



























