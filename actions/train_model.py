import cutie
from pathlib import Path
from colorama import Fore, Style
from ultralytics import YOLO
from core.storage import Storage


def print_selection() -> Path:
    print('{}Please select dataset for training:{}'.format(
        Fore.GREEN,
        Style.RESET_ALL
    ))
    prepared_datasets = Path(Storage().data['base_dir']) / 'datasets' / 'prepared'
    prepared_datasets = [i for i in prepared_datasets.iterdir() if i.is_dir() and i.name.isdigit()]

    return prepared_datasets[cutie.select(prepared_datasets)]


def train_model() -> None:
    selected_dataset = print_selection()
    model = YOLO(Path(Storage().data['base_dir']) / 'models' / 'pretraining.pt')

    model.train(
        data=str(selected_dataset / 'data.yaml'),
        epochs=100,
        batch=8,
        imgsz=(640, 369),
        device='cuda'
    )

    print(Fore.GREEN + 'Model trained successfully.' + Style.RESET_ALL)
    print(Fore.GREEN + 'Press any key and Enter to exit.' + Style.RESET_ALL)
    input()
