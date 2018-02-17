

def helloworld():
    print('Hello World.  Today is a good day to code.')

    

def clean_text_4_classification_remove_backslashes(Text_file):
    '''The purpose of this function is to clean the text files of numerous instances of backslashes 
    in order to prepare them for the regex expression search. 
    Input  =   Single text file 
    Output =   Single text file cleaned 
    '''
    
    # Convert text to lowercase
    Text_file_lower = Text_file.lower()
    
    # Split any values in the text on the backslash.  The Text_split_slash should return a list. 
    Text_split_slash = Text_file_lower.split('\\')
        
    # Return the list to a text. 
    Text_rejoined = ' '.join(Text_split_slash)
                
    # Return a list of the cleaned text docs. 
    return Text_rejoined


def clean_text_4_classification_remove_nABC(Text_file):
    '''The purpose of this function is to remove the 'n' that appears before words that begin with an upper case letter.  
    Input  =   Single txt file
    Output =   Clean list of tokens from original txt file
    '''
    # Define the regex expression that you want to search for. 
    Regex_exp = re.compile('n[A-Z*]')
    
    # Create a list to capture the tokens once they are cleaned 
    Text_tokenized_cleaned = []
            
    # Tokenize the given text
    Text_tokenized = nltk.word_tokenize(Text_file)
            
    # Run for loop over tokens for a given text. 
    for token in Text_tokenized:

        # Search for the regex expression
        Regex_search = re.search(Regex_exp, token)
                
        # Test if there was match (None = no match)
        if Regex_search != None:
                     
            # If there was a match, take all letters after the 'n'.   
            token_cleaned = token[1:]
                    
            Text_tokenized_cleaned.append(token_cleaned)
                        
        # If the Regex_search returned None, return the token back to the Text_tokenized_cleaned list
        else:
            Text_tokenized_cleaned.append(token)
    
    # Return a list of clean tokens
    return Text_tokenized_cleaned


def create_dict_punct():
    '''The purpose of this function is to simply create a dictionary of punctuation symbols to use
    in other functions
    Input  = None
    Output = Dict whose keys are the distinct punctuation marks. 
    '''
    import string
    Dict = {}
    Punct = string.punctuation
    for x in Punct:
        Dict[x] = ''
    return Dict 

def strip_punctuation(Token_list):
    '''The purpose of this function is to strip the punctuation from a list of tokens. 
    Input  =  List of tokens
    Output =  List of tokens absent punctuation.  
    '''
    # Import punctuation dictionary
    Dict_punct = create_dict_punct()

    # Create a list to capture the cleaned tokens
    Clean_token_list = []    
        
    # Iterate over the tokens in the txt file
    for x in Token_list:
        if x not in Dict_punct:
            # Append tokens to clean token list
            Clean_token_list.append(x)
    
    # Return a list of cleaned text
    return Clean_token_list

def strip_two_letter_words(Token_list):
    '''The purpose of this function is to remove any two letter tokens from a list of tokens.
    Input  =   List of tokens
    Output =   List of tokens absent two letter words'''
    
    List = [x for x in Token_list if len(x) > 2]
    
    return List

def create_dict_stopwords():
    '''The purpose of this code is to create a dictionary of stop words. 
    Input  = None
    Output = Dictionary of stop words'''
    
    from nltk.corpus import stopwords
    Stopwords = stopwords.words('english')                  
    Dict = {}
    for x in Stopwords:
        Dict[x] = ''
    return Dict

def strip_stop_words(Token_list):
    ''' The purpose of this code is to strip the stop words from a given text
    Input  = List of tokens 
    Outpu  = Text clean of stop words'''
    
    stop_words = create_dict_stopwords()
    List = []
    for x in Token_list:
        if x not in stop_words:
            List.append(x)
    return List

def create_Concatenated_text_file(Dir_list, New_file_name):     
    # Create new write file
    New_File = open(str(New_file_name) + '.txt','w')
    
    # Identify text files to retreive
    Text_files = (file for file in Dir_list if 'txt.' in file)  # attempt to use a generator. 

    # Create Loop Through List of Directories
    for x in Text_files:
        File = open(x, 'rb')
        Text = File.read()
        
        # Write files to new file
        New_File.write(str(Text))
        New_File.write('\n')
    # Close File
    New_File.close()

def write_to_text_file(Text_2_write, File_name2_use):
    file = open(str(File_name2_use) + '.txt', 'w')    
    file.write(Text_2_write)   

    
def get_cleaned_concatenated_text_file(Dir_list):
    '''
    Input  = List of files in the directory
    Output = Cleaned text 
    
    '''
    # Note, the author assumes there is only one Concat file in the dir.  Since the order of the files in the dir
    # can change, the better approach is to identify it using a list comprehension with an if statement. 
    Clean_concat_text = [file for file in Dir_list if 'Concatenated Text File - Cleaned' in file]
    
    for text_file in Clean_concat_text:
        
        File = open(text_file)
        # Read in dirty text
        Text_dirty = File.read()
        # Run cleaning pipeline
        Clean_text = text_clearning_pipeline_Input_4_Error_Checker_Function(Text_dirty)
    
        # Return cleaned text
    return Clean_text


def create_Wordnet_set():
    '''The purpose of this function is to create a set of all words from the wordnet dictionary.
    Input  = None
    Output = Set object of all words. 
    '''
    # Import words from wordnet
    from nltk.corpus import wordnet as wn
    Words = wn.words()

    # Create List to capture words  
    List_dict_words = []; [List_dict_words.append(x) for x in Words]
    
    # Create Set
    Set_dict_words = set(List_dict_words)
    
    # Return Set
    return Set_dict_words

def correct_tokens_nABC_using_wordnet_dict(Token_list):
    '''The purpose of this code is to '''
    
    Wordnet_set = create_Wordnet_set()
    
    # Creat a clean list of tokens to return to the user. 
    Token_list_cleaned = []
    
    # Convert tokens to lowercase
    Token_list_lower = [x.lower() for x in Token_list]
    
    # Loop over the list of tokens
    for token in Token_list_lower:
        # Find the tokens that start with an 'n'
        if token[0] == 'n':
            # See if the token is in the WordNet Dict when the 'n' is dropped
            if token[1:] in Wordnet_set:
                # If the token is in the dictionary, append the token without the 'n'
                Token_list_cleaned.append(token[1:])
            else:
                # If not, then just append the token as there was no matching word. 
                Token_list_cleaned.append(token)
                
        # If the token does not start with an 'n', then this code does not apply and append back to the list. 
        else:
            Token_list_cleaned.append(token)
    
    return Token_list_cleaned

def get_isalpha(Token_list):
    List = [x for x in Token_list if x.isalpha()]
    return List

def get_set_from_text(Dir_list):
    '''The purpose of this code is to create a set of unique tokens from a text file as a string object. 
    Input  =  Text file as a string object 
    Output =  Set of unique tokens. 
    '''
    
    os.chdir(r'I:\Legal Analytics Sprint-S18\Team Folders\Team Wang\Files Converted to Txt')
    Dir_list = os.listdir(r'I:\Legal Analytics Sprint-S18\Team Folders\Team Wang\Files Converted to Txt')
    
    # Define Set Object
    Create_set = ''
    
    # Obtain Your Target File
    Target_file = [file for file in Dir_list if 'Cleaned' in file]
    
    # Loop over Target_file since it is a generator object. 
    for file in Target_file:
        File = open(file)
        Text = File.read()
        # Tokenize Text
        Text_tokenized = nltk.word_tokenize(Text)
        # Create Set
        Create_set = set(Text_tokenized)
    # Return Set
    return Create_set

def get_clean_text_using_text_clearning_pipeline(Text_file):
    '''The purpose of this function is to prepare text for use with the Error Checker Program
    Input  =  Single text file
    Output =  List of clean tokens representing a single text. 
    '''
    # Run Clearning Pipeline (These functions are taken from the ones define above)
    
    # Input Text Files
    txt_strip_backslashes = clean_text_4_classification_remove_backslashes(Text_file)
    txt_strip_nABC = clean_text_4_classification_remove_nABC(txt_strip_backslashes)
    # Input Tokens - **At a later time you can loop over a single list of tokens and run them through these functions. 
    # Then remove the list creation from each function.  This should spead up the function markedly. 
    txt_strip_punct = strip_punctuation(txt_strip_nABC)
    txt_strip_2_letter_words = strip_two_letter_words(txt_strip_punct)
    txt_strip_stop_words = strip_stop_words(txt_strip_2_letter_words)
    txt_correct_nABC_using_wordnet = correct_tokens_nABC_using_wordnet_dict(txt_strip_stop_words)
    Final_tokenized_text = get_isalpha(txt_correct_nABC_using_wordnet)
    
    return Final_tokenized_text

def create_dataframe_first_N_num_txt_files_target_dir():
    # Create Dataframe 1st Hundred Txt Files
    import os
    import pandas as pd
    
    os.chdir(r'I:\Legal Analytics Sprint-S18\Team Folders\Team Wang\Files Converted to Txt')
    Dir_list = os.listdir()
    Text_files = [x for x in Dir_list if '.txt' in x]
    List_hund = Text_files[3:103]
    
    df = pd.DataFrame(List_hund)
    
    write_to_excel(df, 'Classify 100 Text Files')
    
    return None
    
def get_list_uniqueTokens_from_cleaned_concat_text():
    # Get List Unique Tokens From Cleaned Concatenated Text
    os.chdir(r'I:\Legal Analytics Sprint-S18\Team Folders\Team Wang\Files Converted to Txt')
    File = 'Concatenated Text File - Cleaned.txt'
    Open = open(File, 'rb')
    Read = Open.read()
    Str = str(Read)
    Tokenize = nltk.word_tokenize(Str)    
    Set = set(Tokenize)
    List = list(Set)

    return List

def write_to_excel(dataframe, filename):
    import pandas as pd
    writer = pd.ExcelWriter(filename+'.xlsx')
    dataframe.to_excel(writer, sheet_name = 'Data')
    writer.save()