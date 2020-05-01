#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 22:40:01 2019

@author: jamie k li


This script is intended to exclude those whose devaluation effect is greater 
than 1.5x the interquartile range

This should be ran on a dataset, not on an individual subject! We will have to 
run this script iteratively on subs that passed the IID_exclude single_subject.py 
until we reach 79 usable people at each site

Will output the subjects to be removed as a .csv file.
This .csv file will be in a folder called 'exclusionary_output_dataset' that's 
located in the directory your data is in (or as specified in file_path variable)

Please have a unique identifier for data files in directory, this script will 
look for files that end in _d.mat (line 120) in the directory specified in path_file variable 
The unique identifier can be changed, but we should try to remain consistent across sites!
-if you change the unique identifier, change the number of spaces to look for as well (if that changes)

"""

##################################
#           IMPORTS
##################################

import scipy.io as spio
import pandas as pd
import numpy as np
import os
from datetime import date




##################################
#           FUNCTIONS
##################################

#Citation: https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries/7418519        
def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)
    
def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict
    

##################################
#          MAIN VARIABLES
##################################

#The following loads in the .mat file and turns it into python dicts
#This will need to be changed to point to the new data directory!
path_file = '/Users/jamie/Documents/IIDDataForJamieApril292019/WesselReplication2/GoodData/'

#add your collection site as stanford, tel_aviv, or missouri_western_state! For now, it will be stanford
collection_location = 'stanford'


cols = ['raw_reward_magnitude', #[Phase 1]
        'stim_reward', #(1 = low, no stop; 2 = mid low, no stop; 3 = mid high, no stop…)
        'stepwise_reward_magnitude', #(1 - 4)
        'paired_with_stopping', #
        'stim_shape', #(triangle, flipped triangle, square, diamond, cross, hexagon, I, circle)
        'stim_color', # (green, blue, cyan, magenta, yellow, orange, white, gray)
        'quadrant', # (1 = top L; 2 = top R; 3 = bottom R; 4 = bottom L; 5 = L; 6 = R)
        'response', # (1 = top L; 2 = top R; 3 = bottom R; 4 = bottom L; 5 = L; 6 = R)
        'reaction_time', #
        'block', #
        'num_trial_presentations', # (errors and misses are replayed in Phase 1)
        'stop_signal_trial_type', # [Phase 2] 0 = no SS, 1 = with SS
        'left_SSD', # [Phase 2]
        'right_SSD', # [Phase 2]
        'accuracy', #(1 = Correct; 2 = Error; 3 = Failed stop; 4 = Successful stop; 5 = Miss)
        'chosen_bidding_amount', # [Phase 3]
        'chosen_bidding_level', # [Phase 3]
        'possible_bid_1', #[Phase 3] in order on screen
        'possible_bid_2', #[Phase 3] in order on screen
        'possible_bid_3', #[Phase 3] in order on screen
        'possible_bid_4', #[Phase 3] in order on screen
        'possible_bid_5', #[Phase 3] in order on screen
        'possible_bid_6'] #[Phase 3] in order on screen

## finding the files in directory specified in path_files, then we are going to look for only data files
## please have a unique identifier for data files, so something like _d.mat, instead of just .mat
onlyfiles = [f for f in os.listdir(path_file) if os.path.isfile(os.path.join(path_file, f))]
mat_files = []
for file in onlyfiles:
    if file[-6:] == '_d.mat':
        mat_files.append(file)

        
## initializing empty arrays for data to be collected
stop_shape_bids = []
go_shape_bids = []
IID_effect = []
subjects = []
collection_locations = []
dates = []

today = date.today()
today_date = today.strftime("%d_%m_%Y")

## let's get the IID effect for each subject      
for mat_file in mat_files:
    mat = loadmat(path_file + mat_file)
    df_p3 = pd.DataFrame(data=mat['trialseq_p3'][:,:], index=list(range(0, 80)), columns=cols[0:23])
    ## getting stop-shapes and go-shapes
    stop_shapes = df_p3.loc[(df_p3['paired_with_stopping'] == 1)]
    go_shapes = df_p3.loc[(df_p3['paired_with_stopping'] == 0)]
    ## getting mean for stop-shapes and go-shapes              
    stop_shape_bids.append(stop_shapes['chosen_bidding_amount'].mean())
    go_shape_bids.append(go_shapes['chosen_bidding_amount'].mean())
    #positive values indicate presence of effect, neg values indicate opposite
    IID_effect.append(go_shapes['chosen_bidding_amount'].mean() - stop_shapes['chosen_bidding_amount'].mean())
    subjects.append(mat_file)
    
    #saving this data
    collection_locations.append(collection_location)
    dates.append(today_date)
    

#Using replication data for distribution of IID effects, let's take out
#subs who's IID effect is greater than 1.5x the interquartile range

#finding iqr
q75, q25 = np.percentile(IID_effect, [75 ,25])
iqr = q75 - q25

#defining cutoffs for IID
upper_cutoff = iqr + iqr * 1.5 
lower_cutoff = iqr - iqr * 1.5 


upper_cutoffs = [upper_cutoff] * len(mat_files)
lower_cutoffs = [lower_cutoff] * len(mat_files)

## turning data into a df to be saved as csv
df = pd.DataFrame(list(zip(subjects, IID_effect, stop_shape_bids, go_shape_bids, collection_locations,dates, upper_cutoffs, lower_cutoffs)), 
               columns =['Subject', 'IID_effect', 'stop_shape_avg_bid', 'go_shape_avg_bid', 'data_collection_location', 'date_script_ran', 'upper_IID_cutoff', 'lower_IID_cutoff'])

## identifying subs that need to be removed
removed_subs = df.loc[(df['IID_effect'] > upper_cutoff) | (df['IID_effect'] < lower_cutoff)]
 
## creating output directory                     
if not os.path.exists(path_file + 'exclusionary_output_dataset/'):
    os.makedirs(path_file + 'exclusionary_output_dataset/')    

## saving data in output directory  
removed_subs.to_csv(path_file + 'exclusionary_output_dataset/' + 'IQR_deval_subject_removal.csv', sep=',')

num_usable_subs = len(df) - len(removed_subs)

## let's print some statements
print('')
print('')  
print('results saved in ' + path_file + 'IQR_deval_subject_removal.csv') 
print('')
print('')               
print('remove these subjects: ' + removed_subs['Subject'])
print('')
print('') 
print('You have ' + str(num_usable_subs) + ' usable subjects out of the intended 79')
