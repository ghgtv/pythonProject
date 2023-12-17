import os
from datetime import datetime

import requests
import ClientConfigurator
import json

config = ClientConfigurator.get_configure()


def ask_version():
    url = f"{config['server_url']}/get_server_version"

    data = {"username": config["username"], "password": config["password"]}

    return requests.post(url, data=data).text


def ask_files():
    filesdict = {}
    for address, dirs, files in os.walk(config["working_directory"]):
        for name in files:
            filesdict[os.path.join(name)] = str(datetime.fromtimestamp(
                os.path.getmtime(os.path.join(address, name))).date())
    url = f"{config['server_url']}/get_server_files"

    data = {
        "username": config["username"],
        "password": config["password"],
        "files_time": str(filesdict).replace("'", '"')
    }

    temp = requests.post(url, data=data).text
    return json.loads(temp)

