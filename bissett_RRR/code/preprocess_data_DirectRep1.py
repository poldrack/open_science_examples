# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Preprocess auction data for Direct Replication 1

import pandas as pd
import numpy as np
from pathlib import Path
from get_SSRT import get_SSRT

# ## Preprocess data
#
# - load data and extract auction data

# +
# get the data files

basedir = Path('/Users/poldrack/Dropbox/code/open_science_docuthon/bissett_RRR')
datadir = basedir / 'raw_data/wessel_replication_1_OSF'
datafiles = [i for i in datadir.glob('*.csv')]
assert len(datafiles) > 0
print(f'found {len(datafiles)} data files')

# +
# load data for each subject into a dictionary

data = {}

for datafile in datafiles:
    subcode = datafile.stem.split('_')[0]
    data[subcode] = pd.read_csv(datafile)



# +
# extract stop task data
#
# Go RT: do not include the practice trials (which are in rows ~13-22) but only the main task trials (which are in rows ~429-716). Then find the mean RT of all go trials by averaging goResp.rt on trials in which “trialType” = go and goResp.corr = 1

nsubs = len(data)
subcodes = [k for k in data.keys()]
subcodes.sort()

stoptask_results = pd.DataFrame({
    'goRt_stopStim':np.zeros(nsubs)*np.nan,
    'goRt_goStim': np.zeros(nsubs)*np.nan,
    'SSRT': np.zeros(nsubs)*np.nan,
    'signalRespondRT': np.zeros(nsubs)*np.nan,
    'pSignalRespond': np.zeros(nsubs)*np.nan,
    'pCorrectGo_all': np.zeros(nsubs)*np.nan,
}, index=subcodes)

num_stop_trials = 108
num_go_trials = 180

for subcode in data:
    # filter out practice trials
    data[subcode]['isPracticeTrial'] = 0
    data[subcode].loc[~data[subcode]['pracTrials.thisRepN'].isna(), 'isPracticeTrial'] = 1
    data[subcode].loc[~data[subcode]['pracStopTrials.thisRepN'].isna(), 'isPracticeTrial'] = 1
    data[subcode] = data[subcode].query('isPracticeTrial == 0')

    # find stop task trials
    data[subcode].loc[:, 'isStopTaskTrial'] = ~data[subcode]['stimType'].isna()
    data[subcode].loc[:, 'SSD'] = data[subcode]['stopSignalOnset'].values - data[subcode]['goStimOnset'].values
    
    # confirm correct trial numbers
    assert np.sum(data[subcode].trialType=='go') == num_go_trials
    assert np.sum(data[subcode].trialType=='stop') == num_stop_trials

    # create a temporary df to hold stop task data
    stoptaskDf = data[subcode].query('isStopTaskTrial == True')

    # compute go RT separately by stimType
    all_go_trials = stoptaskDf.query('trialType == "go"')
    stoptask_results.loc[subcode, 'pCorrectGo_all'] = all_go_trials['goResp.corr'].mean()
    correct_go_trials = all_go_trials.loc[all_go_trials['goResp.corr']==1, :]

    # Go RT Stop shapes: same as Go RT except also ensure that “stimType” = stop. 
    stoptask_results.loc[subcode, 'goRt_stopStim'] = correct_go_trials.query('stimType == "stop"')['goResp.rt'].mean()

    # Go RT Non-Stop shapes: same as Go RT except also ensure that “stimType” = go. 
    stoptask_results.loc[subcode, 'goRt_goStim'] = correct_go_trials.query('stimType == "go"')['goResp.rt'].mean()

    # Stop-Failure RT: Do not include the practice trials but only the main task trials, as in Go RT. Then find the mean of goResp.RT only on trials in which goResp.RT is not an empty cell (i.e., only stop-failures) when “trialType” = stop. 
    stoptask_results.loc[subcode, 'stopFailRT'] = stoptaskDf.query('trialType == "stop"')['goResp.rt'].dropna().mean()

    # P(resp|signal) = Again only include main task trials. Then filter for only “trialType” = stop. Then compute the proportion of trials that have a reaction time of any length in goResp.rt
    stoptask_results.loc[subcode, 'pRespSignal'] = 1 - stoptaskDf.query('trialType == "stop"')['goResp.rt'].isna().mean()

    # SSRT: This is traditional integration SSRT with two important exceptions. First, omission trials are not included in the underlying go RT distribution and the probability of responding is corrected with the assumption that omissions occur at the same rate on go and stop trials. Verbruggen et al., 2019 argued that SSRT with replacement is a better correction method. I plan to use the new SSRT with replacement on the new data. I could correct the old data too.  Second, I use go RTs from go trials in which the stimulus was associated with stopping. I did this because these tended to slower than go trials in which the stimulus was not associated with stopping, so I believe the former is a better approximation of the underlying go distribution on stop trials. I will share the original Matlab script that did this calculation and the text file inputs to that code. It should be pretty straightforward, but happy to unpack if necessary. In brief, to recreate, you would need the overall probability of responding given a stop signal for each subject (see the previous row of the graph), a rank ordered list of all 36 go trials for stimuli associated with stop (i.e., “trialType” = go and “stimType” = stop), and the mean SSD (mean of “beginningSSD” column on all main task stop trials, i.e., whenever “trialType” = stop). Then integrate up to the Nth percentile of the go RT distribution where N is the probability of a stop signal. However, mind the omission correction on lines 33-37 and 39-43. 

    # drop go RT trials with stimtype == 'go'
    indexNames = stoptaskDf[(stoptaskDf['trialType'] == 'go') & (stoptaskDf['stimType'] == 'go')].index
    estimationDf = stoptaskDf.drop(indexNames)

    # fix column names for SSRT estimation routine
    estimationDf = estimationDf.rename(
        columns={'goResp.rt': 'goRT',
                 'goResp.corr': 'correctResp'})
    estimationDf['signalRespond'] = (stoptaskDf['trialType'] == 'stop') & (~stoptaskDf['goResp.rt'].isna()).astype('int')

    # compute SSRT without replacing omissions
    ssrt_results = get_SSRT(estimationDf, omissionRT=None)
    for i in ssrt_results.index:
        stoptask_results.loc[subcode, i] = ssrt_results[i]

# check for correct trial nums
assert np.all(stoptask_results.n_stop_trials == num_stop_trials)
del stoptask_results['n_stop_trials']
del stoptask_results['n_go_trials']

# for the variables computed in two places, confirm they are equal
assert np.allclose(stoptask_results.signalRespondRT, stoptask_results.stopFailRT)

# these actually mismatch due to omission correction
#assert np.allclose(stoptask_results.pSignalRespond, stoptask_results.pRespSignal)

# the analysis from get_SSRT only included go trials from the stop stim condition
assert np.allclose(stoptask_results.goRt_stopStim, stoptask_results.meanGoRT)

# rename variables from get_SSRT to be clearer about what they mean
stoptask_results.rename(columns={'pCorrectGoResp': 'pCorrectGo_stopStim',
                                 'pRespSignal': 'pSignalRespond_omissionCorrected'},
                        inplace=True)

# clean up unnecessary variables
del stoptask_results['stopFailRT']
del stoptask_results['meanGoRT']

stoptask_results.to_csv(basedir / 'processed_data/wessel_replication_1_stoptask.csv')

# the go results from 
# +
# extract auction phase data for each subject

auctiondata = None
for subcode in data:
    
    tmpdata = data[subcode].loc[~data[subcode].auctionCondition.isna(),
                                    ['auctionStimValue', 'auctionCondition',
                                     'chosenAuctionAmount']]
    tmpdata['subcode'] = subcode
    if auctiondata is None:
        auctiondata = tmpdata
    else:
        auctiondata = pd.concat((auctiondata, tmpdata))
# -

auctiondata.to_csv(basedir / 'processed_data/wessel_replication_1_auction.csv')

