"""
organize data for Direct Replication 2
from original data files (obtain from OSF)
into Psych-DS (ish) format

study-2/
    study-2_sub-<subnum>_data.tsv
"""


from utils import (get_command_line_arguments,
                   get_directories,
                   get_datafiles,
                   load_and_resave_datafiles)


if __name__ == "__main__":
    args = get_command_line_arguments()
    args = get_directories(
        args)
    args = get_datafiles(args)
    load_and_resave_datafiles(args)
