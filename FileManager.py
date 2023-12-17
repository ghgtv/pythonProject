import ClientConfigurator
import os

config = ClientConfigurator.get_configure()


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'wb')


def unpack_files(incoming_files: dict):
    for file in incoming_files["UPDATE"]:
        f = safe_open_w(f"{config['working_directory']}/{file[0]}")
        f.write(bytes(file[1], "utf-8"))
        f.close()
