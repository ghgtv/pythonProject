import os
from datetime import datetime
from tkinter import messagebox
import requests
import ClientConfigurator
import json

config = ClientConfigurator.get_configure()


def ask_version():
    url = f"{config['server_url']}/get_server_version"

    data = {"username": config["username"], "password": config["password"]}
    answer = requests.post(url, data=data)
    if answer.status_code != 200:
        if answer.status_code == 403:
            messagebox.showerror(title="Login error", message="Invalid login or password, please check your credentials")
        elif answer.status_code == 405:
            messagebox.showerror(title="Connection error", message="Can`t connect to the server, your url is wrong or server offline")
        elif answer.status_code == 500:
            messagebox.showerror(title="Server error", message="The server you are trying to connect has returned internal error")
        else:
            messagebox.showerror(title="Unknown error", message=f"Unknown error happened, there is responce status: {answer.raw}")
        return None
    else:
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

