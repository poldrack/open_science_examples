"""
function to compute SSRT

requires a data frame with the following variables:

trialType: 1=stop, 0=go (can use either 1/0 or stop/go)
goRT: response time, should be nan for omissions or successful stop trials
SSD: stop signal delay for that trial (nan for go trials)
signalRespond: 1 for signal respond trials, 0 for successful stop, nan for go trials
correctResp: 1 for correct go-task response, 0 for incorrect, nan for missing responses and successful stops
"""

import numpy as np
import pandas as pd
import scipy.stats


def sim_stop_data(SSRT=.200, p_correct=0.95,
                  p_missing=0.05, starting_ssd=.250, ntrials=256, p_stop=0.33,
                  ssd_step=.050, seed=1, weib_params=None,
                  save_test_data=None):
    """
    simulate stop trials using race model
    """

    if weib_params is None:
        weib_params = {'shape': 2.2,
                       'scale': 0.5,
                       'loc': 0.2}
    rng = np.random.RandomState(seed)

    n_stop_trials = int(ntrials * p_stop)
    n_go_trials = ntrials - n_stop_trials

    # trialType: 0: go, 1:stop
    trialType = np.hstack((np.zeros(n_go_trials), np.ones(n_stop_trials)))
    rng.shuffle(trialType)

    stopDf = pd.DataFrame({'trialType': trialType})
    stopDf['goRT'] = scipy.stats.weibull_min.rvs(
        c=weib_params['shape'],
        scale=weib_params['scale'],
        loc=weib_params['loc'],
        size=ntrials)

    stopDf['correctResp'] = (rng.rand(ntrials) < p_correct).astype(int)
    stopDf['signalRespond'] = np.nan
    stopDf['SSD'] = np.nan

    SSD = starting_ssd

    for i in stopDf.index:
        if stopDf.loc[i, 'trialType'] == 1:  # stop trial
            stopDf.loc[i, 'SSD'] = SSD
            if stopDf.loc[i, 'goRT'] < (SSD + SSRT):
                stopDf.loc[i, 'signalRespond'] = 1
                SSD -= ssd_step
            else:
                stopDf.loc[i, 'signalRespond'] = 0
                stopDf.loc[i, 'correctResp'] = np.nan
                SSD += ssd_step
                stopDf.loc[i, 'goRT'] = np.nan
        elif rng.rand() < p_missing:  # add missing response
            stopDf.loc[i, 'goRT'] = np.nan
            stopDf.loc[i, 'correctResp'] = np.nan
    if save_test_data is not None:
        stopDf.to_csv(save_test_data)
    return(stopDf)


def get_SSRT(df, omissionRT=2.0, verbose=False):
    """
    get SSD for a single subject

    parameters:
    -----------
    stopDf: pandas DataFrame
    omissionRT: float, RT to use for omitted trials, set to None to prevent
    """
    stopDf = df.copy()
    required_columns = ['trialType', 'goRT', 'signalRespond', 'SSD', 'correctResp']
    for c in required_columns:
        assert c in stopDf.columns
        # convert to integer if book
        if stopDf[c].dtype == 'bool':
            if verbose:
                print(f'changing {c} to integer')
            stopDf[c] = [int(i) for i in stopDf[c]]

    # check columns for proper data

    # convert from stop/go to 1/0
    if 'stop' in stopDf.trialType.unique().tolist():
        if verbose:
            print('changing trial type')
        stopDf['trialType'] = [1 if 'stop' in i else 0 for i in stopDf.trialType]

    # compute results
    results = pd.Series(dtype='object')

    stopTrialDf = stopDf.query('trialType == 1')
    results['n_stop_trials'] = stopTrialDf.shape[0]

    goTrialDf = stopDf.query('trialType == 0')
    if verbose:
        print('goTrialDf shape:', goTrialDf)

    # replace go trial omissions with omissionRT if set
    if omissionRT is not None:
        goTrialDf.loc[goTrialDf.goRT.isna(), 'goRT'] = omissionRT

    results['n_go_trials'] = goTrialDf.shape[0]
    results['pCorrectGoResp'] = goTrialDf.correctResp.mean()
    results['meanSSD'] = stopDf.SSD.mean()
    results['meanGoRT'] = goTrialDf.query('correctResp == 1').goRT.mean()
    results['omissionRate'] = np.mean(goTrialDf.goRT.isna())

    # correct for omission rate
    results['pSignalRespond'] = stopTrialDf.signalRespond.mean() / (1 - results['omissionRate'])

    results['signalRespondRT'] = stopTrialDf.query('signalRespond == 1').goRT.dropna().mean()

    # get SSRT using integration method
    # we do not filter out incorrect responses
    correct_go_rts = goTrialDf.goRT.dropna()
    results['SSRT'] = scipy.stats.scoreatpercentile(
        correct_go_rts, 100 * results['pSignalRespond']) - results['meanSSD']

    return(results)


if __name__ == "__main__":
    simdata = sim_stop_data()

    results = get_SSRT(simdata)

    print(results)
