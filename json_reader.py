import os
import json
from collections import namedtuple


JSONData = namedtuple('JSONData', 'file_name data')


class JSONReader():
    def __init__(self):
        pass

    def is_json_file(self, file_name):
        return file_name.endswith('json')

    def load_data_from_file(self, path_to_file):
        with open(path_to_file, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return None

    def find_json_files_in_folder(self, path_to_folder):
        json_files = []
        with os.scandir(path_to_folder) as entries:
            for entry in entries:
                if self.is_json_file(entry.name):
                    json_files.append(entry)
        return json_files

    def json_data_from_folder(self, path_to_folder):
        json_files = self.find_json_files_in_folder(path_to_folder)
        for json_file in json_files:
            yield JSONData(json_file.name, self.load_data_from_file(json_file.path))
