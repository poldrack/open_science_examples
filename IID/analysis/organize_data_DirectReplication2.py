"""
organize data for Direct Replication 1
from original data files (obtain from OSF)
into Psych-DS (ish) format

study-1/
    study-1_sub-<subnum>_data.tsv
"""


from pathlib import Path
import pandas as pd

basedir = Path('..')
rawdir = basedir / 'raw_data'
sourcedir = rawdir / 'source_data/wessel_replication_2_OSF'
assert sourcedir.exists()

outdir = rawdir / 'study-2'
if not outdir.exists():
    outdir.mkdir()

logdir = Path('logs')
if not logdir.exists():
    logdir.mkdir()


# get data files

datafiles = [i for i in sourcedir.glob('*.csv')]

# get new filename/paths for each data file

rename_dict = {}

for d in datafiles:
    data = pd.read_csv(d, sep='\t', index_col=0)
    subcode = d.stem.split('_')[0]
    outfile = outdir / ('study-2_sub-%s_data.tsv' % subcode)
    data.to_csv(outfile, sep='\t')
