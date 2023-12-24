import struct

import ClientConfigurator
import os


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'wb')


def convert_string_to_bytes(string):
    bts = b''
    for i in string:
        bts += struct.pack("B", ord(i))
    return bts


def unpack_files(incoming_files: dict):
    config = ClientConfigurator.get_configure()
    for file in incoming_files["UPDATE"]:
        f = safe_open_w(f"{config['working_directory']}/{file[0]}")
        contain = file[1][2:len(file[1]) - 1]
        print(contain)
        print(convert_string_to_bytes(contain))
        f.write(convert_string_to_bytes(contain))
        f.close()
    for file in incoming_files["DELETE"]:
        try:
            os.remove(f"{config['working_directory']}/{file}")
        except OSError:
            pass
    ClientConfigurator.update_config("exe_file_path", incoming_files["EXE"])
