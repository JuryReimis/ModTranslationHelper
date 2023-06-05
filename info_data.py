from pathlib import Path

from languages.language_constants import StatWindowConstants


class FileInfoData:
    title = ''

    def __init__(self, filename: Path):
        self.title = filename
        self.used_api = {
            'name': StatWindowConstants.used_service_apis,
            'value': set()
        }
        self.lines_in_files = {
            'name': StatWindowConstants.lines_in_file_len,
            'value': 0
        }
        self.new_lines = {
            'name': StatWindowConstants.new_lines,
            'value': []
        }
        self.translated_lines = {
            'name': StatWindowConstants.translated_lines,
            'value': []
        }
        self.lines_from_vanilla_loc = {
            'name': StatWindowConstants.lines_from_vanilla,
            'value': []
        }
        self.lines_from_previous_version = {
            'name': StatWindowConstants.lines_from_previous_version,
            'value': []
        }
        self.lines_with_errors = {
            'name': StatWindowConstants.lines_with_errors,
            'value': []
        }
        self.process_time = {
            'name': StatWindowConstants.time_of_process,
            'value': 0
        }

    def add_api_service(self, api_name: str):
        self.used_api['value'].add(api_name)

    def set_lines_in_files(self, amount):
        self.lines_in_files['value'] = amount

    def add_new_line(self, line_number):
        self.new_lines['value'].append(line_number + 1)

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
        return {'title': self.title,
                'expanded_data': (self.used_api, self.lines_in_files, self.new_lines, self.translated_lines,
                                  self.lines_from_vanilla_loc, self.lines_from_previous_version,
                                  self.lines_with_errors, self.process_time)}

    def get_file_data_for_csv(self):
        rows = [{'name': self.title}, self.used_api, self.lines_in_files, self.new_lines, self.translated_lines,
                self.lines_from_vanilla_loc, self.lines_from_previous_version, self.lines_with_errors,
                self.process_time, {'name': ''}]
        return rows


class InfoData:

    def __init__(self, mod_name="Mod name"):
        self.title = mod_name
        self.translated_files = {
            'name': StatWindowConstants.translated_files,
            'value': 0
        }

        self.translated_chars = {
            'name': StatWindowConstants.translated_chars,
            'value': 0
        }

        self.used_api = {
            'name': StatWindowConstants.used_service_apis,
            'value': set()
        }

        self.files_info = {}

    def add_file_info(self, file_info: FileInfoData):
        self.files_info[file_info.title] = file_info

    def add_translated_files(self):
        self.translated_files['value'] += 1

    def add_translated_chars(self, chars):
        self.translated_chars['value'] += chars

    def add_api_service(self, api_name: str):
        self.used_api['value'].add(api_name)

    def get_data_for_general(self):
        return {'title': self.title, 'expanded_data': (self.translated_files, self.translated_chars, self.used_api)}

    def get_data_for_csv(self):
        rows = [{'name': self.title}, self.translated_files, self.translated_chars, self.used_api, {'name': ''}]
        for file in self.files_info.values():
            rows += file.get_file_data_for_csv()
        return rows
