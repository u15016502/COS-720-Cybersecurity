"""Header anonymization functions

Script containing functions used for anonymizing the email headers

"""


def anonymize_date(date):
    """ Generalize time of the Date header value """
    values = date[0].split(" ")
    # Looking for time in header values (at index 4)
    time = values[4]
    # Generalize the value by stripping seconds and making it a ranged value
    time = time.split(":")
    time = "[{0}:00 - {0}:59]".format(time[0])
    # Put the generalized time value back in its position
    values[4] = time
    # Join everythin up again
    return [" ".join(values)]


def anonymize(headers):
    """ Removes the explicit identifiers from the headers """
    for header in headers:
        del header["Message-ID"]
        del header["X-From"]
        del header["X-To"]
        del header["X-Origin"]
        del header["X-cc"]
        del header["X-bcc"]
        del header["X-Folder"]
        # Generalize From address
        is_valid_email = len(header["From"][0].split("@")) == 2
        if is_valid_email:
            header["From"] = [header["From"][0].split("@")[1].split(".")[0]]
        # Generalize To Addresses
        # Note: The final condition causes addresses without @ signs to be ignored
        is_valid_email = len(header['To']) > 0 and header["To"][0] != "{mail_list}"
        for index in range(len(header["To"])):
            checks = header["To"][index] != ''
            checks = checks and header["To"][index] != "{mail_list}"
            checks = checks and len(header["To"][index].split("@")) >= 2
            if checks:
                header["To"][index] = header["To"][index].split("@")[1].split(".")[0]
        # Generalize Cc Addresses
        for index in range(len(header["Cc"])):
            if len(header["Cc"][index].split("@")) >= 2:
                header["Cc"][index] = header["Cc"][index].split("@")[1].split(".")[0]
        # Generalize Bcc Addresses
        for index in range(len(header["Bcc"])):
            if len(header["Bcc"][index].split("@")) >= 2:
                header["Bcc"][index] = header["Bcc"][index].split("@")[1].split(".")[0]
        # Suppress X-Filename to only show the file extension
        if len(header["X-FileName"]) > 0 and header["X-FileName"][0] != '':
            header["X-FileName"] = ["." + header["X-FileName"][0].split(".")[1]]
        # Generalize Date header value.
        header["Date"] = anonymize_date(header["Date"])
    return headers
