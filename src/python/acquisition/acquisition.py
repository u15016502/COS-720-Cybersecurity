#!/usr/bin/env python3.6

"""Email header acquisition script

This script is used to acquire email headers from plain text
email files that are specified as arguments.

The script reads the email files and only acquires the headers,
ignoring the email body.

Note: The script sometimes references the word 'data' and it
is important, therefore, to note that in this script the word
'data' generally refers to email headers and their associated
values.

"""

import argparse
import os
import queue
import re
import sys
import time
from multiprocessing import Pool, Queue

sys.path.append('src/python')
import util

FILE_READ_MODE = 'r'
FILE_WRITE_MODE = 'w'
QUEUE_TIMEOUT = 1.5
POOL_PROCESSOR_COUNT = 7

data_to_write_queue = None
data_reader = None
email_headers = None


def create_arg_parser():
    """ Create and initialise an argument parser for acquisition script. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-p',
        '--path',
        required=True,
        help='Path to email files for header acquisition'
    )
    arg_parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='Name of output data file'
    )
    arg_parser.add_argument(
        '-i',
        '--ignore_x_headers',
        action='store_true',
        help='Ignore X headers'
    )
    return arg_parser


def create_header_map():
    """ Create and initialise a header map to fill from email file. """
    global email_headers
    return { header: [] for header in email_headers }


def split_header_line(header_line):
    """ Splits header line into header and header values. """
    # Split line on ':' to get header key-value pair.
    split_line = header_line.split(':')
    header = split_line[0].strip()
    # If the line has multiple ':' characters (such as is common in
    # subject lines) join all values that have been split after the
    # first ':'.
    return header, [':'.join(split_line[1:]).strip()]


def reader(read_file):
    """ Reader function for email headers excluding x-headers. """
    header_map = create_header_map()
    header_values = None
    header = None
    # Iterate through the email file line by line to extract headers.
    # Stop once an empty line has been found (end of headers), or once
    # a x-header is encounter.
    for line in read_file:
        # Check if header value continues on a new line as opposed to
        # encountering a new header or stopping condition.
        if line[:1] == '\t' or line[:1] == ' ':
            header_values.append(line.strip())
            continue
        if not header == None:
            header_map[header] = header_values
        if line[:2] == 'X-' or line == '\n':
            # Not the best solution since it relies on assumption, but it
            # will do.
            if 'X-From' in header_map:
                header, header_values = split_header_line(line)
                header_map[header] = header_values
            break
        header, header_values = split_header_line(line)
    # Return a populated map of header values.
    return header_map


def x_header_inclusive_reader(read_file):
    """ Reader function for email headers including x-headers. """
    # Re-use of basic, non-x-header-inclusive reader.
    header_map = reader(read_file)
    header_values = None
    header = None
    # Similar process is followed as for the above basic, non-x-header-
    # inclusive reader.
    for line in read_file:
        if line[:1] == '\t' or line[:1] == ' ':
            header_values.append(line.strip())
            continue
        if not header == None:
            header_map[header] = header_values
        if line == '\n':
            break
        header, header_values = split_header_line(line)
    return header_map


def create_data_reader(ignore_x_headers):
    """ Return relevant email header reader. """
    return x_header_inclusive_reader if not ignore_x_headers else reader


def initialise_global_variables(ignore_x_headers):
    """ Initialise global variables for use throughout the script. """
    global data_to_write_queue
    global data_reader
    global email_headers
    data_to_write_queue = Queue()
    data_reader = create_data_reader(ignore_x_headers)
    combined_headers = util.EMAIL_HEADERS + util.EMAIL_X_HEADERS
    email_headers = combined_headers if not ignore_x_headers else util.EMAIL_HEADERS


def get_email_file_names(directory):
    """ Recursively collect all file names in specified directory. """
    file_names = []
    # Create spinner to show that script is busy processing.
    spinner = util.Spinner('Seeking files in directory: "{0}"'.format(directory))
    spinner.start()
    # Perform a recursive walk in specified directory.
    for directory_path, directories, files in os.walk(directory):
        for file_name in files:
            file_names.append(os.path.join(directory_path, file_name))
    spinner.stop()
    util.log_print('Found {0} files in "{1}"'.format(
        len(file_names),
        directory
    ))
    return file_names


def get_headers_from_file(file_name):
    """ Retrieves from a specified file and adds said headers to a write queue. """
    global data_to_write_queue
    global data_reader
    # Attempt to open and read given file.
    try:
        # Open file, use data reader and add returned data map to write queue.
        with open(file_name, FILE_READ_MODE) as read_file:
            data_to_write_queue.put(data_reader(read_file))
    # If something went wrong, simply ignore the contents of the file.
    # Not the most ideal solution, but it is the simplest.
    except:
        pass


def write_to_data_file(data_file_name, num_files):
    """ Retrieves data maps from write queue and appends it to specified data file. """
    global data_to_write_queue
    progress_bar = util.ProgressBar(num_files, 'Extracting headers', 73)
    counter = 0
    with open(data_file_name, FILE_WRITE_MODE) as data_file:
        while True:
            # Keep retrieving header data from write queue until timeout exception
            # is raised (should mean that no more data will be added to the queue).
            try:
                data = data_to_write_queue.get(block=True, timeout=QUEUE_TIMEOUT)
                stringified_data = util.stringify_headers(data)
                data_file.write('{0}\n'.format(stringified_data))
                counter += 1
                # Update progress bar.
                progress_bar.update(counter)
            except queue.Empty:
                # Finish up the writing process.
                progress_bar.clean()
                util.log_print('{0} entries written in "{1}"'.format(
                    counter,
                    data_file_name
                ))
                break
            except Exception as error:
                print(error)
                util.log_print('{0} entries written in "{1}"'.format(
                    counter,
                    data_file_name
                ))
                break


def acquire_headers_and_write(directory, data_file_name):
    """ Retrieve email headers and write headers to data file. """
    # Setup a worker pool for reading email files.
    pool = Pool(POOL_PROCESSOR_COUNT)
    # Get email file names in specified root directory.
    email_file_names = get_email_file_names(directory)
    num_email_files = len(email_file_names)
    # Assign files to worker pool for concurrent processing.
    pool.imap(get_headers_from_file, email_file_names)
    # Write header data from write queue.
    write_to_data_file(data_file_name, num_email_files)
    # Clean up processing pool and wait for it to finish up.
    pool.terminate()


def main():
    """ Setup script for header extraction and writing. """
    args = create_arg_parser().parse_args()
    initialise_global_variables(args.ignore_x_headers)
    start_time = time.time()
    acquire_headers_and_write(args.path, args.file)
    end_time = time.time()
    execution_time = (end_time - start_time - QUEUE_TIMEOUT) / 60
    util.log_print('{0:.4f} min'.format(execution_time))


if __name__ == '__main__':
    main()
