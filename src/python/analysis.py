#!/usr/bin/env python3.6

"""Exploratory Data Analysis Script

This script performs exploratory data analysis on
the headers produced by cleaning.py

"""

import json
import argparse
import progressbar
import util
import analysis_functions as af

NUMBER_OF_HEADERS = 251703


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


def bulk_analyze(headers):
    """ Perform all analysis techniques on the provided email headers """
    # Get Subject Word Cloud
    af.analyze_subjects(headers, ["no_subject", "FW", "RE"])
    # Find different Content-Types
    af.analyze_content_types(headers, False)
    # Find different charsets
    af.analyze_content_types(headers, True)
    # Check on which day most emails are sent
    af.analyze_days(headers)
    # Check in which month most emails were sent
    af.analyze_months(headers)
    # Check in which years most emails were sent
    af.analyze_years(headers)
    # Check at what tme most emails were sent
    af.analyze_times(headers)
    # Check who sent the most emails
    af.get_max_senders(headers, 10)
    # Check which are the most common domains that sent emails
    af.analyze_domains(headers, 5)


def main():
    """ Setup for data analysis. """
    args = create_arg_parser().parse_args()
    # Read headers into list
    headers = read_headers(args.file)
    # Perform basic analysis on the full data set
    af.analyze_basic(headers)
    # Perform exploratory analysis on full data set
    util.log_print("Performing Analysis on the Full Data Set")
    bulk_analyze(headers)
    # Perform analysis on emails sent to multiple recipients
    util.log_print("Performing Analysis on Emails Sent to Multiple Recipients")
    multiple_rec_headers = list(filter(lambda h: len(h["To"]) > 1, headers))
    bulk_analyze(multiple_rec_headers)
    # Perform analysis on emails sent to a single recipient
    util.log_print("Performing Analysis on Emails Sent to a Single Recipient")
    single_rec_headers = list(filter(lambda h: len(h["To"]) == 1, headers))
    bulk_analyze(single_rec_headers)


if __name__ == '__main__':
    main()
