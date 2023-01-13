import json
from pathlib import Path
import re
import time
from PyQt5.QtCore import QObject, pyqtSignal
from deep_translator import GoogleTranslator

from languages.language_constants import LanguageConstants


class Prepper:

    def __init__(self, game_path: Path = None, original_mode_path: Path = None,
                 target_path: Path = None, previous_path: Path = None):
        self._game_path = game_path
        self._original_mode_path = original_mode_path
        self._target_path = target_path
        self._previous_path = previous_path

        self._file_hierarchy = []
        self._previous_files = []
        self._original_files_size = 0

        self.validator = Validator()

        self._game_path_validate_result = False
        self._original_mode_path_validate_result = False
        self._previous_path_validate_result = False
        self._target_path_validate_result = False

    def set_game_path(self, game_path: str):
        r"""Должен формировать путь до папки с локализациями (game/localization, localisation и т.п.)"""
        self._game_path = Path(game_path)
        self._game_path_validate_result = self.validator.validate_game_path(self._game_path)

    def get_game_path(self) -> Path:
        return self._game_path

    def get_game_path_validate_result(self) -> bool:
        return self._game_path_validate_result

    def set_original_mode_path(self, original_mode_path: str, original_language: str):
        if original_mode_path == '':
            self._original_mode_path_validate_result = self.validator.validate_original_path(Path(original_mode_path),
                                                                                             original_language)
            self._original_mode_path = Path(original_mode_path)
        else:
            self._original_mode_path = Path(original_mode_path)
            self._original_mode_path_validate_result = self.validator.validate_original_path(self._original_mode_path,
                                                                                             original_language)
            if self.get_original_mode_path_validate_result():
                self._create_localization_hierarchy(original_language=original_language)

    def get_original_mode_path(self) -> Path:
        return self._original_mode_path

    def get_original_files_size(self) -> int:
        return self._original_files_size

    def get_original_mode_path_validate_result(self) -> bool:
        return self._original_mode_path_validate_result

    def set_previous_path(self, previous_path: str):
        self._previous_path = Path(previous_path)
        self._previous_path_validate_result = self.validator.validate_previous_path(self._previous_path)

    def get_previous_path(self) -> Path:
        return self._previous_path

    def get_previous_path_validate_result(self) -> bool:
        return self._previous_path_validate_result

    def set_target_path(self, target_path: str):
        self._target_path = Path(target_path)
        self._target_path_validate_result = self.validator.validate_target_path(self._target_path)

    def get_target_path(self) -> Path:
        return self._target_path

    def get_target_path_validate_result(self) -> bool:
        return self._target_path_validate_result

    def _create_localization_hierarchy(self, original_language=None):
        r"""Создает иерархию файлов из директории _original_mode_path, а также считает размер всех файлов в сумме"""
        self._original_files_size = 0
        self._file_hierarchy = []
        for step in self._original_mode_path.rglob(f'*l_{original_language}*'):
            if step.is_file() and step.suffix in ['.yml', '.txt', ]:
                self._file_hierarchy.append(step.relative_to(self._original_mode_path))
                self._original_files_size += step.stat().st_size

    def get_file_hierarchy(self) -> list:
        r"""Возвращается путь ко всем файлам, относительно пути, расположения локализации основного мода.
                Названия файлов не изменены под новый(target_language) язык"""
        return self._file_hierarchy

    def get_previous_files(self):
        for step in self._previous_path.rglob('*'):
            if step.is_file():
                self._previous_files.append(step)
        return self._previous_files


class Validator:

    def __init__(self):
        pass

    @staticmethod
    def __path_existence(path: Path) -> bool:
        return path.exists()

    @staticmethod
    def __drive_existence(path: Path) -> bool:
        drive_existence = Path(path.drive).exists() and bool(re.findall('.+:.+', str(path)))
        return drive_existence

    def validate_game_path(self, path: Path):
        path_existence = self.__path_existence(path) and self.__drive_existence(path)
        return path_existence

    def validate_original_path(self, path: Path, original_language: str):
        path_existence = self.__path_existence(path / original_language) and self.__drive_existence(path)
        return path_existence

    def validate_previous_path(self, path: Path):
        path_existence = self.__path_existence(path) and self.__drive_existence(path)
        return path_existence

    def validate_target_path(self, path: Path):
        path_existence = self.__drive_existence(path)
        return path_existence


class Settings:
    __settings = {
        'last_game_directory': "",
        'last_original_mode_directory': "",
        'last_previous_directory': "",
        'last_target_directory': "",
        'last_original_language': "english",
        'last_target_language': "russian",

        'app_language': "Русский"
    }

    def __init__(self, local_data_path: Path | None):
        self.__local_data_path = local_data_path
        if self.__local_data_path is not None:
            if self.__local_data_path.exists() and (self.__local_data_path / 'settings.json').exists():
                with (self.__local_data_path / 'settings.json').open(mode='r', encoding='utf-8-sig') as settings:
                    self.__settings = self.__settings | json.load(settings)
            else:
                Path.mkdir(self.__local_data_path, exist_ok=True)
                self.save_settings_data()

    def set_last_game_directory(self, value: Path):
        self.__settings['last_game_directory'] = str(value)

    def get_last_game_directory(self) -> str:
        return self.__settings.get('last_game_directory', '')

    def set_last_original_mode_directory(self, value: Path):
        self.__settings['last_original_mode_directory'] = str(value)

    def get_last_original_mode_directory(self) -> str:
        return self.__settings.get('last_original_mode_directory', '')

    def set_last_previous_directory(self, value: Path):
        self.__settings['last_previous_directory'] = str(value)

    def get_last_previous_directory(self) -> str:
        return self.__settings.get('last_previous_directory', '')

    def set_last_target_directory(self, value: Path):
        self.__settings['last_target_directory'] = str(value)

    def get_last_target_directory(self) -> str:
        return self.__settings.get('last_target_directory', '')

    def set_last_languages(self, original, target):
        self.__settings['last_original_language'] = original
        self.__settings['last_target_language'] = target

    def set_app_language(self, value):
        self.__settings['app_language'] = value

    def get_last_original_language(self):
        return self.__settings.get('last_original_language', 'english')

    def get_last_target_language(self):
        return self.__settings.get('last_target_language', 'russian')

    def get_app_language(self):
        return self.__settings.get('app_language', 0)

    def save_settings_data(self):
        if self.__local_data_path is not None:
            with (self.__local_data_path / 'settings.json').open(mode='w', encoding='utf-8-sig') as settings:
                json.dump(self.__settings, settings, indent=4)


class Performer(QObject):
    info_console_value = pyqtSignal(str)
    info_label_value = pyqtSignal(str)
    progress_bar_value = pyqtSignal(float)
    finish_thread = pyqtSignal()

    def __init__(self, paths: Prepper, original_language: str = None, target_language: str = None,
                 need_translate: bool = False, need_translate_tuple: tuple | None = None):
        super(Performer, self).__init__()
        self.__paths = paths
        self.__original_language = original_language
        self.__target_language = target_language
        self.__translator = GoogleTranslator(source=self.__original_language, target=self.__target_language)
        self.__need_translate_list = need_translate_tuple if need_translate is True else tuple()

        self.__start_running_time = None
        self.__original_language_dictionary = {}
        self.__current_process_file: str = ''
        self.__current_original_lines = []
        self.__original_vanilla_dictionary = {}
        self.__target_vanilla_dictionary = {}
        self.__previous_version_dictionary = {}
        self.__modified_values = {}
        self.__translated_list = []

    def __calculate_time_delta(self) -> str:
        start_time = self.__start_running_time
        current_time = time.time()
        delta = current_time - start_time
        return time.strftime('%H:%M:%S', time.gmtime(delta))

    def __create_directory_hierarchy(self):
        info = f"{LanguageConstants.start_forming_hierarchy} {self.__calculate_time_delta()}\n"
        self.info_console_value.emit(self.__change_text_style(info, 'green'))
        self.info_label_value.emit(LanguageConstants.forming_process)
        if not self.__paths.get_target_path().exists():
            self.__paths.get_target_path().mkdir(parents=True)
        for file in self.__paths.get_file_hierarchy():
            file: Path
            directory = Path(str(file).replace(self.__original_language, self.__target_language)).parent
            try:
                if not (self.__paths.get_target_path() / directory).exists():
                    (self.__paths.get_target_path() / directory).mkdir()
                    info = f"{LanguageConstants.folder_created} {directory} - {self.__calculate_time_delta()}\n"
                    self.info_console_value.emit(info)
            except Exception as error:
                error_text = f"{LanguageConstants.error_with_folder_creating} {directory}:" \
                             f"{error}"
                self.info_console_value.emit(self.__change_text_style(error_text, 'red'))
                self.info_label_value.emit(self.__change_text_style(f'{LanguageConstants.thread_stopped}', 'red'))
                self.finish_thread.emit()

    def __create_original_language_dictionary(self):
        r"""Создает словарь, состоящий из номера строки, в качестве ключа и словаря, в качестве значения
        Каждый словарь содержит пару ключ-значение: key: 'key', value: 'value'
        К применру: 11: {'key': 'AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0',
                        'value': ' AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0 " No order."'},
        Здесь 11 - номер строки, а key - ключ(идентификатор) полной строки value.
        А также в value уже обрезаны пробелы и  символы переноса строки справа"""
        self.__original_language_dictionary = {}
        num_str = 0
        for line in self.__current_original_lines:
            key = self.__get_localization_key(line=line)
            if key is None:
                key = "not_program_data"
            self.__original_language_dictionary[num_str] = {"key": key, "value": line.rstrip()}
            num_str += 1
        self.__translated_list = ['' for _ in range(len(self.__current_original_lines))]

    def __create_game_localization_dictionary(self):
        self.info_console_value.emit(f'{LanguageConstants.localization_dict_creating_started}'
                                     f' - {self.__calculate_time_delta()}\n')
        self.info_label_value.emit(LanguageConstants.game_localization_processing)
        original_vanilla_path = self.__paths.get_game_path() / self.__original_language
        target_vanilla_path = self.__paths.get_game_path() / self.__target_language
        for file in original_vanilla_path.rglob('*'):
            self.__original_vanilla_dictionary | self.__process_file(file=file)
        for file in target_vanilla_path.rglob('*'):
            self.__target_vanilla_dictionary | self.__process_file(file=file)

    def __process_file(self, file: Path):
        localization_dict = {}
        if file.is_file() and file.suffix in ['.yml', '.txt', ]:
            try:
                with file.open(mode='r', encoding='utf-8-sig') as file:
                    for line in file.readlines():
                        localization_key = self.__get_localization_key(line=line)
                        if localization_key is not None:
                            localization_dict[localization_key] = line.rstrip()
            except Exception as error:
                error_text = f"{LanguageConstants.error_with_file_processing} {str(file)} - {error}"
                self.info_console_value.emit(self.__change_text_style(error_text, 'red'))
        return localization_dict

    def __create_previous_version_dictionary(self):
        self.info_console_value.emit(f'{LanguageConstants.previous_localization_dict_creating_started} -'
                                     f' {self.__calculate_time_delta()}\n')
        self.info_label_value.emit(LanguageConstants.previous_localization_processing)
        self.__previous_version_dictionary = {"lang": "l_" + self.__target_language + ":\n"}
        for file in self.__paths.get_previous_files():
            file: Path
            try:
                with file.open(mode='r', encoding='utf-8-sig') as file_with_previous_version:
                    for line in file_with_previous_version.readlines():
                        localization_key = self.__get_localization_key(line=line)
                        if localization_key is not None:
                            self.__previous_version_dictionary[localization_key] = line
            except Exception as error:
                error_text = f"{LanguageConstants.error_with_file_processing} {str(file)} - {error}"
                self.info_console_value.emit(self.__change_text_style(error_text, 'red'))

    def __create_translated_list(self, line_number: int, key_value: dict):
        if line_number == 0:
            self.__translated_list[0] = "l_" + self.__target_language + ":\n"
        else:
            match self.__paths.get_previous_path_validate_result():
                case True:
                    self.__translated_list[line_number] = self.__compare_with_previous(key_value=key_value) + "\n"
                case False:
                    self.__translated_list[line_number] = self.__compare_with_vanilla(key_value=key_value) + "\n"

    def __compare_with_previous(self, key_value) -> str:
        previous_line = self.__previous_version_dictionary.get(key_value['key'], None)
        if previous_line is None:
            return self.__compare_with_vanilla(key_value=key_value)
        else:
            return previous_line

    def __compare_with_vanilla(self, key_value: dict) -> str:
        original_vanilla_value = self.__original_vanilla_dictionary.get(key_value["key"], None)
        target_vanilla_value = self.__target_vanilla_dictionary.get(key_value["key"], None)
        if original_vanilla_value is not None and target_vanilla_value is not None:
            if original_vanilla_value == key_value["value"]:
                return target_vanilla_value
        if key_value["value"] == "":
            return key_value["value"]
        else:
            return self.__translate_line(translator=self.__translator, line=key_value["value"])

    def __translate_line(self, translator: GoogleTranslator | None, line: str) -> str:
        r"""На вход должна подаваться строка с уже обрезанным символом переноса строки"""
        if self.__current_process_file in self.__need_translate_list:
            translate_flag = True
        else:
            translate_flag = False
        if translate_flag is False:
            return line + " #NT!"
        else:
            localization_value = self.__get_localization_value(line=line)
            if localization_value is None:
                return line
            else:
                try:
                    modified_line = self.__modify_line(line=localization_value, flag="modify")
                    translated_line = translator.translate(text=modified_line[1:-1])
                    normal_string = self.__modify_line(line=translated_line, flag="return_normal_view")
                    return line + f" <\"{normal_string}\">" + " #NT!"
                except Exception as error:
                    error_text = f"{LanguageConstants.error_with_translation}\n{line}\n{error}\n"
                    self.info_console_value.emit(self.__change_text_style(error_text, 'red'))
                    return line + " #Translation Error!"

    def __modify_line(self, line: str, pattern: str | None = r"\[.*?\]", flag: str | None = None) -> str | None:
        r"""При флаге "modify" позволяет заменить некоторые части строки по шаблону на скрытую, ничего не обозначающую
        переменную. При флаге "return_normal_view" позволяет вернуть нормальный вид строки по словарю параметров"""
        match flag:
            case "modify":
                self.__modified_values = {}
                shadow_number = 0
                regular_groups = re.findall(pattern=pattern, string=line)
                if regular_groups:
                    for step in regular_groups:
                        self.__modified_values[f"[{shadow_number}]"] = step
                        line = line.replace(step, f"[{shadow_number}]")
                        shadow_number += 1
                return line
            case "return_normal_view":
                for key, value in self.__modified_values.items():
                    line = line.replace(key, value)
                return line
            case _:
                self.info_console_value(LanguageConstants.error_with_modification)
                self.finish_thread.emit()

    @staticmethod
    def __change_text_style(text: str, flag):
        match flag:
            case 'red':
                return f'<span style=\" color: red;\">' + text + '</span>'
            case 'green':
                return f'<span style=\" color: green;\">' + text + '</span>'
            case 'orange':
                return f'<span style=\" color: orange;\">' + text + '</span>'

    @staticmethod
    def __get_localization_key(pattern=r"(.*:)(\d*)( *)(\".*\")", line='') -> str | None:
        separated_line = re.findall(pattern=pattern, string=line)
        if separated_line:
            return separated_line[0][0].lstrip()
        else:
            return None

    @staticmethod
    def __get_localization_value(pattern: str = r'(\".*\D+?.*\")', line: str = ''):
        value = re.findall(pattern=pattern, string=line)
        if value:
            return value[0]

    def __process_data(self):
        r"""Здесь происходит процесс обработки файлов. Последовательное открытие, создание и запись"""
        self.info_console_value.emit(f'{LanguageConstants.start_file_processing} - {self.__calculate_time_delta()}\n')
        for file in self.__paths.get_file_hierarchy():
            self.__current_process_file = file
            original_file_full_path = self.__paths.get_original_mode_path() / file
            changed_file_full_path = self.__paths.get_target_path() / str(file).replace(self.__original_language,
                                                                                        self.__target_language)
            try:
                with original_file_full_path.open(mode='r', encoding='utf-8-sig') as original_file, \
                        changed_file_full_path.open(mode='w', encoding='utf-8-sig') as target_file:
                    info = f"{LanguageConstants.file_opened} {file} - {self.__calculate_time_delta()}\n"
                    self.info_console_value.emit(info)
                    self.__current_original_lines = original_file.readlines()
                    amount_lines = len(self.__current_original_lines)
                    self.__create_original_language_dictionary()
                    for line_number, key_value in self.__original_language_dictionary.items():
                        self.__create_translated_list(line_number=line_number, key_value=key_value)
                        info = f"{LanguageConstants.process_string} {line_number + 1}/{amount_lines}\n" \
                               f"{LanguageConstants.of_file} {str(original_file_full_path.name)}"
                        self.info_label_value.emit(info)
                        self.progress_bar_value.emit(original_file_full_path.stat().st_size /
                                                     len(self.__current_original_lines) /
                                                     self.__paths.get_original_files_size())
                    print(*self.__translated_list, file=target_file, sep='', end='')
            except Exception as error:
                error_info = f"{LanguageConstants.error_with_data_processing}:\n {error}\n"
                self.info_console_value.emit(self.__change_text_style(error_info, 'red'))

    def run(self):
        self.__start_running_time = time.time()
        self.__create_directory_hierarchy()
        self.__create_game_localization_dictionary()
        if self.__paths.get_previous_path_validate_result():
            self.__create_previous_version_dictionary()
        self.__process_data()
        info = f"{LanguageConstants.final_time} {self.__calculate_time_delta()}"
        self.info_console_value.emit(self.__change_text_style(info, 'orange'))
        self.info_label_value.emit(LanguageConstants.final)
        self.finish_thread.emit()
