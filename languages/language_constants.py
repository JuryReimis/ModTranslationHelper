from PyQt5 import QtCore


class LanguageConstants:
    menu = ''
    settings = ''
    program_version = ''

    game_directory_help = ''
    original_directory_help = ''
    previous_directory_help = ''
    target_directory_help = ''
    need_translation_help = ''
    disable_original_line_help = ''
    choice_supported_source_language_help = ''
    choice_supported_target_language_help = ''

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
    error_quota_exceeded = ''
    api_service_changed = ''
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
    error_path_not_exists = ''

    warning_disable_original_line = ''
    warning_disable_original_line_title = ''

    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate
        cls.menu = _translate("Constants", "&Меню")
        cls.settings = _translate("Constants", "Настройки")
        cls.program_version = _translate("Constants", "Версия")

        cls.game_directory_help = _translate("Constants",
                                             "Место, где установлена игра, для которой вы собираетесь переводить. Путь должен вести к папке с локализацией (там где находятся папки english, russian, french и т.д.) Стандартный путь для Crusader Kings 3: \n../Steam/steamapps/common/Crusader Kings III/game/localization")
        cls.original_directory_help = _translate("Constants",
                                                 "Папка, где хранится локализация мода, на который вы хотите создать перевод. Пример: ../Steam/steamapps/workshop/content/1158310/2507209632/localization")
        cls.previous_directory_help = _translate("Constants",
                                                 "Если происходит обновление перевода и у вас уже есть готовый перевод предыдущей версии, то стоит указать директорию с предыдущей версией перевода.Программа сама пробежится\n"
                                                 "по старым файлам и использует строки, которые там найдет для построения новой версии. При этом все новые строки будут обработаны в обычном режиме и помечены комментарием #NT!")
        cls.target_directory_help = _translate("Constants",
                                               "Папка, в которую будут помещены все файлы, созданные в результате работы программы.\n"
                                               "(Точная копия оригинальной локализации по структуре папок и файлов, но с заменой данных о языке и с машинным переводом(если отмечен ниже).\n"
                                               "Пример: Если выбран english, как исходный язык, а russian, как целевой, все l_english будут заменены на l_russian, а машинный перевод будет на русский язык)")
        cls.need_translation_help = _translate("Constants", "При включении данной функции будет совершена попытка перевести все строки локализации на целевой язык, при этом перевод будет записан рядом с оригинальной строкой,\n"
                                                            "что подразумевает последующие правки текста, который может быть далек по смыслу от оригинала из-за неточности машинного перевода")
        cls.disable_original_line_help = _translate("Constants", "Отключает вывод оригинальной строки, оставляет только машинный перевод.\n"
                                                                 "Включать, только если вы отдаете себе отчет о последствиях!")
        cls.choice_supported_source_language_help = _translate("Constants", "Поддерживаемый игрой язык - выбор исходного языка, который поддерживается игрой. Здесь указывается название языка папок и файлов,\n"
                                                                            "в которых хранится оригинальная локализация, требующая перевода.\n"
                                                                            "Язык оригинала - выбор исходного языка текста. Здесь указывается язык, на котором написан текст в указанных файлах.\n"
                                                                            "Справка: Если игра не поддерживает, русский язык, то при переводе русский текст записывается в файлы для английской версии,\n"
                                                                            "поэтому в файлах типо *_l_english может находиться русская локализация")
        cls.choice_supported_target_language_help = _translate("Constants", "Поддерживаемый игрой язык - выбор целевого языка, который поддерживается игрой. Здесь указывается название языка папок и файлов,\n"
                                                                            "в которых хранится предыдущая версия локализации и в которые вы хотите поместить созданный перевод.\n"
                                                                            "Язык оригинала - выбор целевого языка, поддерживаемого игрой. Здесь указывается язык, на который вы хотите перевести текст.\n"
                                                                            "Справка: Если игра не поддерживает, какай-либо язык официально, то локализацию на этот язык можно запускать через английскую версию игры,\n"
                                                                            "если при этом в файлах с названием english лежит локализация нужного языка")

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
        cls.error_quota_exceeded = _translate("Constants", "Превышены ограничения вашего тарифа на перевод!")
        cls.api_service_changed = _translate("Constants", "Сервис перевода сменен на ")
        cls.thread_stopped = _translate("Constants", "Поток обработки остановлен")
        cls.localization_dict_creating_started = _translate("Constants", "Начато создание словаря игровой локализации")
        cls.game_localization_processing = _translate("Constants", "Обработка игровой локализации")
        cls.of_file = _translate("Constants", "файла")
        cls.previous_localization_dict_creating_started = _translate("Constants",
                                                                     "Начато создание словаря предыдущей локализации")
        cls.previous_localization_processing = _translate("Constants", "Обработка предыдущей локализации")
        cls.process_string = _translate("Constants", "Обработка строки")
        cls.final = _translate("Constants", "Обработка данных закончена")
        cls.final_time = _translate("Constants", "Программа закончила свою работу за")

        cls.error_settings_file_not_exist = _translate("Constants", "Место хранения настроек - не найдено")
        cls.error_folder_does_not_exist = _translate("Constants", "Директория не существует")
        cls.error_drive_not_exist = _translate("Constants", "Выбранный диск не существует")
        cls.error_path_not_exists = _translate("Constants", "Невозможно открыть")

        cls.warning_disable_original_line = _translate("Constants",
                                                       "Внимание!\nАвтор программы считает, что при включении данной функции сильно пострадает качество перевода. Включайте на свой страх и риск. После работы программы вы получите полностью машинный перевод с огромным количеством ошибок! Проверяйте перевод перед его публикацией где-либо!")
        cls.warning_disable_original_line_title = _translate("Constants", "Предупреждение")


class SettingsWindowConstants:

    protection_symbol_help = ''

    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate

        cls.protection_symbol_help = _translate("SettingsWindow", "Внимание!!! Не меняйте эту настройку, если не уверены в том, как это работает\n"
                                                             "Данный символ используется для подмены значений, которые по тем или иным причинам\n"
                                                             "могут быть испорчены переводчиком и не должны быть отправлены вместе с основным текстом")


class StatWindowConstants:
    open_file = ''
    open_statements_directory = ''

    used_service_apis = ''
    lines_in_file_len = ''
    new_lines = ''
    translated_lines = ''
    lines_from_vanilla = ''
    lines_from_previous_version = ''
    lines_with_errors = ''
    time_of_process = ''

    translated_files = ''
    translated_chars = ''

    name_column_param = ''
    name_column_value = ''
    save_csv_pushButton = ''
    open_statements_pushButton = ''
    close_pushButton = ''


    @classmethod
    def retranslate(cls):
        _translate = QtCore.QCoreApplication.translate
        cls.open_file = _translate("StatWindow", "Открыть файл")
        cls.open_statements_directory = _translate("StatWindow", "Открыть директорию с отчетами")
        cls.used_service_apis = _translate("StatWindow", "Использованные сервисы перевода")
        cls.lines_in_file_len = _translate("StatWindow", "Количество строк в файле")
        cls.new_lines = _translate("StatWindow", "Новые строки")
        cls.translated_lines = _translate("StatWindow", "Список переведенных строк")
        cls.lines_from_vanilla = _translate("StatWindow", "Список строк из ваниллы")
        cls.lines_from_previous_version = _translate("StatWindow", "Список строк из предыдущей версии перевода")
        cls.lines_with_errors = _translate("StatWindow", "Ошибки перевода в строках")
        cls.time_of_process = _translate("StatWindow", "Время выполнения")

        cls.translated_files = _translate("StatWindow", "Переведено файлов")
        cls.translated_chars = _translate("StatWindow", "Переведено символов")

        cls.name_column_param = _translate("StatWindow", "Показатель")
        cls.name_column_value = _translate("StatWindow", "Значение")
        cls.save_csv_pushButton = _translate("StatWindow", "Сохранить статистику в csv-файл")
        cls.open_statements_directory = _translate("StatWindow", "Открыть папку со статистикой")
        cls.close_pushButton = _translate("StatWindow", "Закрыть")


