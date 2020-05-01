#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 20:36:41 2019

@author: jamie k li


Instructions for running script:
-This should be ran on an individual subject's data - right after data collection!
-To suppress warnings caused by this file, run as:
    python -W ignore IID_include_sub.py
    
-You will need to modify file_path variable to your dataset location
-The script will prompt you for the .mat file to run through, copy and paste the file to run.



Outline of script:
1) load .mat file into workable python types
    1a) loaded .mat files seem to have this structure:
        [('data', (1, 1), 'struct'),
         ('settings', (1, 1), 'struct'),
         ('trialseq_p1', (400, 11), 'double'),
         ('trialseq_p2', (288, 15), 'double'),
         ('trialseq_p3', (80, 23), 'double'),
         ('output', (1, 1), 'struct')]
         
         1aa) data is a dict that gives NR, age, gender, handedness, and phase 

         1bb) settings is a dict that outlines some parameters for experiment (i.e., which colors, buttons)

         1cc) trialseq_p1, trialseq_p2, and trialseq_p3 are the raw data
                Column 1: Raw reward magnitude [Phase 1]
                Column 2: Shape (1 = low, no stop; 2 = mid low, no stop; 3 = mid high, no stop…)
                Column 3: Stepwise reward magnitude (1 - 4)
                Column 4: Generally paired with stopping or not?
                Column 5: Shape (triangle, flipped triangle, square, diamond, cross, hexagon, I, circle)
                Column 6: Color (green, blue, cyan, magenta, yellow, orange, white, gray)
                Column 7: Quadrant (1 = top L; 2 = top R; 3 = bottom R; 4 = bottom L; 5 = L; 6 = R)
                Column 8: Response (1 = top L; 2 = top R; 3 = bottom R; 4 = bottom L; 5 = L; 6 = R)
                Column 9: Reaction Time
                Column 10: Block
                Column 11: Number of trial presentations (errors and misses are replayed in Phase 1)
                Column 12: Stop Signal? [Phase 2]
                Column 13: Left SSD [Phase 2]
                Column 14: Right SSD [Phase 2]
                Column 15: Accuracy (1 = Correct; 2 = Error; 3 = Failed stop; 4 = Successful stop; 5 = Miss)
                Column 16: Bidding amount chosen [Phase 3]
                Column 17: Bidding level chosen [Phase 3]
                Col. 18-23: Possible bids (in order on screen) [Phase 3]

         1dd) output is a dict that contains 3 dicts, one for each part, p1, p2, and p3 of the experiment.
              each dict gives basic descriptive stats for that phase:
              RT, stop-success, stop-fail, stim info, etc..
            
2) After we get data into a workable format, apply following exclusion criteria:
    (1) stop-failure RTs >= no-stop-signal RT, 
    (2) SSRT < 100 ms, Instead of calculating mean SSRT, we will calculate integration SSRT 
        with replacement, as suggested by a recent consensus guide for the 
        stop-signal task (Verbruggen et al., 2019). Additionally, when computing 
        SSRT, we will use the reaction times to stop shapes as the underlying 
        go distribution on stop trials, as we did in the Supplement. We found 
        that RTs tends to be slower to stop than non-stop shapes, so 
        no-stop-signal RTs on only stop shapes should act as a better, more 
        specific estimate of the underlying go distribution on stop trials. 
   

        
3) Script will check each of the conditions above, and output 'include' or 'exclude'
    1. will also output the subject_vector (which criteria sub passed [1-pass, 0-fail]) as a .txt file.
    This .txt file will be in a folder called 'exclusionary_output_individual_subject' that's 
    located in the directory your data is in (or as specified in file_path variable)
    
       
"""
##################################
#           IMPORTS
##################################

import scipy.io as spio
import numpy as np 
import pandas as pd
import os
import json
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
##file path for .mat file - change to point to the new data directory
file_path = '/Users/jamie/Documents/IIDDataForJamieApril292019/WesselReplication2/GoodData/'
#please put where collection took place, Stanford University, Tel Aviv University, or Missouri Western State University
#please put as stanford, tel_aviv, and missouri_western_state! For now, it will be blank
#this is used in the data description json made at the end
dataset_collection_place = ''
mat_file = input('Which subject? ')
##The following loads in the .mat file and turns it into python dicts
mat = loadmat(file_path + mat_file)


##min SSRT for inclusion. 
minSSRTCutoff = 100 #ms
##For each subject, we will construct a vector of size 2 containing 0 or 1s, called subject_vector
##subject_vector appends a 1 for every passed criteria and 0 for every failed criteria
##at the end, we will check if subject_vector == include_vector, and if it does, the sub passed all criteria
subject_vector = []
##include_vector should have 2 1's, 1 for each of the criteria
include_vector = [1,1] 
 

##Cols were taken from Stop Devaluation Manual by Wessel (2015)
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

df_p2 = pd.DataFrame(data=mat['trialseq_p2'][:,:], index=list(range(0, 288)), columns=cols[0:15])

##################################
#           SCRIPT
##################################

## calc stop-failure >= no-stop-signal RT
stop_failure_trials = df_p2.loc[(df_p2['accuracy'] == 3)]                          
no_stop_signal_trials_go_shapes = df_p2.loc[(df_p2['paired_with_stopping'] == 0)] 
no_stop_signal_trials_stop_shapes = df_p2.loc[(df_p2['paired_with_stopping'] == 1) & (df_p2['stop_signal_trial_type'] == 0)]
no_stop_signal_trials_all_shapes = df_p2.loc[(df_p2['stop_signal_trial_type'] == 0)]

                                  
meanRT_stop_fail = stop_failure_trials['reaction_time'].mean()
meanRT_no_stop_trials_all_shapes = no_stop_signal_trials_all_shapes['reaction_time'].mean()
## 2 lines below not necessary, so I commented it out
#meanRT_no_stop_trials_go_shapes = no_stop_signal_trials_go_shapes['reaction_time'].mean()
meanRT_no_stop_trials_stop_shapes = no_stop_signal_trials_stop_shapes['reaction_time'].mean()

## appending to subject_vector whether this sub passed stop_fail_RT < no_stop_RT criterion
if meanRT_stop_fail >= meanRT_no_stop_trials_stop_shapes:
    subject_vector.append(0)
else:
    subject_vector.append(1)
    
'''       
calc SSRT - there are two SSD tracking procedures, one for left stims and the other for right stims.
The following SSRT calculations are separated by these two SSD tracking procedures, 
so I get an SSRT for left stims and an SSRT for right stims, and then I use the avg of those two as final SSRT.
I also calculate SSRT over all trials - ignoring the two tracking procedures, just out of curiousity


need to get trials where stop shapes are presented w.o stop-signal - these are the specified go_trials
if they don't respond on the above trials, i.e., miss, we need to replace those missing vals with
the highest allowable time (max response time for trial, or 1sec)
get their p(respond | stop-signal), and get the nth rt from stop shapes are presented w.o stop-signal that corresponds to this value
so if their p(respond|SS) = .50 and there were 100 go trials, we should get the RT that has rank of 50 when sorted.  
rank = p(respond|SS) * # go trials
nth_rt - SSD = SSRT
'''

## we need all trials with a stop-signal
trials_with_SS = df_p2.loc[(df_p2['stop_signal_trial_type'] == 1)] 
## these are all trials with a stop-signal that had a stim on the left quadrant
trials_with_SS_left = trials_with_SS.loc[(trials_with_SS['quadrant'] == 5)] 
## these are all trials with a stop-signal that had a stim on the right quadrant
trials_with_SS_right = trials_with_SS.loc[(trials_with_SS['quadrant'] == 6)] 

## prob of responding given a stop-signal - first index is the 0 response, 
## so we do (all SS trials - successful stops / all SS trials) to  get prob of responding                  
pRespond_given_SS = (len(trials_with_SS) - trials_with_SS.groupby('response').count().iloc[0].accuracy) / len(trials_with_SS)
## Do it for the left shapes
pRespond_given_SS_left = (len(trials_with_SS_left) - trials_with_SS_left.groupby('response').count().iloc[0].accuracy) / len(trials_with_SS_left)
## Also for the right shapes
pRespond_given_SS_right = (len(trials_with_SS_right) - trials_with_SS_right.groupby('response').count().iloc[0].accuracy) / len(trials_with_SS_right)


## let's get rank, given by P(respond | SS) * number no-stop trials for stop shapes
rank = round(pRespond_given_SS * len(no_stop_signal_trials_stop_shapes)) 
## The following two lines divide the no-stop-signal trials into 2, one for left stims and the other for right stims
rank_left_trials = no_stop_signal_trials_stop_shapes.loc[(no_stop_signal_trials_stop_shapes['quadrant'] == 5)]
rank_right_trials = no_stop_signal_trials_stop_shapes.loc[(no_stop_signal_trials_stop_shapes['quadrant'] == 6)]
## We are replacing missed no-stop trials with the maximum response time, 1 second
no_stop_signal_trials_stop_shapes['reaction_time_replaced'] = np.where(no_stop_signal_trials_stop_shapes['reaction_time'] == 0, 1, no_stop_signal_trials_stop_shapes['reaction_time'])
rank_left_trials['reaction_time_replaced'] = np.where(rank_left_trials['reaction_time'] == 0, 1, rank_left_trials['reaction_time'])
rank_right_trials['reaction_time_replaced'] = np.where(rank_right_trials['reaction_time'] == 0, 1, rank_right_trials['reaction_time'])
## after we get no-stop-signal trials for stop shapes with stims presented on the left, we can get the rank_left                                                          
rank_left = round(pRespond_given_SS_left * len(rank_left_trials))
## also for rank_right                                                          
rank_right = round(pRespond_given_SS_right * len(rank_right_trials)) 
  
## let's get the Nth_rt that corresponds to the rank - this is choosing from all no-stop-signal trials for stop stims
Nth_RT = no_stop_signal_trials_stop_shapes.sort_values(by=['reaction_time_replaced']).iloc[int(rank)].reaction_time_replaced * 1000
## now choosing from just no-stop-signal trials for stop stims presented on the left, using rank_left
Nth_RT_left = rank_left_trials.sort_values(by=['reaction_time_replaced']).iloc[int(rank_left)].reaction_time_replaced * 1000
## now choosing from just no-stop-signal trials for stop stims presented on the right, using rank_right
Nth_RT_right = rank_right_trials.sort_values(by=['reaction_time_replaced']).iloc[int(rank_right)].reaction_time_replaced * 1000

## get avg SSD across all trials - making sure not to double count SSD's
avg_SSD = (rank_left_trials['left_SSD'].mean() + rank_right_trials['right_SSD'].mean()) / 2
## get avg SSD for left no-stop-signal stop trials
avg_SSD_left = rank_left_trials['left_SSD'].mean()
## get avg SSD for right no-stop-signal stop trials
avg_SSD_right = rank_right_trials['right_SSD'].mean()

## This SSRT was calculated ignoring the separate tracking procedure
SSRT = Nth_RT - avg_SSD
## This SSRT was calculated by getting (SSRT_left + SSRT_right) / 2
SSRT_left_right = ((Nth_RT_left - avg_SSD_left) + (Nth_RT_right - avg_SSD_right) )/ 2
#SSRT_left = Nth_RT_left - avg_SSD_left
#SSRT_right = Nth_RT_right - avg_SSD_right


## appending to subject_vector whether this sub passed SSRT criterion
if SSRT < minSSRTCutoff:
    subject_vector.append(0)
else:
    subject_vector.append(1)
  
    
 
    
    

## collecting info to be saved
today = date.today()
today_date = today.strftime("%d_%m_%Y")
data_info = {'subject': mat_file,
             'race_model_criteria': subject_vector[0],
             'ssrt_criteria': subject_vector[1],
             'meanRT_no_stop_trials_stop_shapes' : round(meanRT_no_stop_trials_stop_shapes * 1000),
             'meanRT_stop_fail': round(meanRT_stop_fail * 1000),
             'SSRT': int(round(SSRT)),
             'include': subject_vector == include_vector,
             'date_subject_passed': today_date,
             'description': 'sub passed criteria if the value = 1, failed = 0. 2 criteria: stopFailRT < noStopRT and ssrt > 99',
             'dataset': 'IID_' + dataset_collection_place}
             
    
## creating output directories
if not os.path.exists(file_path + 'exclusionary_output_individual_subject/'):
    os.makedirs(file_path + 'exclusionary_output_individual_subject/')
    

## saving info in output directory
with open(file_path + 'exclusionary_output_individual_subject/' + mat_file + '.json', 'w') as outfile:
    json.dump(data_info, outfile)

## this loads the outputted info back in as a df - making sure that data is transferable and others can have access if they need
with open(file_path + 'exclusionary_output_individual_subject/' + mat_file + '.json', 'r') as f:
    data = json.load(f)
## turns info into a dataframe       
json_df = pd.DataFrame({'sub_' + mat_file: data}).T
    

##  Let's print some output
if subject_vector == include_vector:
    print('include - subject passed all criteria')
else:
    print('exclude - subject did not pass all criteria')
 
    
print('')
print('')    
print('output saved in /exclusionary_output_individual_subject/' + mat_file + '.txt')