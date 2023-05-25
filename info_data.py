from pathlib import Path


class FileInfoData:
    title = ''

    def __init__(self, filename: Path):
        self.title = filename
        self.lines_in_files = {
            'name': 'Количество строк в файле',
            'value': 0
        }
        self.translated_lines = {
            'name': 'Переведенные строки',
            'value': []
        }
        self.lines_from_vanilla_loc = {
            'name': 'Строки из ваниллы',
            'value': []
        }
        self.lines_from_previous_version = {
            'name': 'Строки из предыдущей версии',
            'value': []
        }
        self.lines_with_errors = {
            'name': 'Строки с ошибками',
            'value': []
        }
        self.process_time = {
            'name': 'Время выполнения',
            'value': 0
        }

    def set_lines_in_files(self, amount):
        self.lines_in_files['value'] = amount

    def add_translated_line(self, line_number):
        self.translated_lines['value'].append(line_number + 1)

    def add_line_from_vanilla_loc(self, line_number):
        self.lines_from_vanilla_loc['value'].append(line_number + 1)

    def add_line_from_previous_version(self, line_number):
        self.lines_from_previous_version['value'].append(line_number + 1)

    def add_line_with_error(self, line_number):
        self.lines_with_errors['value'].append(line_number + 1)

    def set_process_time(self, time_delta):
        self.process_time['value'] = time_delta

    def get_file_data(self):
        return {'title': self.title, 'expanded_data': (self.lines_in_files, self.translated_lines, self.lines_from_vanilla_loc,
                self.lines_from_previous_version, self.lines_with_errors, self.process_time)}


class InfoData:
    title = "General"

    def __init__(self):

        self.translated_files = {
            'name': 'Переведено файлов',
            'value': 0
        }

        self.translated_chars = {
            'name': 'Переведено символов',
            'value': 0
        }

        self.used_api = {
            'name': 'Использованные апи',
            'value': None
        }

        self.files_info = {}

    def add_file_info(self, file_info: FileInfoData):
        self.files_info[file_info.title] = file_info

    def add_translated_files(self):
        self.translated_files['value'] += 1

    def add_translated_chars(self, chars):
        self.translated_chars['value'] += chars

    def get_data_for_general(self):
        return {'title': self.title, 'expanded_data': (self.translated_files, self.translated_chars, self.used_api)}
