import csv
import pandas as pd
import numpy as np
import os
import re
from .global_settings import *

def get_subject_dir(path):
    """ Return sublist of directories with subect code in name, from a given path """
    return [n for n in os.listdir(path) if re.match(r'[A-Z]\d{3}',n)]

def get_subject_list(path):
    """ Return list of subjects, based on a given list. """
    return [n[:4] for n in os.listdir(path) if re.match(r'[A-Z]\d{3}',n)]

def read_file(path,sub_dir,file_name):
    """ Return data frame, read from a given path,  """
    return pd.read_csv(f'{path}/{sub_dir}/{file_name}','\t',skiprows=3)

def get_event_data_frame(file,event_code):
    """ Select part of data frame starting with row with second event_code 
    (first one is stimulation, second one is rating)
    and return part of it with event code and 20 following rows. """
    #get lower argument, where event code is given 
    #and return second appearance
    arg_low = file.loc[file['Code'] == event_code].index[1]
    return file.loc[arg_low:arg_low+20]

def get_event_codes(file):
    """ Return event codes list, that file contains. """
    return[f'S{n_sce}_P{n_part}' for n_sce in range(1,6) for n_part \
           in range(2,6) if f'S{n_sce}_P{n_part}' in file['Code'].values]

def get_tp(file_name):
    """ Return time point information from file name. """
    return [tp for tp in TIME_POINT_LIST if tp.lower() in file_name.lower()][0]
        
def get_variable_value(df,var):
    """ Return value of given variable in a given data frame """
    arg_var = df[df['Code'] == var].index[0]+1
    return df.loc[arg_var,'Code']

def get_event_results(file,event_code_list,sub_code,tp):   
    """ Return results, updated for each event, present in a given file,
    based on a given list of events codes. Results is a dictionary with
    time point linked to nested sub-dictionary. In sub-dictionary, there is
    created variable 'Kod OB', linked to given subject code."""
    #create placeholder-directory linked to each time point, with
    #subject code as starting variable (which later is appended to Data Frame)
    #get names of files in a given sub-directory
    results = {tp:{'Kod OB':sub_code} for tp in TIME_POINT_LIST} 
    #Iterate for each event codes, detected in a given file
    for event_code in event_code_list:
        #Iterate for each variable analyzed variables
        for var in MEASURED_VARIABLES:
            #exception handler, if in given file is no rating/
            try:
                #get event data frame
                evt_df = get_event_data_frame(file,event_code)
                #save and link value to a given variable in placeholder
                results[tp][f"{DICT_INFORMAL_2_FORMAL[event_code]}_{var}"] = \
                                                get_variable_value(evt_df,var)
            except:
                pass
    return results

def get_file_results(path,sub_dir,file_name):
    """ Load file from a given file name, and save results on a given
    dictionary-placeholder. Func returns tuple time point (string), results"""
    #exception handling if name of file is wrong in terms of time point code
    try:
        #get time point
        tp = get_tp(file_name)
        #load file
        file = read_file(PATH,sub_dir,file_name)
        #geg codes, present in a given file
        event_code_list = get_event_codes(file)
        #get subject code
        sub_code = sub_dir[:4]
        #get results
        results = get_event_results(file,event_code_list,sub_code,tp)
        #return time point and results
        return tp,results
    except IndexError as error:
        #print message about exception hangling and save it in log
        msg = f"Warning: Problem with file {file_name}, {error}."
        print(msg)
        with open('error.log','a') as log:
            log.write(msg)
        pass

def get_result_dir(dir_list):
    """ Get result form every file in directory """
    #create dictionary with time point key linked to Data Frame placeholder 
    results_df = {tp:pd.DataFrame() for tp in TIME_POINT_LIST}
    #Iterate for each subject directory
    for sub_dir in dir_list:
        #Get and iterate for each file 
        file_names_list = os.listdir(f'{PATH}/{sub_dir}/')
        for file_name in file_names_list:
            #Exception handling in case of empty results
            #(when no rating is in file) 
            try:
                #get time point and results dict
                tp,results = get_file_results(PATH,sub_dir,file_name)
                #append dictionary results to data frame
                results_df[tp] = results_df[tp].append(results[tp],
                                                       ignore_index=True)
            except:
                pass
    return results_df

def save_results(results_df,name_file='Wyniki_behawioralne.xlsx'):
    """ Save results in one excel file, seperated in each sheet"""
    with pd.ExcelWriter(name_file) as writer:
        for tp in TIME_POINT_LIST:
            results_df[tp].to_excel(writer,sheet_name=tp)