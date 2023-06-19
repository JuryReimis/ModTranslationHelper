import re
from pathlib import Path

from loguru import logger


class ModernParadoxParser:
    def __init__(self, filename: Path):
        self._filename = filename

    @logger.catch()
    def parse_file(self, get_list: bool = False) -> dict | list:
        if get_list:
            result_storage = []
        else:
            result_storage = {}
        if self._filename.is_file() and self._filename.suffix in ['.yml', '.txt', ]:
            with self._filename.open(mode='r', encoding='utf-8-sig') as file:
                lines = file.readlines()
                for line in lines:
                    key = self._get_localization_key(line=line)
                    value = self._get_localization_value(line=line)
                    if get_list:
                        result_storage.append({'key': key, 'value': value})
                    else:
                        result_storage[key] = value
        return result_storage

    @staticmethod
    def _get_localization_key(pattern=r"(.*:)(\d*)( *)(\".*\")", line='') -> str | None:
        separated_line = re.findall(pattern=pattern, string=line)
        if separated_line:
            return separated_line[0][0].strip()
        else:
            return line.rstrip()

    @staticmethod
    def _get_localization_value(pattern: str = r'(\".*\w*?.*\")', line: str = '') -> str | None:
        value = re.findall(pattern=pattern, string=line)
        if value:
            return value[0].rstrip()
        else:
            return ''
