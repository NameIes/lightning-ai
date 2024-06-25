import cutie
import msvcrt
from pathlib import Path
from colorama import Fore, Style
from ultralytics import YOLO
from core.storage import Storage


def print_selection() -> Path:
    prepared_datasets = Path(Storage()['base_dir']) / 'datasets' / 'prepared'
    prepared_datasets = [i for i in prepared_datasets.iterdir() if i.is_dir()]

    if not prepared_datasets:
        print(Fore.RED + 'No prepared datasets found.' + Style.RESET_ALL)
        return None

    print('{}Please select dataset for training:{}'.format(
        Fore.GREEN,
        Style.RESET_ALL
    ))

    return prepared_datasets[cutie.select(prepared_datasets)]


def train_model() -> None:
    selected_dataset = print_selection()
    if selected_dataset is None:
        print(Fore.GREEN + 'Press any key to continue...' + Style.RESET_ALL)
        msvcrt.getch()
        return

    model = YOLO(Path(Storage()['base_dir']) / 'models' / 'pretraining.pt')

    model.train(
        data=str(selected_dataset / 'data.yaml'),
        epochs=100,
        batch=8,
        imgsz=(640, 640),
        device='cuda',
        name='trained',
    )

    print(Fore.GREEN + 'Model trained successfully.' + Style.RESET_ALL)
    print(Fore.GREEN + 'Press any key and Enter to exit.' + Style.RESET_ALL)
    input()
