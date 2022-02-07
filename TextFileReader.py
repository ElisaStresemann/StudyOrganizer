#!/usr/bin/python3

'''
    Library for text file reading functions.
    
    Author: Robert Ringel
    Date: November, 2020
    File name: TextFileReader.py
'''

def open_file(file_name):
    ''' Opens the named text file for reading.
    
        Args:
            file_name (string) : name of the text file
            
        Returns:
            TextIOWrapper : reference to the opened file
    '''
    fh = None
    try:                                      
        fh = open(file_name, "rt")             
    except Exception as err:                  
        print(err)
    return fh

def read_line(file_handle):
    ''' Reads a line of text from the given file.
    
        Args:
            file_handle (TextIOWrapper) : reference to an open text file
        
        Returns:
            string : the line of text 
    '''
    text = None
    try:                                      
        text = file_handle.readline()          
    except Exception as err:                  
        print(err)
    return text

def get_line_items(file_handle, sep='\t'):
    ''' Reads a line of text from a file and provides a list of tokens.
    
        Args:
            file_handle (TextIOWrapper) : reference to an open text file
            sep (string) : a separator to split the line into tokens
            
        Returns:
            list : list of strings taken from the line
    '''
    items = None
    line = read_line(file_handle)
    if len(line) > 0:
        line = line.strip()
        items = line.split(sep)
    return items

def close_file(file_handle):
    ''' Closes the given file.
    
        Args:
            file_handle (TextIOWrapper) : reference to an open text file
    '''
    try:                                      
        if file_handle != None:
            file_handle.close()                
    except Exception as err:                  
        print(err) 
        
def main():
    ''' The main function shows how to use these functions.
    '''
    file = open_file('PegelNeisse.txt')
    line = read_line(file)
    print(line)
    items = get_line_items(file)
    print(items)
    close_file(file)
        
#print("[",__name__,"]")
if __name__ == "__main__":
    print("Calling main-function:")
    main()