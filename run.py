#!/usr/bin/env python3

import argparse
import os
import progressbar
import requests
import stat
import sys
import tarfile
from enum import IntEnum
from subprocess import run

DATASET_DOWNLOAD_URL = 'https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz'
DEFAULT_RESOURCE_DIR = 'res'
DEFAULT_DATASET_DIR = 'maildir'
DEFAULT_HEADER_FILE = 'headers.dat'
DEFAULT_CLEAN_HEADER_FILE = 'headers_clean.dat'
DEFAULT_ANONYMISED_FILE = 'headers_clean_anon.dat'
BASE_SRC_DIR = 'src'
BASE_PYTHON_DIR = 'python'
ACQUISITION_PACKAGE = 'acquisition'
ACQUISITION_SCRIPT = 'acquisition.py'
CLEANING_PACKAGE = 'cleaning'
CLEANING_SCRIPT = 'cleaning.py'
ANONYMISATION_PACKAGE = 'anonymization'
ANONYMISATION_SCRIPT = 'anonymization.py'
ANALYSIS_PACKAGE = 'exploratory_analysis'
ANALYSIS_SCRIPT = 'analysis.py'
LEARNING_PACKAGE = 'machine_learning'
TARGET_SCRIPTS = []
TARGET_RULES = []

class Rule(IntEnum):
    DOWNLOAD = 0
    ACQUISITION = 1
    CLEANING = 2
    ANONYMISATION = 3
    ANALYSIS = 4
    LEARNING = 5


def create_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--all',
        action='store_true',
        default=True,
        help='Run all target rules'
    )
    arg_parser.add_argument(
        '--download',
        action='store_true',
        default=False,
        help='Download raw email dataset'
    )
    arg_parser.add_argument(
        '--acquisition',
        action='store_true',
        default=False,
        help='Run acquisition rule'
    )
    arg_parser.add_argument(
        '--cleaning',
        action='store_true',
        default=False,
        help='Run cleaning rule'
    )
    arg_parser.add_argument(
        '--anonymisation',
        action='store_true',
        default=False,
        help='Run anonymisation rule'
    )
    arg_parser.add_argument(
        '--analysis',
        action='store_true',
        default=False,
        help='Run explaratory analysis rule'
    )
    arg_parser.add_argument(
        '--learning',
        action='store_true',
        default=False,
        help='Run machine learning rule'
    )
    arg_parser.add_argument(
        '-p',
        '--path',
        default=os.path.join(
            DEFAULT_RESOURCE_DIR,
            DEFAULT_DATASET_DIR
        ),
        help='Path to resource folder for data files'
    )
    arg_parser.add_argument(
        '-f',
        '--file',
        default=os.path.join(
            DEFAULT_RESOURCE_DIR,
            DEFAULT_HEADER_FILE
        ),
        help='Name of output data file for specified phase'
    )
    arg_parser.add_argument(
        '-i',
        '--isolated',
        action='store_true',
        default=False,
        help='Run only the target rule'
    )
    return arg_parser


def initialise_global_variables():
    global TARGET_RULES
    global TARGET_SCRIPTS
    TARGET_RULES = [
        download_rule,
        acquisition_rule,
        cleaning_rule,
        anonymisation_rule,
        analysis_rule,
        learning_rule
    ]
    base_path = os.path.join(
        BASE_SRC_DIR,
        BASE_PYTHON_DIR
    )
    target_script_paths = [
        os.path.join(ACQUISITION_PACKAGE, ACQUISITION_SCRIPT),
        os.path.join(CLEANING_PACKAGE, CLEANING_SCRIPT),
        os.path.join(ANONYMISATION_PACKAGE, ANONYMISATION_SCRIPT),
        os.path.join(ANALYSIS_PACKAGE, ANALYSIS_SCRIPT)
    ]
    TARGET_SCRIPTS = [ 
        os.path.join(base_path, script) for script in target_script_paths
    ]


def is_executable(file_path):
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)


def check_executable_rules():
    global TARGET_SCRIPTS
    for script in TARGET_SCRIPTS:
        if not is_executable(script):
            script_stat = os.stat(script)
            os.chmod(script, script_stat.st_mode | stat.S_IEXEC)


def print_rule_title(title):
    print('')
    print('{0:^110}'.format('--- {0} ---'.format(title)))


def append_to_file_name(file_name, appendage):
    dir_name = os.path.dirname(file_name)
    file_base_name = os.path.basename(file_name)
    return os.path.join(
        dir_name,
        '{0}.{1}'.format(
            file_base_name.split('.')[0] + appendage,
            file_base_name.split('.')[-1]
        )
    )


def download_rule(**kwargs):
    dataset_path = kwargs.get(
        'dataset_path',
        os.path.join(
            DEFAULT_RESOURCE_DIR,
            DEFAULT_DATASET_DIR
        )
    )
    res_path = os.path.dirname(dataset_path)
    download_file = os.path.join(
        res_path,
        DATASET_DOWNLOAD_URL.split('/')[-1]
    )
    # Check if dataset path given exists if it does not assume
    # the dataset has not been downloaded.
    if not os.path.exists(download_file) and not os.path.exists(dataset_path):
        print_rule_title('Downloading')
        # Download the dataset file
        request = requests.get(DATASET_DOWNLOAD_URL, stream=True)
        total_length = int(request.headers.get('content-length'))
        ch_size = 256 * 2 ** 20
        # Move the downloaded bytes to a local file
        with open(download_file, 'wb') as file:
            bar = progressbar.ProgressBar(maxval=(total_length / ch_size) + 1)
            bar.start()
            for chunk in request.iter_content(chunk_size=ch_size): 
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
            bar.finish()
    # Check to see if extraction of download file is necessary.
    if os.path.isfile(download_file) and not os.path.exists(dataset_path):
        # The downloaded file is a tarball so extract it
        with tarfile.open(download_file) as tar:
            tar.extractall(path=res_path)


def acquisition_rule(**kwargs):
    print_rule_title('Acquisition')
    dataset_path = kwargs.get('dataset_path', DEFAULT_RESOURCE_DIR)
    data_file = kwargs.get('file', os.path.join(
        DEFAULT_RESOURCE_DIR,
        DEFAULT_HEADER_FILE
    ))
    # Run the acquisition script
    run(
        '{0} {1} {2}'.format(
            os.path.join(
                BASE_SRC_DIR,
                BASE_PYTHON_DIR,
                ACQUISITION_PACKAGE,
                ACQUISITION_SCRIPT
            ),
            '{0} {1}'.format('--path', dataset_path),
            '{0} {1}'.format('--file', data_file)
        ),
        shell=True
    )


def cleaning_rule(**kwargs):
    print_rule_title('Cleaning')
    data_file = kwargs.get('file', os.path.join(
        DEFAULT_RESOURCE_DIR,
        DEFAULT_HEADER_FILE
    ))
    # Run the cleaning script
    run(
        '{0} {1}'.format(
            os.path.join(
                BASE_SRC_DIR,
                BASE_PYTHON_DIR,
                CLEANING_PACKAGE,
                CLEANING_SCRIPT
            ),
            '{0} {1}'.format('--file', data_file)
        ),
        shell=True
    )


def anonymisation_rule(**kwargs):
    print_rule_title('Anonymisation')
    data_file = kwargs.get('file', os.path.join(
        DEFAULT_RESOURCE_DIR,
        DEFAULT_HEADER_FILE
    ))
    data_file = append_to_file_name(data_file, '_clean')
    # Run the anonymisation script
    run(
        '{0} {1}'.format(
            os.path.join(
                BASE_SRC_DIR,
                BASE_PYTHON_DIR,
                ANONYMISATION_PACKAGE,
                ANONYMISATION_SCRIPT
            ),
            '{0} {1}'.format('--file', data_file)
        ),
        shell=True
    )


def analysis_rule(**kwargs):
    print_rule_title('Analysis')
    data_file = kwargs.get('file', os.path.join(
        DEFAULT_RESOURCE_DIR,
        DEFAULT_HEADER_FILE
    ))
    data_file = append_to_file_name(data_file, '_clean')
    # Run the analysis script
    run(
        '{0} {1}'.format(
            os.path.join(
                BASE_SRC_DIR,
                BASE_PYTHON_DIR,
                ANALYSIS_PACKAGE,
                ANALYSIS_SCRIPT
            ),
            '{0} {1}'.format('--file', data_file)
        ),
        shell=True
    )


def learning_rule(**kwargs):
    print_rule_title('Learning')


def filter_rules(rule, isolated):
    if isolated:
        return [ TARGET_RULES[rule] ]
    return TARGET_RULES[:][:rule + 1]


def get_rules(args):
    if args.download:
        return filter_rules(Rule.DOWNLOAD, args.isolated)
    elif args.acquisition:
        return filter_rules(Rule.ACQUISITION, args.isolated)
    elif args.cleaning:
        return filter_rules(Rule.CLEANING, args.isolated)
    elif args.anonymisation:
        return filter_rules(Rule.ANONYMISATION, args.isolated)
    elif args.analysis:
        return filter_rules(Rule.ANALYSIS, args.isolated)
    elif args.learning:
        return filter_rules(Rule.LEARNING, args.isolated)
    elif args.all:
        return TARGET_RULES[:]
    else:
        print('Error: No target rule specified.')
        sys.exit()


def run_rules(rules, args):
    check_executable_rules()
    for rule in rules:
        rule(
            dataset_path=args.path,
            file=args.file
        )


def main():
    args = create_arg_parser().parse_args()
    initialise_global_variables()
    rules = get_rules(args)
    run_rules(rules, args)
    print('')


if __name__ == '__main__':
    main()
