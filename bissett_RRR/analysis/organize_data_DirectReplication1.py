"""
organize data for Direct Replication 1
from original data files (obtain from OSF)
into Psych-DS (ish) format

study-1/
    study-1_sub-<subnum>_data.tsv
"""


from pathlib import Path, PosixPath
import pandas as pd
from utils import get_command_line_arguments


def get_directories(args):
    if type(args.basedir) != PosixPath:
        args.basedir = Path(args.basedir)
    assert args.basedir.exists()

    setattr(args, 'rawdir', args.basedir / 'raw_data')
    setattr(args, 'sourcedir', args.rawdir / 'source_data/wessel_replication_1_OSF')
    assert args.sourcedir.exists()

    setattr(args, 'outdir', args.rawdir / 'study-1')
    if not args.outdir.exists():
        args.outdir.mkdir()

    setattr(args, 'logdir', args.basedir / 'logs')
    if not args.logdir.exists():
        args.logdir.mkdir()
    return(args)


def get_datafiles(args):
    setattr(args, 'datafiles', [i for i in args.sourcedir.glob('*.csv')])
    return(args)


def load_and_resave_datafiles(args):

    for d in args.datafiles:
        data = pd.read_csv(d)
        subcode = d.stem.split('_')[0]
        outfile = args.outdir / ('study-1_sub-%s_data.tsv' % subcode)
        data.to_csv(outfile, sep='\t')


if __name__ == "__main__":

    args = get_command_line_arguments()
    args = get_directories(args)
    args = get_datafiles(args)
    load_and_resave_datafiles(args)
