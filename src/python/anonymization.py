#!/usr/bin/env python3.6

"""Data Anonymization Script

This script is used to anonymize the the headers produced by cleaning.py
The data produced by this script must still maintain its machine learning
utility without having enough information to uniquely identify a person

"""

import argparse
import progressbar
import util
import json
import anonymization_functions as af

NUMBER_OF_HEADERS = 251703


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
    util.log_print("Reading Headers")
    headers = []
    counter = 0
    with open(filename) as file:
        with progressbar.ProgressBar(max_value=NUMBER_OF_HEADERS) as bar:
            for line in file:
                headers.append(json.loads(line))
                bar.update(counter)
                counter += 1
    return headers


def main():
    """ Setup for data anonymization. """
    args = create_arg_parser().parse_args()
    # Read headers into list
    headers = read_headers(args.file)
    # Perform anonymization
    headers = af.anonymize(headers)


if __name__ == '__main__':
    main()
