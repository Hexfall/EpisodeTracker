import json
import os
import subprocess
from pathlib import Path


data_path = os.path.join(os.path.dirname(__file__), 'data')
paths_path = data_path + '/paths.json'
index_path = data_path + '/index.json'
extensions = [
    "mkv",
    "mp4",
    "avi",
]


def create_data_folder() -> None:
    if not os.path.exists(data_path):
        os.makedirs(data_path)


class ShowManager:
    def __init__(self) -> None:
        self.__paths = {}
        self.__indexes = {}
        self.__load_data()

    def get_shows(self):
        return list(self.__paths.keys())

    def __load_data(self) -> None:
        create_data_folder()

        if os.path.exists(paths_path):
            with open(paths_path, 'r', encoding='utf-8') as f:
                self.__paths = json.load(f)

        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                self.__indexes = json.load(f)

    def __save_data(self) -> None:
        create_data_folder()
        with open(paths_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__paths, indent=4))
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__indexes, indent=4))

    def set_index(self, show: str, index: int) -> None:
        self.__indexes[show] = index

    def inc_index(self, show: str, index: int) -> None:
        self.set_index(show, self.__indexes[show]+index)

    def reset_index(self, show: str) -> None:
        self.set_index(show, 0)

    def remove_show(self, show: str) -> None:
        self.__paths.pop(show, None)
        self.__indexes.pop(show, None)

    def add_show(self, show: str, path: str) -> None:
        if not Path(path).is_dir():
            raise FileNotFoundError('Path is not a directory.')
        self.__paths[show] = path
        self.__indexes[show] = 0

    def play(self, show: str) -> None:
        if show not in self.get_shows():
            raise ValueError(f"Show {show} not in  library.")
        files = self.__get_files(show)
        self.set_index(show, self.__indexes[show] % len(files))
        os.system(f"vlc -V x11 '{files[self.__indexes[show]]}' >/dev/null 2>&1 &")
        self.inc_index(show, 1)

    def get_progress(self, show: str) -> str:
        return f"{self.__indexes[show]:.>{len(str(max(self.__indexes.values())))}}/{len(self.__get_files(show))}"

    def __get_files(self, show: str) -> list:
        if show not in self.__paths.keys():
            raise Exception(f'Could not get files for show "{show}". Show not found in path list.')
        if not os.path.exists(self.__paths[show]):
            raise FileNotFoundError(f'Path for show "{show}" does not exist.')
        ret = []
        for ext in extensions:
            ret += list(Path(self.__paths[show]).rglob('*.' + ext))
        return sorted(ret)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__save_data()

    def __enter__(self):
        return self
