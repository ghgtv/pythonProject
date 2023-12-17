import os.path
import sys
import subprocess
import Requester
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from client_ui import Ui_MainWindow
import ClientConfigurator
import FileManager
from settings_ui import Ui_Settings_form
import tkinter
from tkinter import filedialog


class SettingsWidget(QWidget, Ui_Settings_form):
    def __init__(self):
        super().__init__()
        self.config = ClientConfigurator.get_configure()
        self.setupUi(self)
        self.server_url.setText(self.config["server_url"])
        self.login.setText(self.config["username"])
        self.password.setText(self.config["password"])
        self.working_directory.setText(self.config["working_directory"])
        self.apply_button.clicked.connect(self.apply)
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        self.open_folder_dialog_button.clicked.connect(self.open_folder_dialog)

    def apply(self):
        ClientConfigurator.update_config("server_url", self.server_url.toPlainText())
        ClientConfigurator.update_config("username", self.login.toPlainText())
        ClientConfigurator.update_config("password", self.password.toPlainText())
        ClientConfigurator.update_config("working_directory", self.working_directory.toPlainText())

    def save(self):
        self.apply()
        self.close()

    def open_folder_dialog(self):
        root = tkinter.Tk()
        root.withdraw()
        directory_path = filedialog.askdirectory()
        self.working_directory.setText(directory_path)


# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        self.ex = None
        self.launch_button.clicked.connect(self.launch)
        self.config = ClientConfigurator.get_configure()
        self.open_directory_button.clicked.connect(self.open_directory)
        self.settings_button.clicked.connect(self.open_settings)
        self.repair_button.clicked.connect(self.repair)

    def launch(self):
        version = Requester.ask_version()
        if version == self.config["version"]:
            subprocess.run([f'{self.config["working_directory"]}/{self.config["exe_file_path"]}'])

        else:
            FileManager.unpack_files(Requester.ask_files())
            ClientConfigurator.update_config("version", version)
            subprocess.run([f'{self.config["working_directory"]}/{self.config["exe_file_path"]}'])

    def open_directory(self):
        path = self.config["working_directory"]
        subprocess.Popen(f'explorer /select,"{os.path.normpath(path)}"')

    def open_settings(self):
        if self.ex is None:
            self.ex = SettingsWidget()
        self.ex.show()

    def repair(self):
        ClientConfigurator.update_config("version", "REPAIR")
        self.launch()


def exept_hook(cls, exeption, traceback):
    sys.__excepthook__(cls, exeption, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = exept_hook
    sys.exit(app.exec_())
