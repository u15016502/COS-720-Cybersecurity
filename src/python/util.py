
import hashlib
import json
import math
import sys
import time
import threading

EMAIL_HEADERS = [
    'Message-ID',
    'Date',
    'From',
    'To',
    'Subject',
    'Cc',
    'Mime-Version',
    'Content-Type',
    'Content-Transfer-Encoding',
    'Bcc'
]
EMAIL_X_HEADERS = [
    'X-From',
    'X-To',
    'X-cc',
    'X-bcc',
    'X-Folder',
    'X-Origin',
    'X-FileName'
]

def log_print(string):
    """ Used to print to console in a consistent manner. """
    print('{0:=^100}'.format('    {0}    '.format(string)))

def create_header_map():
    """ Create and initialise a header map to fill from email file. """
    global email_headers
    return { header: [] for header in email_headers }

def stringify_headers(data_map):
    """ Stringifies given header data map. """
    return json.dumps(data_map, separators=(',', ':'))

def parse_headers(data_string):
    """ Parse stringified header data into header map. """
    return json.loads(data_string)

def determine_optimal_chunksize(num_elements, num_cores):
    """ Determines optimal chunksize of an iterable based on number of elements and cores. """
    return int(math.ceil(num_elements / float(num_cores)))

def hash_data(data_map):
    """ Produces and returns a hash string to check for data uniqueness. """
    data_string = '{0}{1}{2}'.format(
        data_map['Date'],
        data_map['From'],
        data_map['Subject']
    )
    return hashlib.md5(data_string.encode()).hexdigest()

def create_new_data_file_name(current_data_file_name, file_name_appendage):
    """ Generates a new file name for current data file based on appendage. """
    # Split the the file name into path sections (in case they are present).
    file_path = current_data_file_name.split('/')
    # Split the file name into name and extensions.
    file_name = file_path[-1].split('.')
    # Use the unclean data file name as the basis for the name of the new file.
    file_name[0] = '{0}{1}'.format(file_name[0], file_name_appendage)
    # Join everything again and return final name.
    file_path[-1] = '.'.join(file_name)
    return '/'.join(file_path)

def file_line_count(file_name):
    """ Get line count of specified file. """
    spinner = Spinner('Counting entries in "{0}"'.format(file_name))
    spinner.start()
    i = 0
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    spinner.stop()
    return i + 1

class Spinner(threading.Thread):
    """ Animated spinner to indicate processing is occurring. """
    
    def __init__(self, init_message):
        """ Initialise spinner. """
        sys.stdout.write('{0}   '.format(init_message))
        sys.stdout.flush()
        super().__init__(target=self._spin)
        self._stopevent = threading.Event()

    def _spin(self):
        """ Continuously animate spinner (intended to run on separate thread). """
        while not self._stopevent.isSet():
            for cursor in '|/-\\':
                if not self._stopevent.isSet():
                    sys.stdout.write('{0}{1} '.format(u'\u001b[2D', cursor))
                    sys.stdout.flush()
                    time.sleep(0.1)

    def stop(self):
        """ Set stop event of spinner thread and clean current line of terminal. """
        self._stopevent.set()
        time.sleep(0.1)
        sys.stdout.write(u'\u001b[1000D')
        sys.stdout.flush()

class ProgressBar():
    """ Animated progress bar to track progress of processing. """
    
    _ROUND_DECIMAL_PLACES = 1

    def __init__(self, total, status, bar_length):
        """ Initialise progress bar. """
        self._status = status
        self._total = total
        self._bar_length = bar_length

    def update(self, current_length, total=None):
        """ Update the progress of the animated progress bar. """
        total_length = self._total if total is None else total
        filled_length = int(round(self._bar_length * (current_length / float(total_length))))
        percent = round(100.0 * (current_length / float(total_length)), ProgressBar._ROUND_DECIMAL_PLACES)
        bar = '=' * filled_length + '-' * (self._bar_length - filled_length)
        sys.stdout.write('[{0}] {1}{2} ...{3}\r'.format(bar, percent, '%', self._status))
        sys.stdout.flush()

    def clean(self):
        """ Clean current line of terminal to remove progress bar. """
        sys.stdout.write(u'\u001b[1000D')
        sys.stdout.flush()
