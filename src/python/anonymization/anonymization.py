#!/usr/bin/env python3.6

"""Data Anonymization Script

This script is used to anonymize the the headers produced by cleaning.py
The data produced by this script must still maintain its machine learning
utility without having enough information to uniquely identify a person

"""

import argparse
import progressbar
import json
from .. import util
import anonymization_functions as af

NUMBER_OF_HEADERS = 251703
ANON_FILE_NAME_ADDITION = '_anon'
FILE_WRITE_MODE = 'w'

def create_arg_parser():
    """ Create and initialise an argument parser for anonymization script. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='Name of clean data file'
    )
    return arg_parser


def read_headers(filename):
    """ Reads the headers from the specified file and returns them as a list """
    # Get number of entries in given dataset file.
    NUMBER_OF_HEADERS = util.file_line_count(filename)
    # Continue reading of headers.
    util.log_print("{} entries found".format(NUMBER_OF_HEADERS))
    headers = []
    counter = 0
    with open(filename) as file:
        with progressbar.ProgressBar(max_value=NUMBER_OF_HEADERS) as bar:
            for line in file:
                headers.append(json.loads(line))
                bar.update(counter)
                counter += 1
    return headers


def write_anaonymized_headers(current_file_name, headers_list):
    """ Writes anonymized headers to a file. """
    # Create new file name from given file name.
    new_file = util.create_new_data_file_name(
        current_file_name,
        ANON_FILE_NAME_ADDITION
    )
    counter = 0
    # Write header content to new file.
    with open(new_file, FILE_WRITE_MODE) as data_file:
        for headers in headers_list:
            data = util.stringify_headers(headers)
            data_file.write('{0}\n'.format(data))
            counter += 1
    util.log_print("{} entries anonymized".format(counter))


def main():
    """ Setup for data anonymization. """
    args = create_arg_parser().parse_args()
    # Read headers into list
    headers = read_headers(args.file)
    # Perform anonymization
    headers = af.anonymize(headers)
    # Write anonymized headers to file.
    write_anaonymized_headers(args.file, headers)


if __name__ == '__main__':
    main()
