import uuid
import os
from datetime import datetime


class Writer:

    def __init__(self, city_name: str):
        self._city_name = city_name
        self._dir_path = self.__init_dir_path()

    def __init_dir_path(self) -> str:
        formatted_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        suffix = str(uuid.uuid4())
        path = '-'.join([formatted_time, self._city_name, suffix])

        os.mkdir(path)
        return path

    def create_new_file_path(self) -> str:
        return self._dir_path + '/' + '-'.join([self._city_name, str(uuid.uuid4())])

    def write(self, response_list: list[dict], file_path):
        with open(file_path, 'a', encoding='utf-8') as file:
            for response_dict in response_list:
                name = response_dict['name']
                vicinity = response_dict['vicinity']
                rating = 0 if 'rating' not in response_dict else response_dict['rating']

                data = '/'.join(map(str, [name, vicinity, rating]))
                self.__write_each_line(data, file)

    def __write_each_line(self, data, file):
        file.write(data)
        file.write('\n')
