#!/usr/bin/env python3.6

"""Email header cleaning script

This script is used to clean email headers from plain text
data file produced by the acquisition.py script.

The script cleans the data entries and writes the cleaned data
entries in a new file in the same directory as the unclean data
file.

Note: The script sometimes references the word 'data' and it
is important, therefore, to note that in this script the word 
'data' generally refers to email headers and their associated
values.

"""

import argparse
import cleaning_functions
import copy
import os
import sys
import time
import traceback
import util
from multiprocessing import Lock, Manager, Process, Pool, Queue, Value

FILE_READ_MODE = 'r'
FILE_WRITE_MODE = 'w'
CLEAN_FILE_NAME_ADDITION = '_clean'
QUEUE_TIMEOUT = 1.5
POOL_PROCESSOR_COUNT = 6

data_to_write_queue = None
unique_data_set = None
number_of_data_lines = None
modify_global_mutex = None


def create_arg_parser():
    """ Create and initialise an argument parser for cleaning script. """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='Name of unclean data file'
    )
    return arg_parser


def is_file(file_name):
    """ Determines whether the given file exists. """
    return os.path.isfile(file_name)


def check_is_valid_file(file_name):
    """ Check if the specified file exists. """
    # If the file does not exist, let the user know and exit the script.
    if not is_file(file_name):
        util.log_print('File "{0} does not exist"'.format(file_name))
        sys.exit()


def initialise_global_variables(unclean_data_file_name):
    """ Initialise global variables for use throughout the script. """
    global data_to_write_queue
    global unique_data_set
    global number_of_data_lines
    global modify_global_mutex
    data_to_write_queue = Queue()
    unique_data_set = Manager().dict()
    number_of_data_lines = Value('i', util.file_line_count(unclean_data_file_name))
    modify_global_mutex = Lock()


def is_unique_entry(data_map):
    """ Checks to see if the given data map is a unique entry within the dataset. """
    global unique_data_set
    global modify_global_mutex
    # Create hash to check for uniqueness.
    data_hash = util.hash_data(data_map)
    if data_hash not in unique_data_set:
        # Acquire lock and add the hash.
        with modify_global_mutex:
            unique_data_set[data_hash] = True
        return True
    # Entry is not unique.
    return False


def is_valid_header_entry(header_map):
    """ Determines whether a given header map is a valid data entry. """
    for header in header_map:
        # Check if the current header exists as a header specified for
        # cleaning, and assume that if the header is present in said
        # cleaning map, that it is valid.
        # This of course also assumes that all valid headers are contained
        # within the cleaning map.
        if header not in cleaning_functions.HEADER_CLEANING_MAP:
            return False
    # Entry is assumed to be valid if this point is reached.
    return True


def clean_data_map(data_map):
    """ Cleans data by mutating the given data map. """
    # Get header and associated cleaning functions from the cleaning map.
    for header, cleaners in cleaning_functions.HEADER_CLEANING_MAP.items():
        map_copy = copy.deepcopy(data_map)
        header_values = data_map[header]
        # Apply cleaning functions on header values.
        for cleaner in cleaners:
            header_values = cleaner(header, header_values, map_copy)
        # Save clean header values in data map.
        data_map[header] = header_values


def clean_data_line(unclean_data_line):
    """ Clean given data line. """
    global data_to_write_queue
    global number_of_data_lines
    # Parse given data line.
    data_map = util.parse_headers(unclean_data_line)
    # Check if if the data map is valid, not malformed and unique.
    if is_valid_header_entry(data_map) and is_unique_entry(data_map):
        try:
            # Clean the data map (parsed headers).
            clean_data_map(data_map)
            # Stringify the cleaned data map.
            cleaned_data_line = util.stringify_headers(data_map)
            # Add cleaned, stringified data to data write queue.
            data_to_write_queue.put(cleaned_data_line, False)
        # If something went wrong, ignore the data entry.
        except Exception:
            number_of_data_lines.value -= 1
    # If the data entry is not valid or unique, update the global count of data
    # entries for progress and logging purposes.
    else:
        number_of_data_lines.value -= 1


def read_unclean_data_file(unclean_data_file_name):
    """ Reads unclean data file and assigns unclean data lines to worker pool. """
    # Setup a worker pool for cleaning.
    pool = Pool(POOL_PROCESSOR_COUNT)
    # Attempt to open the unclean data file for reading.
    try:
        with open(unclean_data_file_name, FILE_READ_MODE) as unclean_data_file:
            # Fetch every data line in the file.
            for data_line in unclean_data_file:
                # Assign an unclean data line for cleaning to a worker process.
                pool.apply_async(clean_data_line, args=(data_line,))
    # If there was an error let the user know.
    except:
        util.log_print('Error reading file: "{0}"'.format(unclean_data_file_name))
        pool.terminate()
        return
    # Wait for worker pool to finish up.
    pool.close()
    pool.join()


def write_clean_data_file(clean_data_file_name):
    """ Write clean data to the specified data file. """
    global data_to_write_queue
    global number_of_data_lines
    # Create a progress bar to show progress of processing.
    progress_bar = util.ProgressBar(number_of_data_lines.value, 'Cleaning headers', 71)
    counter = 0
    with open(clean_data_file_name, FILE_WRITE_MODE) as data_file:
        while True:
            # Keep retrieving header data from write queue until timeout exception 
            # is raised (should mean that no more data will be added to the queue).
            try:
                clean_data = data_to_write_queue.get(block=True, timeout=QUEUE_TIMEOUT)
                data_file.write('{0}\n'.format(clean_data))
                counter += 1
                # Update progress bar.
                progress_bar.update(counter, total=number_of_data_lines.value)
            except Exception:
                # Finish up the writing process.
                progress_bar.clean()
                break
    # Return the number of entries that were written.
    return counter


def clean_data(unclean_data_file_name):
    """ Orchestrates reading and writing data processes. """
    global number_of_data_lines
    # Report original number of data lines.
    pre_log_entry = 'Found {0} entries in "{1}"'.format(
        number_of_data_lines.value,
        unclean_data_file_name
    )
    util.log_print(pre_log_entry)
    # Create a separate process to read unclean data file.
    read_process = Process(target=read_unclean_data_file, args=(unclean_data_file_name,))
    read_process.start()
    # Write clean data in current process.
    clean_data_file_name = util.create_new_data_file_name(
        unclean_data_file_name,
        CLEAN_FILE_NAME_ADDITION
    )
    entries_written = write_clean_data_file(clean_data_file_name)
    # Report number of clean data lines.
    post_log_entry = '{0} entries written in "{1}"'.format(
        entries_written,
        clean_data_file_name
    )
    util.log_print(post_log_entry)
    # Wait for reading process to finish up.
    read_process.join()


def main():
    """ Setup for data cleaning. """
    args = create_arg_parser().parse_args()
    check_is_valid_file(args.file)
    initialise_global_variables(args.file)
    start_time = time.time()
    clean_data(args.file)
    end_time = time.time()
    execution_time = (end_time - start_time - QUEUE_TIMEOUT) / 60
    util.log_print('{0:.4f} min'.format(execution_time))


if __name__ == '__main__':
    main()
