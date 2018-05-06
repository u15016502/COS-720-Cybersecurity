"""Header anonymization functions

Script containing functions used for anonymizing the email headers

"""
import progressbar


def anonymize(headers):
    """ Removes the explicit identifiers from the headers """
    valid_headers = list(filter(lambda h: len(h["From"][0].split("@")) == 2 and h["To"][0] != "{mail_list}", headers))
    for header in valid_headers:
        del header["Message-ID"]
        del header["X-From"]
        del header["X-To"]
        del header["X-Origin"]
        del header["X-cc"]
        del header["X-bcc"]
        # Suppress X-Folder
        # Note: Might have to be deleted as the folder might be too revealing
        folder_parts = header["X-Folder"][0].split("\\")
        header["X-Folder"] = [folder_parts[len(folder_parts) - 1]]
        # Generalize From address
        header["From"] = [header["From"][0].split("@")[1].split(".")[0]]
        # Generalize To Addresses
        # Note: The final condition causes addresses without @ signs to be ignored
        for index in range(len(header["To"])):
            if header["To"][index] != '' and header["To"][index] != "{mail_list}" and len(header["To"][index].split("@")) >= 2:
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

    return headers
