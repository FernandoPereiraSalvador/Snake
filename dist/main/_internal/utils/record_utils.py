from constants import RECORD_FILE


def save_record(record):
    """
    Save the score record in a txt file.

    This function compares the current score with the record stored in the file. If the current score is higher than
    the stored record, it updates the record in the file with the new score.

    :param record: The current game score that is compared to the record.
    :return: None
    """

    # We obtain the previous record
    record_anterior = get_record()

    # We check if we have achieved a new record
    if record > record_anterior:
        with open(RECORD_FILE, "w") as file:
            file.write(str(record))

def get_record():
    """
    Gets the record score stored in a txt file.

    Attempts to open the file that stores the score record and reads it. If the file exists and contains a valid number,
    the stored record is returned. If the file does not exist or does not contain a valid number, 0 is returned as the default value.

    :return: The score record stored in the file or 0 if the record is not found or is invalid.
    """
    try:
        with open(RECORD_FILE, 'r') as file:
            contenido = file.read()
            if contenido:
                return int(contenido)
            else:
                return 0
    except (FileNotFoundError, ValueError):
        return 0
