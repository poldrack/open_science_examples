"""
test stop signal estimation procedure
"""

from get_SSRT import sim_stop_data, get_SSRT
import numpy as np
import pandas as pd


def test_SSRT_estimation(threshold=0.95, nruns=100,
                         meanSSRT=0.5, sdSSRT=0.4,
                         ntrials=1000):
    """
    test ssrt estimation by simulating
    data with varying SSRT and p_correct
    """

    results = []
    SSRT = np.random.rand(nruns) * sdSSRT + meanSSRT
    SSRT = SSRT + np.min(SSRT)

    p_correct = 1 - np.random.rand(nruns) * .1

    for i in range(nruns):
        simdata = sim_stop_data(
            SSRT=SSRT[i],
            p_correct=p_correct[i],
            ntrials=ntrials)

        results.append(get_SSRT(simdata))

    df = pd.DataFrame(results)
    cc_SSRT = np.corrcoef(df.SSRT, SSRT)[0, 1]
    assert cc_SSRT > threshold
    cc_pcorr = np.corrcoef(df.pCorrectGoResp, p_correct)[0, 1]
    assert cc_pcorr > threshold
