import json
from pathlib import Path
import re
import time
from typing import KeysView

from PyQt5.QtCore import QObject, pyqtSignal
from deep_translator import GoogleTranslator
from deepl import QuotaExceededException

from info_data import InfoData, FileInfoData
from languages.language_constants import LanguageConstants

from loguru import logger

from parsers.modern_paradox_parser import ModernParadoxParser
from settings import BASE_DIR
from shielded_values import ShieldedValues
from translators.translator_manager import TranslatorManager


class Prepper:

    @logger.catch()
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

    @logger.catch()
    def set_game_path(self, game_path: str):
        r"""Должен формировать путь до папки с локализациями (game/localization, localisation и т.п.)"""
        self._game_path = Path(game_path)
        self._game_path_validate_result = self.validator.validate_game_path(self._game_path)

    @logger.catch()
    def get_game_path(self) -> Path:
        return self._game_path

    @logger.catch()
    def get_game_path_validate_result(self) -> bool:
        return self._game_path_validate_result

    @logger.catch()
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

    @logger.catch()
    def set_previous_path(self, previous_path: str, target_language: str):
        if previous_path:
            self._previous_path = Path(previous_path)
            self._previous_path_validate_result = self.validator.validate_previous_path(
                self._previous_path / target_language)
        else:
            self._previous_path = Path('.')
            self._previous_path_validate_result = False

    def get_previous_path(self) -> Path:
        return self._previous_path

    def get_previous_path_validate_result(self) -> bool:
        return self._previous_path_validate_result

    @logger.catch()
    def set_target_path(self, target_path: str):
        self._target_path = Path(target_path)
        self._target_path_validate_result = self.validator.validate_target_path(self._target_path)

    def get_target_path(self) -> Path:
        return self._target_path

    def get_target_path_validate_result(self) -> bool:
        return self._target_path_validate_result

    @logger.catch()
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

    @logger.catch()
    def get_previous_files(self, target_language: str):
        self._previous_files = []
        replace_path = self._previous_path / 'replace' / target_language
        target_path = self._previous_path / target_language
        if replace_path.exists():
            for file in replace_path.rglob('*'):
                self._previous_files.append(file)
        for step in target_path.rglob('*'):
            if step.is_file():
                self._previous_files.append(step)
        return self._previous_files


class Validator:

    def __init__(self):
        pass

    @staticmethod
    @logger.catch()
    def __path_existence(path: Path) -> bool:
        return path.exists()

    @staticmethod
    @logger.catch()
    def __drive_existence(path: Path) -> bool:
        drive_existence = Path(path.drive).exists() and bool(re.findall('.+:.+', str(path)))
        return drive_existence

    @logger.catch()
    def validate_game_path(self, path: Path):
        drive_existence = self.__drive_existence(path)
        path_existence = self.__path_existence(path)
        logger.debug(f'{path} - Full path: {path_existence}, Drive: {drive_existence}')
        return path_existence and drive_existence

    @logger.catch()
    def validate_original_path(self, path: Path, original_language: str):
        drive_existence = False
        path_existence = False
        if original_language is not None:
            path_existence = self.__path_existence(path / original_language)
            drive_existence = self.__drive_existence(path)
        logger.debug(f'{path}/{original_language} - Full path: {path_existence}, Drive: {drive_existence}')
        return path_existence and drive_existence

    @logger.catch()
    def validate_previous_path(self, path: Path):
        path_existence = self.__path_existence(path) and self.__drive_existence(path)
        logger.debug(f'{path} - Full path: {path_existence}')
        return path_existence

    @logger.catch()
    def validate_target_path(self, path: Path):
        path_existence = self.__drive_existence(path)
        logger.debug(f'drive - Full path: {path_existence}')
        return path_existence


class Settings:
    __settings = {
        'last_game_directory': "",
        'last_original_mode_directory': "",
        'last_previous_directory': "",
        'last_target_directory': "",
        'last_supported_source_language': 'english',
        'last_supported_target_language': 'english',
        'last_original_language': "english",
        'last_target_language': "russian",

        'translator_api': "GoogleTranslator",
        'protection_symbol': "☻",

        'app_language': "Русский",
        'games': {},
        'selected_game': 'Crusader Kings 3',
        'app_size': [1300, 700],
        'app_position': [100, 50],
    }

    @logger.catch()
    def __init__(self, local_data_path: Path | None):
        self.__local_data_path = local_data_path
        if self.__local_data_path:
            if self.__local_data_path.exists() and (self.__local_data_path / 'settings.json').exists():
                with (self.__local_data_path / 'settings.json').open(mode='r', encoding='utf-8-sig') as settings:
                    self.__settings = self.__settings | json.load(settings)
            else:
                Path.mkdir(self.__local_data_path, exist_ok=True)
                logger.debug(f'Settings directory - created: {local_data_path}')
                self.save_settings_data()
            self.disable_original_line = False
        else:
            logger.warning(f'settings storage: {local_data_path}: not exists')

        self.__init_games()

    @logger.catch()
    def __init_games(self):
        game_supported_languages = BASE_DIR / 'game_supported_languages.json'
        with game_supported_languages.open(mode='r', encoding='utf-8-sig') as file:
            self.__settings['games'] = json.load(file)

    def get_games(self) -> KeysView:
        return self.__settings.get('games').keys()

    def set_selected_game(self, game: str):
        self.__settings['selected_game'] = game

    def get_selected_game(self):
        return self.__settings.get('selected_game')

    def get_game_languages(self, game: str):
        return self.__settings.get('games').get(game, [])

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

    def set_last_supported_source_language(self, source):
        self.__settings['last_supported_source_language'] = source

    def set_last_supported_target_language(self, target):
        self.__settings['last_supported_target_language'] = target

    def set_translator_api(self, translator_api):
        self.__settings['translator_api'] = translator_api

    def set_protection_symbol(self, symbol):
        self.__settings['protection_symbol'] = symbol

    def set_app_language(self, value):
        self.__settings['app_language'] = value

    def set_app_size(self, width, height):
        self.__settings['app_size'] = [width, height]

    def set_app_position(self, x, y):
        self.__settings['app_position'] = [x, y]

    def get_last_original_language(self):
        return self.__settings.get('last_original_language', 'english')

    def get_last_target_language(self):
        return self.__settings.get('last_target_language', 'russian')

    def get_last_supported_source_language(self):
        return self.__settings.get('last_supported_source_language', 'english')

    def get_last_supported_target_language(self):
        return self.__settings.get('last_supported_target_language', 'english')

    def get_translator_api(self):
        return self.__settings.get('translator_api', None)

    def get_protection_symbol(self):
        return self.__settings.get('protection_symbol', None)

    def get_app_language(self):
        return self.__settings.get('app_language', 0)

    def get_app_size(self):
        return self.__settings.get('app_size', None)

    def get_app_position(self) -> [int, int]:
        return self.__settings.get('app_position', None)

    def save_settings_data(self):
        if self.__local_data_path is not None:
            with (self.__local_data_path / 'settings.json').open(mode='w', encoding='utf-8-sig') as settings:
                json.dump(self.__settings, settings, indent=4)


class TranslatorAccount:
    def __init__(self, local_path: Path):
        self.__translator_accounts_path = local_path / 'translator accounts.json'
        if self.__translator_accounts_path.exists():
            with self.__translator_accounts_path.open(mode='r', encoding='utf-8-sig') as accounts:
                self.__translator_accounts = json.load(accounts)
        else:
            with self.__translator_accounts_path.open(mode='w') as accounts:
                self.__translator_accounts = {}
                json.dump(self.__translator_accounts, accounts, indent=4)

    def get_translator_account(self, translator_name) -> dict:
        return self.__translator_accounts.get(translator_name, {})

    def add_new_account(self, translator_name: str, **data):
        self.__translator_accounts[translator_name] = data

    def save_accounts(self):
        with self.__translator_accounts_path.open(mode='w', encoding='utf-8-sig') as accounts:
            json.dump(self.__translator_accounts, accounts, indent=4)


class BasePerformer(QObject):
    info_data: InfoData
    file_info_data: FileInfoData

    info_console_value = pyqtSignal(str)
    info_label_value = pyqtSignal(str)
    progress_bar_value = pyqtSignal(float)
    finish_thread = pyqtSignal(InfoData)

    @logger.catch()
    def __init__(
            self,
            paths: Prepper,
            translator: TranslatorManager = None,
            original_language: str = None,
            target_language: str = None,
            need_translate: bool = False,
            need_translate_tuple: tuple | None = None,
            disable_original_line: bool = False,
            protection_symbol: str = "☻"
    ):
        super(BasePerformer, self).__init__()
        self._paths = paths
        self._original_language = original_language
        self._target_language = target_language
        self._translator = translator
        self._need_translate_list = need_translate_tuple if need_translate is True else tuple()
        self._disable_original_line = disable_original_line
        self._protection_symbol = protection_symbol

        self._shielded_values = ShieldedValues.get_common_pattern()

        self._start_running_time = None
        self._original_language_list = {}
        self._current_process_file: str = ''
        self._current_original_lines = []
        self._original_vanilla_dictionary = {}
        self._target_vanilla_dictionary = {}
        self._previous_version_dictionary = {}
        self._modified_values = {}
        self._translated_list = []

    @logger.catch()
    def _calculate_time_delta(self, start_time: float = None) -> str:
        if not start_time:
            start_time = self._start_running_time
        current_time = time.time()
        delta = current_time - start_time
        return time.strftime('%H:%M:%S', time.gmtime(delta))

    @logger.catch()
    def _create_directory_hierarchy(self):
        info = f"{LanguageConstants.start_forming_hierarchy} {self._calculate_time_delta()}\n"
        self.info_console_value.emit(self._change_text_style(info, 'green'))
        self.info_label_value.emit(LanguageConstants.forming_process)
        logger.debug(f'{info}')
        if not self._paths.get_target_path().exists():
            logger.debug(f'Making target directories')
            self._paths.get_target_path().mkdir(parents=True)
        logger.debug(f'Hierarchy creating start.')
        for file in self._paths.get_file_hierarchy():
            file: Path
            logger.debug(f'Creating {str(file)}')
            directory = Path(str(file).replace(self._original_language, self._target_language)).parent
            try:
                if not (self._paths.get_target_path() / directory).exists():
                    (self._paths.get_target_path() / directory).mkdir(parents=True)
                    info = f"{LanguageConstants.folder_created} {directory} - {self._calculate_time_delta()}\n"
                    self.info_console_value.emit(info)
            except Exception as error:
                error_text = f"{LanguageConstants.error_with_folder_creating} {directory}:" \
                             f"{error}"
                self.info_console_value.emit(self._change_text_style(error_text, 'red'))
                self.info_label_value.emit(self._change_text_style(f'{LanguageConstants.thread_stopped}', 'red'))
                self.finish_thread.emit()

    @logger.catch()
    def _create_original_language_dictionary(self):
        r"""Создает словарь, состоящий из номера строки, в качестве ключа и словаря, в качестве значения
        Каждый словарь содержит пару ключ-значение: key: 'key', value: 'value'
        К применру: 11: {'key': 'AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0',
                        'value': '" No order."'},
        Здесь 11 - номер строки, а key - ключ(идентификатор) полной строки value.
        А также в value уже обрезаны пробелы и  символы переноса строки справа"""
        pass

    @logger.catch()
    def _create_game_localization_dictionary(self):
        pass

    @logger.catch()
    def _get_lines_dictionary(self, file: Path) -> dict:
        pass

    @logger.catch()
    def _create_previous_version_dictionary(self):
        pass

    @logger.catch()
    def _create_translated_list(self, line_number: int, key_value: dict):
        pass

    @logger.catch()
    def _compare_with_previous(self, key_value) -> str:
        pass

    @logger.catch()
    def _compare_with_vanilla(self, key_value: dict) -> str:
        pass

    @logger.catch()
    def _translate_line(self, translator: GoogleTranslator | None, key_value: dict) -> str:
        pass

    @logger.catch()
    def _modify_line(self, line: str, pattern: str | None = r"\[.*?\]", flag: str | None = None) -> str | None:
        r"""При флаге "modify" позволяет заменить некоторые части строки по шаблону на скрытую, ничего не обозначающую
        переменную. При флаге "return_normal_view" позволяет вернуть нормальный вид строки по словарю параметров"""
        match flag:
            case "modify":
                self._modified_values = {}
                shadow_number = 0
                regular_groups = re.findall(pattern=pattern, string=line)
                logger.debug(f'Found params for modify - {regular_groups}')
                if regular_groups:
                    for step in regular_groups:
                        self._modified_values[shadow_number] = step
                        if self._translator == "GoogleTranslator":
                            line = line.replace(step, f"{self._protection_symbol}_{shadow_number}")
                        elif self._translator == "DeepLTranslator":
                            line = line.replace(step, f'<span translate="no">{step}</span>')
                        shadow_number += 1
                return line
            case "return_normal_view":
                if self._translator == "GoogleTranslator":
                    for key, value in self._modified_values.items():
                        line = line.replace(f'☻_{key}', value)
                if self._translator == "DeepLTranslator":
                    tags = re.findall(pattern=r'(<[^>]*translate=\"no\"[^>]*>).*?(<[^>]*>)', string=line)
                    for open_tag, close_tag in tags:
                        line = line.replace(open_tag, '').replace(close_tag, '')
                return line
            case _:
                self.info_console_value(LanguageConstants.error_with_modification)
                self.finish_thread.emit()

    @staticmethod
    @logger.catch()
    def _change_text_style(text: str, flag):
        match flag:
            case 'red':
                return f'<span style=\" color: red;\">' + text + '</span>'
            case 'green':
                return f'<span style=\" color: green;\">' + text + '</span>'
            case 'orange':
                return f'<span style=\" color: orange;\">' + text + '</span>'

    @logger.catch()
    def _process_data(self):
        r"""Здесь происходит процесс обработки файлов. Последовательное открытие, создание и запись"""
        pass

    def run(self):
        logger.info(f'Process start')
        self._start_running_time = time.time()
        self._create_directory_hierarchy()
        self._create_game_localization_dictionary()
        if self._paths.get_previous_path_validate_result():
            self._create_previous_version_dictionary()
        self._process_data()
        info = f"{LanguageConstants.final_time} {self._calculate_time_delta()}"
        self.info_console_value.emit(self._change_text_style(info, 'orange'))
        self.info_label_value.emit(LanguageConstants.final)
        self.finish_thread.emit(self.info_data)


class ModernParadoxGamesPerformer(BasePerformer):

    def __init__(self, *args, **kwargs):
        super(ModernParadoxGamesPerformer, self).__init__(*args, **kwargs)
        self._default_padding = 1

    @logger.catch()
    def _create_original_language_dictionary(self, filename):
        r"""Создает словарь, состоящий из номера строки, в качестве ключа и словаря, в качестве значения
        Каждый словарь содержит пару ключ-значение: key: 'key', value: 'value'
        К применру: 11: {'key': 'AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0',
                        'value': " No order."'},
        Здесь 11 - номер строки, а key - ключ(идентификатор) полной строки value.
        А также в value уже обрезаны пробелы и  символы переноса строки справа"""
        self._original_language_list = []
        self._original_language_list = ModernParadoxParser(filename=filename).parse_file(get_list=True)
        logger.info(f'List with key_value: {self._original_language_list}')
        self._translated_list = ['' for _ in range(len(self._original_language_list))]

    @logger.catch()
    def _create_game_localization_dictionary(self):
        self.info_console_value.emit(f'{LanguageConstants.localization_dict_creating_started}'
                                     f' - {self._calculate_time_delta()}\n')
        self.info_label_value.emit(LanguageConstants.game_localization_processing)
        original_vanilla_path = self._paths.get_game_path() / self._original_language
        target_vanilla_path = self._paths.get_game_path() / self._target_language
        for file in original_vanilla_path.rglob('*'):
            lines_dictionary = ModernParadoxParser(filename=file).parse_file()
            self._original_vanilla_dictionary |= lines_dictionary
        for file in target_vanilla_path.rglob('*'):
            lines_dictionary = ModernParadoxParser(filename=file).parse_file()
            self._target_vanilla_dictionary |= lines_dictionary

    @logger.catch()
    def _create_previous_version_dictionary(self):
        self.info_console_value.emit(f'{LanguageConstants.previous_localization_dict_creating_started} -'
                                     f' {self._calculate_time_delta()}\n')
        self.info_label_value.emit(LanguageConstants.previous_localization_processing)
        self._previous_version_dictionary = {"lang": "l_" + self._target_language + ":\n"}
        for file in self._paths.get_previous_files(target_language=self._target_language):
            file: Path
            self._previous_version_dictionary |= ModernParadoxParser(filename=file).parse_file()

    @logger.catch()
    def _create_translated_list(self, key_value: dict):
        if self._current_line_number == 0:
            self._translated_list[0] = "l_" + self._target_language + ":\n"
        else:
            match self._paths.get_previous_path_validate_result():
                case True:
                    self._translated_list[self._current_line_number] = " " * self._default_padding \
                                                         + self._compare_with_previous(key_value=key_value) + "\n"
                case False:
                    self._translated_list[self._current_line_number] = " " * self._default_padding \
                                                         + self._compare_with_vanilla(key_value=key_value) + "\n"

    @logger.catch()
    def _compare_with_previous(self, key_value) -> str:
        previous_line = self._previous_version_dictionary.get(key_value['key'], '')
        if not previous_line.strip():
            previous_line = None
        logger.debug(f'Key - Value: {key_value}')
        if previous_line is None:
            if not key_value['value'] in ["", None]:
                self.file_info_data.add_new_line(self._current_line_number)
            logger.debug(f'Previous is {previous_line} if line is {key_value["value"]}')
            return self._compare_with_vanilla(key_value=key_value)
        else:
            self.file_info_data.add_line_from_previous_version(self._current_line_number)
            return " ".join((key_value['key'], previous_line))

    @logger.catch()
    def _compare_with_vanilla(self, key_value: dict) -> str:
        original_vanilla_value = self._original_vanilla_dictionary.get(key_value["key"], None)
        target_vanilla_value = self._target_vanilla_dictionary.get(key_value["key"], None)
        logger.debug(f'Original value - {"found" if original_vanilla_value is not None else None}, '
                     f'Target value - {"found" if target_vanilla_value is not None else None} ')
        if original_vanilla_value is not None and target_vanilla_value is not None:
            if original_vanilla_value == key_value["value"]:
                logger.debug(f'Return vanilla value')
                self.file_info_data.add_line_from_vanilla_loc(self._current_line_number)
                return " ".join((key_value["key"], target_vanilla_value))
        if key_value["value"] in ["", None]:
            logger.debug('String is empty')
            return " ".join((key_value["key"], key_value["value"]))
        else:
            return self._translate_line(translator=self._translator, key_value=key_value)

    @logger.catch()
    def _translate_line(self, translator: TranslatorManager | None, key_value: dict) -> str:
        r"""На вход должна подаваться строка с уже обрезанным символом переноса строки"""
        if self._current_process_file in self._need_translate_list:
            translate_flag = True
            logger.debug(f'Current file is checked for translating')
        else:
            translate_flag = False
            logger.debug(f'Current file is not checked for translating')
        if translate_flag is False:
            return " ".join((key_value["key"], key_value["value"], "#NT!"))
        else:
            localization_value = key_value["value"]
            logger.debug(f'Only text from line - {localization_value}')
            if localization_value[1:-1].strip() == "":
                return " ".join((key_value["key"], key_value["value"]))
            else:
                try:
                    modified_line = self._modify_line(line=localization_value, flag="modify",
                                                      pattern=self._shielded_values)
                    translated_line = translator.translate(text=modified_line[1:-1])
                    normal_string = self._modify_line(line=translated_line, flag="return_normal_view")
                    self.file_info_data.add_translated_line(self._current_line_number)
                    self.info_data.add_translated_chars(len(modified_line[1:-1]))
                    self.file_info_data.add_api_service(translator.get_api_name())
                    if self._disable_original_line:
                        return " ".join((key_value["key"],
                                         key_value["value"].replace(localization_value, f'\"{normal_string}\"'),
                                         '#NT!'))
                    return " ".join((key_value["key"], key_value["value"], f" <\"{normal_string}\">", " #NT!"))
                except QuotaExceededException as error_text:
                    error_text = f'{LanguageConstants.error_quota_exceeded} - {error_text}'
                    logger.warning(error_text)
                    translator.set_new_api_service(api_service='GoogleTranslator',
                                                   last_source=translator.get_source_language(),
                                                   last_target=translator.get_target_language())
                    self.info_console_value.emit(f'{LanguageConstants.api_service_changed}{translator.get_api_name()}')
                    self.file_info_data.add_api_service('GoogleTranslator')
                    self.info_data.add_api_service('GoogleTranslator')
                    self.info_console_value.emit(self._change_text_style(error_text, 'red'))
                    return self._translate_line(translator=translator, key_value=key_value)
                except Exception as error:
                    self.file_info_data.add_line_with_error(self._current_line_number)
                    error_text = f"{LanguageConstants.error_with_translation}\n{key_value['value']} {key_value['value']}\n{error}\n"
                    logger.error(f'{error_text}')
                    self.info_console_value.emit(self._change_text_style(error_text, 'red'))
                    return " ".join((key_value['key'], key_value['value'], "#Translation Error!"))

    @logger.catch()
    def _process_data(self):
        r"""Здесь происходит процесс обработки файлов. Последовательное открытие, создание и запись"""
        self.info_console_value.emit(f'{LanguageConstants.start_file_processing} - {self._calculate_time_delta()}\n')
        self.info_data = InfoData(self._paths.get_target_path().name)
        for file in self._paths.get_file_hierarchy():
            start_time = time.time()

            logger.info(f'Started file {file}')
            self._current_process_file = file
            original_file_full_path = self._paths.get_original_mode_path() / file
            changed_file_full_path = self._paths.get_target_path() / str(file).replace(self._original_language,
                                                                                       self._target_language)
            self.file_info_data = FileInfoData(filename=changed_file_full_path)
            with changed_file_full_path.open(mode='w', encoding='utf-8-sig') as target_file:
                info = f"{LanguageConstants.file_opened} {file} - {self._calculate_time_delta()}\n"
                self.info_console_value.emit(info)

                self._create_original_language_dictionary(original_file_full_path)
                amount_lines = len(self._original_language_list)
                self.file_info_data.set_lines_in_files(amount_lines)
                self.info_data.add_api_service(self._translator.get_api_name())
                for line_number, key_value in enumerate(self._original_language_list):
                    self._current_line_number = line_number
                    self._create_translated_list(key_value=key_value)
                    info = f"{LanguageConstants.process_string} {line_number + 1}/{amount_lines}\n" \
                           f"{LanguageConstants.of_file} {str(original_file_full_path.name)}"
                    self.info_label_value.emit(info)
                    self.progress_bar_value.emit(original_file_full_path.stat().st_size /
                                                 amount_lines /
                                                 self._paths.get_original_files_size())
                print(*self._translated_list, file=target_file, sep='', end='')
            self.file_info_data.set_process_time(self._calculate_time_delta(start_time=start_time))
            self.info_data.add_file_info(self.file_info_data)
            self.info_data.add_translated_files()
