"""
utility functions for replication analysis
"""

import argparse


def get_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Reorganize replication data')
    parser.add_argument('-b', '--basedir', required=True,
                        help='base directory')
    return(parser.parse_args())
