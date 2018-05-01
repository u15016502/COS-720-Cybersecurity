"""Header cleaning functions

Script containing functions used for cleaning header values.

Cleaning functions that are to be associated with headers
are also assigned within this script.

The script is intended to be used in conjunction with
cleaning.py script.

"""

import re

# List of tags inserted during cleaning when necessary.
CLEANING_TAGS = {
    'mail_list': '{mail_list}',
    'no_subject': '{no_subject}'
}

# Regex used for specific cleaning functions.
# Indexed using the function name.
CLEANING_FUNCTION_REGEX = {
    'clean_x_to_header': {
        'search': re.compile(r'</o(.*?)>'),
        'split': re.compile(r'(</o.*?>),?')
    },
    'clean_subject_header': {
        'search': re.compile(r'(re:|fw:|fwd:)', flags=re.IGNORECASE),
        'split': re.compile(r'(re:|fw:|fwd:)', flags=re.IGNORECASE)
    }
}


def clean_content_type_header(header, header_values, map_copy):
    """ Cleans Content-Type header values. """
    # The Content-Type header value usually resembles the following:
    #   text/plain; charset=us-ascii
    # This function splits the value into distinct values to possibly
    # aid the processes of exploration and learning.
    return ''.join(header_values).split('; ')


def clean_empty_header(header, header_values, map_copy):
    """ Cleans headers that are empty. """
    # Some values contain [''] as opposed to [], therefore to avoid
    # confusion and to standardise the dataset, enforce the use of []
    # over the use of [''].
    if header_values == ['']:
        return []
    return header_values


def clean_empty_to_header(header, header_values, map_copy):
    """ Cleans empty To headers. """
    if header_values == [''] or header_values == []:
        # An assumption is made that the map_copy contains already cleaned data.
        x_header = 'X-{0}'.format(header if header == 'To' else header.lower())
        x_header_values = map_copy[x_header]
        if x_header_values != []:
            # Insert a tag to indicate that the recipients most likely belong
            # to a mailing list specified in the X-To header.
            return [CLEANING_TAGS['mail_list']]
    # All is fine and well in header land.
    return header_values


def clean_non_multi_value_header(header, header_values, map_copy):
    """ Cleans headers that should not have multiple values. """
    # Some header values ought to be one single value as opposed
    # to multiple (which happens during header aquistion), such
    # as the Subject header. 
    if len(header_values) > 1:
        return [''.join(header_values)]
    return header_values


def clean_subject_header(header, header_values, map_copy):
    """ Cleans Subject header values. """
    if header_values != [''] and header_values != []:
        header_values_string = ''.join(header_values)
        compiled_regex = CLEANING_FUNCTION_REGEX['clean_subject_header']
        if compiled_regex['search'].search(header_values_string):
            new_header_values = compiled_regex['split'].split(header_values_string)
            if new_header_values is not None:
                # First elements should be 'RE:' or 'FW:'.
                # Clean the values so that 'RE:' and 'FW:' are consistent and not 're:'
                # for example.
                for i in range(0, len(new_header_values) - 1):
                    new_header_values[i] = new_header_values[i].strip()
                    if compiled_regex['search'].search(new_header_values[i]):
                        new_header_values[i] = new_header_values[i].upper()
                # Last element should be the subject body.
                new_header_values[-1] = new_header_values[-1].strip()
                # If there is no subject body, insert a tag.
                if new_header_values[-1] == '':
                    new_header_values[-1] = CLEANING_TAGS['no_subject']
                return [' '.join(new_header_values).strip()]
        # The subject is acceptible as is.
        return header_values
    # There is no subject, therefore, tag it.
    return [CLEANING_TAGS['no_subject']]


def clean_to_header(header, header_values, map_copy):
    """ Cleans To and similar header values. """
    # Since aquisition reads line-by-line, this function ensures that
    # the To header (as well as similar header values such as Cc) values
    # are distinctly separated values. 
    #   e.g: ['john@enron.com', 'jane@enron.com'] as opposed to 
    #       ['john@enron.com, jane@enron.com']
    new_header_values = ''.join(header_values).split(',')
    return [ to.strip() for to in new_header_values ]


def clean_x_to_header(header, header_values, map_copy):
    """ Cleans X-To header values. """
    compiled_regex = CLEANING_FUNCTION_REGEX['clean_x_to_header']
    header_values_string = ''.join(header_values)
    if compiled_regex['search'].search(header_values_string):
        new_header_values = []
        split_header_values = compiled_regex['split'].split(header_values_string)
        # These header values are formatted as 'Surname, Name' while the To
        # header values are formatted as 'Name Surname', therefore, for
        # consistency, enforce 'Name Surname' formatting.
        for i in range(0, len(split_header_values) - 2, 2):
            new_header_parts = [ part.strip() for part in split_header_values[i].split(', ')[::-1] ]
            new_header_value = ' '.join(new_header_parts)
            new_header_values.append(new_header_value.strip())
        return new_header_values
    # Uses format more akin to the To header.
    return clean_to_header(header, header_values, map_copy)


# Cleaning map that maps headers to corresponding cleaning functions.
# Defined here so that function symbols can be referenced.
HEADER_CLEANING_MAP = {
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'Message-ID': [],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'Date': [],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'From': [],
    # Requires cleaning.
    # Header value sometimes empty, which is valid.
    'Subject': [
        clean_non_multi_value_header,
        clean_subject_header
    ],
    # Requires cleaning.
    # Header value sometimes empty, which is valid.
    'Cc': [
        clean_to_header,
        clean_empty_header
    ],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'Mime-Version': [],
    'Content-Type': [
        clean_content_type_header
    ],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'Content-Transfer-Encoding': [],
    'Bcc': [
        clean_to_header,
        clean_empty_header
    ],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'X-From': [],
    # Requires cleaning.
    # Header value sometimes empty, which is valid.
    'X-To': [
        clean_x_to_header,
        clean_empty_header
    ],
    # Requires cleaning.
    # Header value sometimes empty, which is valid.
    'X-cc': [
        clean_x_to_header,
        clean_empty_header
    ],
    # Requires cleaning.
    # Header value almost always empty (only 170 entries with values).
    # Consider removing entirely.
    'X-bcc': [
        clean_x_to_header,
        clean_empty_header
    ],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'X-Folder': [],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'X-Origin': [],
    # Unlikely to need cleaning.
    # Header value should not be empty.
    'X-FileName': [],
    # Requires cleaning.
    # Header value sometimes empty, which is not valid and
    # should be addressed specifically.
    # Specified last due to order of processing requirements.
    'To': [
        clean_to_header,
        clean_empty_to_header
    ]
}
