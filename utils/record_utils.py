from constants import RECORD_FILE


def save_record(record):

    record_anterior = get_record()

    if record > record_anterior:
        with open(RECORD_FILE, "w") as file:
            file.write(str(record))

def get_record():
    try:
        with open(RECORD_FILE, 'r') as file:
            contenido = file.read()
            if contenido:
                return int(contenido)
            else:
                return 0  #
    except (FileNotFoundError, ValueError):
        return 0
