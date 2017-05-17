#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
import os

"""
Useful functions to go through one or more folders of VSM datafiles and load desired files.
By default the indexer is '#' but can be specified if needed.

Files can be loaded according to their index, and its also easy to just load all datafiles in a folder,
or the first or last file.
"""

#~~~~~~~~~~~~~~~~~~~ FILE MATCHING ~~~~~~~~~~~~~~~~~~~ #
def argsort(unsorted_list):
    """ 
    Returns the indices that would sort an array (like in matlab or with numpy argsort) 
    """
    idx = sorted(range(len(unsorted_list)), key=lambda x:unsorted_list[x])
    
    return idx


def get_txt_files(directory, extension='.txt'):
    """ 
    In a directory, get names of all files with 
    relevant extension, defaults to .txt
    """
    filenames = []
    
    for filename in os.listdir(directory):
        basename, ext = os.path.splitext(filename)
        
        if ext == extension:
            filenames.append(filename)
            
    return filenames


def index_files(filenames, indexer):
    """ 
    Input:      A list of filenames
    Returns:    All filenames with an index matching the indexer string (e.g. '#'),
                as well as all indices of files.
                Sorted according to indices.
    """
    
    filenames_matched = []
    indices = []
    
    # Ensure special characters in indexer are not interpreted (e.g. \ or *)
    # Convert indexer to regular expression which returns 
    # the numbers found after the indexer
    indexer = re.escape(indexer)
    index_regex = re.compile(indexer+r'(\d+)')
    
    for filename in filenames:
        # Search for indexer in filename and return index number
        index = re.search(index_regex, filename)
        
        # If index number is found, append filename and index to list
        if index:
            index = int(index.group(1)) # Convert found string to integer
            filenames_matched.append(filename)
            indices.append(index)
        
    # Sort filenames according to index numbers
    idx = argsort(indices)
    indices = [indices[i] for i in idx]
    filenames_matched = [filenames_matched[i] for i in idx]
    
    return filenames_matched, indices


def match_files(directory, extension='.txt', indexer='#', index_vals='all', include_string=''):
    """ 
    Returns list of VSM datafiles in directory with relevant extension and index number
    Examples of possible I_vals to search for in the files:
        int: index_vals = 5 matches exactly the file with index 5
        list: index_vals =  [5, 6, 10, 4], matches files with I values in the list
        tuple: index_vals  = (5, 8), matches range of I_vals = [5, 6, 7, 8]
        string: 'all', 'first', 'last', (take a guess which filenames they will match...)
        
    TODO Filter out filenames not matching include_string
    """
    
    # Get all files with an index, as well as their indices
    filenames = get_txt_files(directory, extension)
    filenames, indices = index_files(filenames, indexer)
     
    filenames_matched = []
    
    # If input is a tuple, make it into a list ranging from first to last index
    if type(index_vals) == tuple:
        index_min = index_vals[0]
        index_max = index_vals[1] + 1
        
        index_vals = list(range(index_min, index_max))   
    
    
    # Match files of desired index or indices
    if type(index_vals) == int:
        # Look for and include filename with specific index
        for i, index in enumerate(indices):
            if index == index_vals:
                filenames_matched.append(filenames[i])
                continue
            
    elif type(index_vals) == list:
        # Look for and include filenames with the index in the desired range
        for i, index in enumerate(indices):
            if index in index_vals:
                filenames_matched.append(filenames[i])
                
    elif index_vals == 'first':
        # Find the file with the lowest index and append only that
        index_min = min(indices)
        idx_index_min = indices.index(index_min)
        filenames_matched.append(filenames[idx_index_min])
        
    elif index_vals == 'last':
        # Find the file with the highest index and append only that
        index_max = max(indices)
        idx_index_max = indices.index(index_max)
        filenames_matched.append(filenames[idx_index_max])
        
    elif index_vals == 'all':
        # All indexed files are wanted, match them all
        filenames_matched = filenames
    
    return filenames_matched




#~~~~~~~~~~~~~~~~~~~ FILE LOADING ~~~~~~~~~~~~~~~~~~~ #
def get_linenumber(filepath, search_string):
    """ 
    Returns first linenumber containing a specific string. 
    Used e.g. to find start of data with search_string=***DATA*** 
    """
    
    # Convert search string to make sure * is interpreted as \* and not a wildcard symbol
    search_string = re.escape(search_string)
    
    # Go through datafile line by line
    with open(filepath) as datafile:
        for linenumber, line in enumerate(datafile):
            
            # Search for string in the line
            match = re.findall(search_string, line)
            if match:
                break
        
        if not match:
            linenumber = None
            
    return linenumber


def get_header(filepath, search_string = '***DATA***'):
    # Header needs to be one lower than the linenumber with ***DATA*** in it when loading files (?)
    header = get_linenumber(filepath, search_string) - 1
    
    return header

def units_to_si(vsm_data):
    """ Checks units on a loaded VSM dataframe, converts to SI if in cgs """
    columns = vsm_data.columns
    
    if 'Field(G)' in columns:
        # Gauss to militesla
        vsm_data['Field(G)'] = vsm_data['Field(G)']/10
        vsm_data.rename(columns={'Field(G)':'B'}, inplace=True)
    
    if 'Moment(emu)' in columns:
        # emu to Am^2
        vsm_data['Moment(emu)'] = vsm_data['Moment(emu)']*1000
        vsm_data.rename(columns={'Moment(emu)':'m'}, inplace=True)
        
    if 'Temperature(K)' in columns:
        # Kelvin to C
        vsm_data['Temperature(K)'] = vsm_data['Temperature(K)']+273.15
        vsm_data.rename(columns={'Temperature(K)':'T'}, inplace=True)
    
    return vsm_data


def rename_columns(dataframe, naming='short'):
    #TODO: Recognize and rename datacolumns into something easier! (B instead of Field(G)...)
    print('Todo!')


def load_vsm_file(filepath):
    # Load a full datafile from the VSM
    # Delimiter of \s+ means any whitespace is delimiter
    data = pd.read_csv(filepath, 
                   delimiter='\s+', 
                   header=get_header(filepath))
    
    return data


def load_directory(directory, si_units=True, **kwargs):
    """ 
    Loads VSM datafiles from directory (defaults to current working directory).
    See match_files() for keyword arguments, such as index values.
    Returns a list of pandas dataframes containing the VSM data
    
    TODO: Ensure that all fields are renamed to short names (B, T, m etc) regardles of Si conversion
    """
    
    # Get current directory
    old_cwd = os.getcwd()
    
    print('Changing directory:')
    print(directory)
    os.chdir(directory)
    directory = os.getcwd()
    
    # Get filenames and prepare empty list with same size
    filenames = match_files(directory, **kwargs)
    vsm_data = [None]*len(filenames)
    
    print('Loading files:')
    for i, filename in enumerate(filenames):
        print(filename)
        vsm_data[i] = load_vsm_file(filename)
        if si_units:
            vsm_data[i] = units_to_si(vsm_data[i])
    
    # Go back to initial working directory
    os.chdir(old_cwd)
    
    
    return vsm_data
    

