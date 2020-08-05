"""
organize data for Direct Replication 2
from original data files (obtain from OSF)
into Psych-DS (ish) format

study-2/
    study-2_sub-<subnum>_data.tsv
"""

import argparse
from utils import (get_directories,
                   get_datafiles,
                   load_and_resave_datafiles)


def get_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Reorganize replication data')
    parser.add_argument('-b', '--basedir', required=True,
                        help='base directory')
    parser.add_argument('--studynum',
                        default=1,
                        type=int,
                        help='study number')
    parser.add_argument('--studyname',
                        default='wessel_replication_1_OSF',
                        help='study name')
    return(parser.parse_args())


if __name__ == "__main__":
    args = get_command_line_arguments()
    args = get_directories(
        args)
    args = get_datafiles(args)
    load_and_resave_datafiles(args)
