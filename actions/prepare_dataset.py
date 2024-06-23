import os
from flask import Flask
from colorama import Fore, Style
from core.storage import Storage


def print_info() -> None:
    os.system('cls')
    print('{}The server for dataset preparation will be started now.\n Press {}Ctrl + C{} inside console to stop.{}'.format(
        Fore.GREEN,
        Fore.YELLOW + Style.BRIGHT,
        Style.RESET_ALL + Fore.GREEN,
        Style.RESET_ALL
    ))


def prepare_dataset() -> None:
    print_info()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Hello, World!'

    os.system('start http://localhost:5000')
    app.run(host='localhost', debug=False)
