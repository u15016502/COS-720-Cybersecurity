#!/usr/bin/env python3.6

"""Exploratory Data Analysis Script

This script performs exploratory data analysis on
the headers produced by cleaning.py

"""

import json
import argparse
import scripts.analysis_functions as af


def create_arg_parser():
    """ Create and initialise an argument parser for analysis script. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='Name of clean data file'
    )
    return arg_parser


def read_headers(filename):
    headers = []
    with open(filename) as file:
        for line in file:
            headers.append(json.loads(line))
    return headers


def main():
    """ Setup for data analysis. """
    args = create_arg_parser().parse_args()
    # Read headers into list
    headers = read_headers(args.file)
    # Get Subject Word Cloud
    # af.analyze_subjects(headers, ["no_subject", "FW", "RE"])
    # Find different Content-Types
    # af.analyze_content_types(headers, False)
    # Find different charsets
    # af.analyze_content_types(headers, True)
    # Check on which day most emails are sent
    # af.analyze_days(headers)
    # Check in which month most emails were sent
    # af.analyze_months(headers)
    # Check in which years most emails were sent
    # af.analyze_years(headers)
    # Check at what tme most emails were sent
    # af.analyze_times(headers)
    af.get_max_senders(headers, 20)


if __name__ == '__main__':
    main()
