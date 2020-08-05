"""
utility functions for replication analysis
"""

import argparse
import pandas as pd
from pathlib import Path, PosixPath


def get_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Reorganize replication data')
    parser.add_argument('-b', '--basedir', required=True,
                        help='base directory')
    parser.add_argument('--studynum',
                        required=True, type=int,
                        help='study number')
    parser.add_argument('--studyname',
                        required=True,
                        help='study name')
    return(parser.parse_args())


def get_directories(args):
    if type(args.basedir) != PosixPath:
        args.basedir = Path(args.basedir)
    assert args.basedir.exists()

    setattr(args, 'datadir',
            args.basedir / 'data')
    setattr(args, 'rawdir',
            args.datadir / 'primary_data/source_data')
    setattr(args, 'sourcedir',
            args.rawdir / args.studyname)
    assert args.sourcedir.exists()

    setattr(args, 'outdir',
            args.datadir / str('primary_data/study-%d' % args.studynum))
    if not args.outdir.exists():
        args.outdir.mkdir()

    setattr(args, 'logdir', args.basedir / 'logs')
    if not args.logdir.exists():
        args.logdir.mkdir()
    return(args)


def load_and_resave_datafiles(args):

    for d in args.datafiles:
        data = pd.read_csv(d)
        subcode = int(d.stem.split('_')[0])
        outfile = args.outdir / ('study-%d_sub-%03d_data.tsv' % (args.studynum, subcode))
        data.to_csv(outfile, sep='\t')


def get_datafiles(args):
    setattr(args, 'datafiles', [i for i in args.sourcedir.glob('*.csv')])
    return(args)
