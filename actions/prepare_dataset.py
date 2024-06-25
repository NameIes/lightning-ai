import os
from flask import Flask, send_from_directory
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
    base_dir = Storage()['base_dir'] / 'datasets' / 'collected'

    @app.route('/')
    def index():
        lst = []

        for i in base_dir.iterdir():
            if i.is_dir():
                lst.append(i)

        return '\n'.join(['<a href="/dataset/{}/">{}</a>'.format(i.name, str(i)) for i in lst])

    @app.route('/img/<dataset>/<img>/')
    def get_images(dataset: str, img: str):
        return send_from_directory(base_dir / dataset, img)

    @app.route('/dataset/<dataset>/')
    def get_datasets(dataset: str):
        if not (base_dir / dataset).exists():
            raise FileNotFoundError

        lst = []
        for i in (base_dir / dataset).iterdir():
            if i.suffix == '.jpg':
                lst.append(i)

        page = '<div style="display: flex; flex-wrap: wrap; gap: 5px">{}</div>'.format(
            '\n'.join([
                '<a href="/dataset/{}/{}/"><img src="/img/{}/{}/" style="width: 128px; height: 128px;" /></a>'.format(
                    dataset, i.name, dataset, i.name
                ) for i in lst
            ])
        )
        return page

    @app.route('/dataset/<dataset>/<img>/')
    def get_image(dataset: str, img: str):
        # Get YOLO rects
        # Add YOLO rects to script tag variable
        # With vue js create app for:
        # 1. Create rects
        # 2. Delete rects
        # 3. Move rects
        # 4. Resize rects
        # 5. Send rects to server
        # 6. Moving between images
        # Rules:
        # 1. Don't send to server empty rects
        return 'NEED VUE JS'

    @app.route('/dataset/<dataset>/<img>/save/', methods=['POST'])
    def save_image(dataset: str, img: str):
        # Copy image to prepared dataset
        # In prepared dataset create _annotations.coco.json
        # Add YOLO rects to _annotations.coco.json
        return 'BE HAPPY'

    os.system('start http://localhost:5000')
    app.run(host='localhost', debug=False)


if __name__ == '__main__':
    prepare_dataset()
