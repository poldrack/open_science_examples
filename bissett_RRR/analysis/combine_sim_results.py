
import pandas as pd
from pathlib import Path

# load files

datadir = Path('../processed_data/powersim')
csvfiles = [i for i in datadir.glob('*.csv')]

results_sim = None
for f in csvfiles:
    d = pd.read_csv(f, index_col=0)
    if results_sim is None:
        results_sim = d
    else:
        results_sim = pd.concat((results_sim, d))

results_sim.to_csv('../processed_data/combined_powersim_results.csv')
