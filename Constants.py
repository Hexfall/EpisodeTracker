import os


data_path = os.path.join(os.path.dirname(__file__), 'data')
lastshow_path = os.path.join(data_path, 'lastshow.txt')
paths_path = data_path + '/paths.json'
index_path = data_path + '/index.json'
extensions = [
    "mkv",
    "mp4",
    "avi",
]
