"""
extract and prepare stopping and auction data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from get_SSRT import get_SSRT
import argparse


# these are included here for testing
num_stop_trials = 108
num_go_trials = 180


def get_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Reorganize replication data')
    parser.add_argument('-b', '--basedir', required=True,
                        help='base directory')
    return(parser.parse_args())


def find_datafiles(raw_datadir, processed_datadir):
    datafiles = [i for i in raw_datadir.glob('*.tsv')]
    assert len(datafiles) > 0
    print(f'found {len(datafiles)} data files')
    return(datafiles)


def load_data(datafiles):
    data = {}

    for datafile in datafiles:
        subcode = datafile.stem.split('_')[1]
        data[subcode] = pd.read_csv(datafile, sep='\t')
    return(data)


def extract_auctiondata(data):
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
    return(auctiondata)


def remove_practice_trials(subdata):
    subdata['isPracticeTrial'] = 0
    subdata.loc[~subdata['pracTrials.thisRepN'].isna(), 'isPracticeTrial'] = 1
    subdata.loc[~subdata['pracStopTrials.thisRepN'].isna(), 'isPracticeTrial'] = 1
    subdata = subdata.query('isPracticeTrial == 0')
    return(subdata)


def initialize_stoptask_results(datadict):
    nsubs = len(datadict)
    subcodes = [k for k in datadict.keys()]
    subcodes.sort()

    return(pd.DataFrame({
        'goRt_stopStim': np.zeros(nsubs) * np.nan,
        'goRt_goStim': np.zeros(nsubs) * np.nan,
        'SSRT': np.zeros(nsubs) * np.nan,
        'signalRespondRT': np.zeros(nsubs) * np.nan,
        'pSignalRespond': np.zeros(nsubs) * np.nan,
        'pCorrectGo_all': np.zeros(nsubs) * np.nan,
    }, index=subcodes))


def find_stop_trials(subdata):
    subdata.loc[:, 'isStopTaskTrial'] = ~subdata['stimType'].isna()
    subdata.loc[:, 'SSD'] = subdata['stopSignalOnset'].values - subdata['goStimOnset'].values

    # When RTs are > 1s, they are recorded in a different set of columns. RT is in key_resp_9.rt
    # and its accuracy is reflected in key_resp_9.corr. However, to get the appropriate rt value
    # in these instances, you need to add 1s to the value reflected in key_resp_9.rt
    if 'key_resp_9.rt' in subdata:
        subdata.loc[~subdata['key_resp_9.rt'].isna(), 'goResp.rt'] =\
            1 + subdata.loc[~subdata['key_resp_9.rt'].isna(), 'key_resp_9.rt']
        subdata.loc[~subdata['key_resp_9.rt'].isna(), 'goResp.corr'] =\
            1 + subdata.loc[~subdata['key_resp_9.rt'].isna(), 'key_resp_9.corr']
    subdata.loc[subdata['goResp.corr'] > 1, 'goResp.corr'] = 1
    stoptaskDf = subdata.query('isStopTaskTrial == True')

    return(subdata, stoptaskDf)


def check_trial_numbers(subdata, num_stop_trials=108, num_go_trials=180):
    assert np.sum(subdata.trialType == 'go') == num_go_trials
    assert np.sum(subdata.trialType == 'stop') == num_stop_trials


def analyze_go_trials(subcode, stoptaskDf, stoptask_results):
    # compute go RT separately by stimType
    all_go_trials = stoptaskDf.query('trialType == "go"')

    stoptask_results.loc[subcode, 'pCorrectGo_all'] = all_go_trials['goResp.corr'].mean()
    correct_go_trials = all_go_trials.loc[all_go_trials['goResp.corr'] == 1, :]

    # Go RT Stop shapes: same as Go RT except also ensure that “stimType” = stop.
    stoptask_results.loc[subcode, 'goRt_stopStim'] = correct_go_trials.query('stimType == "stop"')['goResp.rt'].mean()

    # Go RT Non-Stop shapes: same as Go RT except also ensure that “stimType” = go.
    stoptask_results.loc[subcode, 'goRt_goStim'] = correct_go_trials.query('stimType == "go"')['goResp.rt'].mean()

    # Stop-Failure RT: Do not include the practice trials but only the main task trials, as in Go RT. Then find the mean of goResp.RT only on trials in which goResp.RT is not an empty cell (i.e., only stop-failures) when “trialType” = stop.
    stoptask_results.loc[subcode, 'stopFailRT'] = stoptaskDf.query('trialType == "stop"')['goResp.rt'].dropna().mean()

    # P(resp|signal) = Again only include main task trials. Then filter for only “trialType” = stop. Then compute the proportion of trials that have a reaction time of any length in goResp.rt
    stoptask_results.loc[subcode, 'pRespSignal'] = 1 - stoptaskDf.query('trialType == "stop"')['goResp.rt'].isna().mean()
    return(stoptask_results)


def estimate_SSRT(subcode, stoptaskDf, stoptask_results):
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
    return(stoptask_results)


def check_stoptask_results(stoptask_results, num_stop_trials=108):
    # check for correct trial nums
    assert np.all(stoptask_results.n_stop_trials == num_stop_trials)

    # for the variables computed in two places, confirm they are equal
    assert np.allclose(stoptask_results.signalRespondRT, stoptask_results.stopFailRT)

    # the analysis from get_SSRT only included go trials from the stop stim condition
    assert np.allclose(stoptask_results.goRt_stopStim, stoptask_results.meanGoRT)

    assert np.all(stoptask_results.pCorrectGo_all <= 1.)


def cleanup_stoptask_results(stoptask_results):
    del stoptask_results['n_stop_trials']
    del stoptask_results['n_go_trials']
    # rename variables from get_SSRT to be clearer about what they mean
    stoptask_results.rename(columns={'pCorrectGoResp': 'pCorrectGo_stopStim',
                                     'pRespSignal': 'pSignalRespond_omissionCorrected'},
                            inplace=True)

    # clean up unnecessary variables
    del stoptask_results['stopFailRT']
    del stoptask_results['meanGoRT']

    # move subcode from index to separate column
    stoptask_results = stoptask_results.reset_index().rename(columns={'index': 'subcode'})
    return(stoptask_results)


def get_stoptask_results(data):
    stoptask_results = initialize_stoptask_results(data)

    for subcode in data:
        data[subcode] = remove_practice_trials(data[subcode])

        data[subcode], stoptaskDf = find_stop_trials(data[subcode])

        check_trial_numbers(data[subcode])

        stoptask_results = analyze_go_trials(subcode, stoptaskDf, stoptask_results)

        stoptask_results = estimate_SSRT(subcode, stoptaskDf, stoptask_results)

    check_stoptask_results(stoptask_results)

    stoptask_results = cleanup_stoptask_results(stoptask_results)

    return(stoptask_results)


if __name__ == '__main__':
    args = get_command_line_arguments()

    raw_datadir = Path(args.basedir) / Path('data/primary_data/study-1')
    processed_datadir = Path(args.basedir) / Path('data/processed_data')

    datafiles = find_datafiles(raw_datadir, processed_datadir)

    data = load_data(datafiles)

    stoptask_results = get_stoptask_results(data)

    stoptask_results.to_csv(processed_datadir / 'study-1_task-stop_data.tsv', sep='\t')

    auctiondata = extract_auctiondata(data)

    auctiondata.to_csv(processed_datadir / 'study-1_task-auction_data.tsv', sep='\t')
