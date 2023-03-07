from PyQt5 import QtCore


class LanguageConstants:
    menu = ''
    settings = ''
    program_version = ''

    start_forming_hierarchy = ''
    start_file_processing = ''
    file_opened = ''
    forming_process = ''
    folder_created = ''
    error_with_data_processing = ''
    error_with_folder_creating = ''
    error_with_file_processing = ''
    error_with_modification = ''
    error_with_translation = ''
    thread_stopped = ''
    localization_dict_creating_started = ''
    game_localization_processing = ''
    of_file = ''
    previous_localization_dict_creating_started = ''
    previous_localization_processing = ''
    process_string = ''
    final = ''
    final_time = ''

    error_settings_file_not_exist = ''
    error_folder_does_not_exist = ''
    error_drive_not_exist = ''

    warning_disable_original_line = ''

    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate
        cls.menu = _translate("Constants", "&Меню")
        cls.settings = _translate("Constants", "Настройки")
        cls.program_version = _translate("Constants", "Версия")

        cls.start_forming_hierarchy = _translate("Constants", "Начато формирование иерархии директорий -")
        cls.start_file_processing = _translate("Constants", "Начата обработка файлов")
        cls.file_opened = _translate("Constants", "Начата работа с файлом")
        cls.forming_process = _translate("Constants", "Формирую иерархию\nдиректорий")
        cls.error_with_data_processing = _translate("Constants", "Произошла ошибка")
        cls.folder_created = _translate("Constants", "Создана папка")
        cls.error_with_folder_creating = _translate("Constants", "Произошла ошибка при попытке создания директории")
        cls.error_with_file_processing = _translate("Constants", "Произошла ошибка при обработке файла")
        cls.error_with_modification = _translate("Constants", "Ошибка при модификации, флаг нечитаем")
        cls.error_with_translation = _translate("Constants", "Произошла ошибка с переводом строки:")
        cls.thread_stopped = _translate("Constants", "Поток обработки остановлен")
        cls.localization_dict_creating_started = _translate("Constants", "Начато создание словаря игровой локализации")
        cls.game_localization_processing = _translate("Constants", "Обработка игровой локализации")
        cls.of_file = _translate("Constants", "файла")
        cls.previous_localization_dict_creating_started = _translate("Constants", "Начато создание словаря предыдущей локализации")
        cls.previous_localization_processing = _translate("Constants", "Обработка предыдущей локализации")
        cls.process_string = _translate("Constants", "Обработка строки")
        cls.final = _translate("Constants", "Обработка данных закончена")
        cls.final_time = _translate("Constants", "Программа закончила свою работу за")

        cls.error_settings_file_not_exist = _translate("Constants", "Место хранения настроек - не найдено")
        cls.error_folder_does_not_exist = _translate("Constants", "Директория не существует")
        cls.error_drive_not_exist = _translate("Constants", "Выбранный диск не существует")

        cls.warning_disable_original_line = _translate("Constants", "Внимание!\nАвтор программы считает, что при включении данной функции сильно пострадает качество перевода. Включайте на свой страх и риск. После работы программы вы получите полностью машинный перевод с огромным количеством ошибок! Проверяйте перевод перед его публикацией где-либо!")


