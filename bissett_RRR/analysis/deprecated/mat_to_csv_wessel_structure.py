#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:59:18 2019

@author: jamie

This file takes a .mat file with the structure given by Wessel et al. (2014) 
and turns them into csv files.  Each .mat file will give out two csv files:
    1) data.csv has all trial data
    2) demographics.csv has all other data that is not trial data

The demographics.csv file will be listed in a newly created sub-directory within the data.csv files

path_dir (under variables portion) takes the path to the directory with the .mat files
-this should be changed to point to the new directory!

new_dir (under variables portion) is where we will save the newly constructed .csv files
-this should also be changed to your new desired location!

"""
    
##################################
#           IMPORTS
##################################

import pandas as pd
import os
import scipy.io as spio


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
#           VARIABLES
##################################

path_file = '/Users/jamie/Documents/IIDDataForJamieApril292019/only_IID/WesselReplication2/GoodData/wessel_replication_2_OSF/bad_data/'

new_dir =   '/Users/jamie/Documents/IIDDataForJamieApril292019/only_IID/WesselReplication2/GoodData/wessel_replication_2_OSF_2/bad_data/'


##################################
#              SCRIPT
##################################

if not os.path.exists(new_dir + 'experiment_info/'):
        os.makedirs(new_dir + 'experiment_info/') 
        
        
onlyfiles = [f for f in os.listdir(path_file) if os.path.isfile(os.path.join(path_file, f))]
mat_files = []
for file in onlyfiles:
    if file[-4:] == '.mat':
        mat_files.append(file)
        


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


df_p1_col = ['part_1'] * 400
df_p2_col = ['part_2'] * 288
df_p3_col = ['part_3'] * 80

df_settings_col = ['settings']*42
df_output_col = ['output']*15

for mat_file in mat_files:
    mat = loadmat(path_file + mat_file)
    
    # This part concatenates trial data for p1, p2, and p3, then saves as CSV file
    df_p1 = pd.DataFrame(data=mat['trialseq_p1'][:,:], index=list(range(0, 400)), columns=cols[0:11])
    df_p1['which_part'] = df_p1_col
    
    df_p2 = pd.DataFrame(data=mat['trialseq_p2'][:,:], index=list(range(0, 288)), columns=cols[0:15])
    df_p2['which_part'] = df_p2_col
    
    df_p3 = pd.DataFrame(data=mat['trialseq_p3'][:,:], index=list(range(0, 80)), columns=cols[0:23])
    df_p3['which_part'] = df_p3_col
    
    
    df_trials_concat = pd.concat([df_p1,df_p2,df_p3])
    
    df_trials_concat.to_csv(new_dir + mat_file + '.csv', sep='\t')
    
    
    
    # This part transforms non-trial info to csv file. Saves demographics, settings, and output 
    df_settings = pd.DataFrame.from_dict(mat['settings'])
    df_settings['which_info'] = df_settings_col
    
    df_output = pd.DataFrame.from_dict(mat['output'])
    df_output['which_info'] = df_output_col
    
    df_data = pd.DataFrame({'count': mat['data']}).T
    df_data['which_info'] = ['data']
    
    
    df_demo = pd.concat([df_data,df_output,df_settings])
     
    
    df_demo.to_csv(new_dir + 'experiment_info/' + mat_file + '.csv', sep='\t')

print('')
print('')    
print('csv files saved in ' + new_dir)
print('')
print('')
print('experiment information saved in ' + new_dir + 'experiment_info/')
   

