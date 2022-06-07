import re
import os
import sys
import time
from deep_translator import GoogleTranslator


def get_previous_new_path(original_language: str, target_language: str) -> [str, str, bool]:
    was_previous = input("У вас есть предыдущая версия локализации? y/n ")
    match was_previous.lower():
        case "y":
            previous_translate_path = input("""Введите путь к previous: """)
            new_translate_path = input("""Введите путь к папке new: """)
        case "n":
            previous_translate_path = None
            new_translate_path = input("""Введите путь к папке new: """)
        case _:
            print("Ответ не распознан, повторите попытку")
            return get_previous_new_path(original_language=original_language, target_language=target_language)
    need_translate = need_translation(original_language=original_language, target_language=target_language)
    return previous_translate_path, new_translate_path, need_translate


def need_translation(original_language: str, target_language: str):
    need_translate = input("""Добавить машинный перевод строк? Будет записан рядом с оригинальной в <> y/n """)
    match need_translate.lower():
        case "y":
            return GoogleTranslator(source=original_language, target=target_language)
        case _:
            print(f"Ответ отрицательный или не обработан, вы ввели: {need_translate}, перевод не будет выполнен")
            return None


def get_original_localization_hierarchy(original_path: str) -> list:
    hierarchy = []
    for step in os.walk(original_path):
        language_path_divided = os.path.relpath(step[0], start=original_path)
        for name in step[2]:
            hierarchy.append(os.path.join(language_path_divided, name))
    return hierarchy


def make_new_language_hierarchy(new_translation_path, target_language, original_language, original_hierarchy):
    for file in original_hierarchy:
        target_file = file.replace(original_language, target_language)
        target_path = os.path.dirname(os.path.join(new_translation_path, target_file))
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            print(f"Создана директория {target_path}")


def make_language_dictionary(original_language_lines: list) -> dict:
    r"""Создает и возвращает словарь, состоящий из позиции, в качестве ключа и словаря, в качестве значения
    Каждый словарь содержит пару ключей-значений: key: 'key', value: 'value'
    К применру: 11: {'key': 'AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0',
                    'value': ' AI_UNIT_TOOLTIP_UNIT_STACK_NO_ORDER:0 " No order."'},
    Здесь 11 - номер строки, а key - ключ(идентификатор) полной строки value"""
    original_language_dictionary = {}
    num_str = 0
    for line in original_language_lines:
        separated_line = re.findall(pattern=r"(.*:)(.*) (\".*\")", string=line)
        if separated_line:
            key = separated_line[0][0]
        else:
            key = "not_program_data"
        value = line
        original_language_dictionary[num_str] = {"key": key, "value": value}
        num_str += 1
    return original_language_dictionary


def translate_line(translator: GoogleTranslator | None, line: str) -> str:
    line = line.rstrip()
    if translator is None:
        return line + " #NT!\n"
    else:
        only_text = re.findall(pattern=r"\".+\"", string=line)
        if not only_text:
            try:
                not_content_string = translator.translate(text=line)
                return not_content_string + "\n"
            except Exception as e:
                print("Произошла ошибка с переводом строки:\n", line, "\n", e)
                return line + " #Translation Error" + "\n"
        else:
            if only_text[0][1:-1].isdigit():
                return line + " #NT!\n"
            try:
                modified_text, values_dict = modify_text(line=only_text[0], pattern=r"\[.*?\]", flag="modify")
                if modified_text is None and values_dict is None:
                    return line + "#NT!\n"
                translated = translator.translate(text=modified_text[1:-1])
                normal_string = modify_text(line=translated, pattern=None, flag="return_normal_view",
                                            values_dict=values_dict)
                return line + f" <\"{normal_string}\">" + " #NT!\n"
            except Exception as e:
                print("Произошла ошибка с переводом строки:\n", line, "\n", e)
                return line + " #Translation Error!" + "\n"


def modify_text(line: str, pattern: str | None, flag: str, values_dict: None | dict = None) -> (str, dict) or str:
    r"""При флаге "modify" позволяет заменить некоторые части строки по шаблону на скрытую, ничего не обозначающую
    переменную. При флаге "return_normal_view" позволяет вернуть нормальный вид строки по словарю параметров"""
    match flag:
        case "modify":
            values_dict = {}
            shadow_number = 0
            regular_groups = re.findall(pattern=pattern, string=line)
            for step in regular_groups:
                values_dict[f"[{shadow_number}]"] = step
                line = line.replace(step, f"[{shadow_number}]")
                shadow_number += 1
            return line, values_dict
        case "return_normal_view":
            values_dict: dict
            for key, value in values_dict.items():
                line = line.replace(key, value)
            return line
        case _:
            print("Ошибка при модификации, флаг нечитаем")
            sys.exit()


def get_game_languages_path(game_path: str, original_language: str, target_language: str) -> [str, str]:
    game_path_original_language = os.path.join(game_path, "localization", original_language)
    game_path_target_language = os.path.join(game_path, "localization", target_language)
    return game_path_original_language, game_path_target_language


def get_game_original_language_dictionary(path_to_original: str, path_to_target) -> [dict, dict]:
    game_original_dictionary, game_target_dictionary = {}, {}
    if os.path.exists(path_to_original) is True and os.path.exists(path_to_target) is True:
        with open(file=path_to_original, mode="r", encoding="utf-8-sig") as game_original_language_file, \
                open(file=path_to_target, mode="r", encoding="utf-8-sig") as game_target_language_file:
            for line in game_original_language_file.readlines():
                separated_line = re.findall(pattern=r"(.*:)(.*) (\".*\")", string=line)
                if separated_line:
                    game_original_dictionary[separated_line[0][0].lstrip()] = line.rstrip()
            for line in game_target_language_file.readlines():
                separated_line = re.findall(pattern=r"(.*:)(.*) (\".*\")", string=line)
                if separated_line:
                    game_target_dictionary[separated_line[0][0].lstrip()] = line.rstrip()
    return game_original_dictionary, game_target_dictionary


def main():
    print("""Приветствую! Эта программа поможет вам справиться с локализацией многих модов.
    Основной проблемой при локализации является поиск новых строчек для перевода, автор может добавить новые события
    посреди огромного списка, и поиск этих новых строчек занимает больше времени, чем сам перевод.
    Это программа написана для облегчения поиска новых строчек. Сейчас коротко опишу принцип работы.
    В результате выполнения вы получите идентичную оригинальной иерархию файлов с локализацие, в которой будут помечены
    непереведенные строчки, а переведенные сохранены.
    Чтобы запустить программу вам нужно знать некоторую информацию:
        Из какой папки программа должна взять оригинальную локализацию - original
        Из какой папки программа должнавзять предыдущую версию перевода - previous
        В какую папку программа поместит объединенные файлы(имеющие перевод и новые оригинальные) - new""")
    original_language_path = input("Введите путь к папке original. Должна заканчиваться на /localization/[language] ")
    original_language = os.path.basename(original_language_path)
    game_path = input(r"Введите путь к папке игры, например: D:\Steam\steamapps\common\Crusader Kings III\game ")
    all_languages = GoogleTranslator.get_supported_languages()
    print(*all_languages, sep="\n")
    target_language = input(f"Выберите язык из списка выше, на который будет производиться локализация ")

    if target_language not in all_languages:
        print(f"Язык {target_language} не поддерживается")
        sys.exit()

    previous_translate_path, new_translate_path, need_translate = get_previous_new_path(
        original_language=original_language, target_language=target_language)
    game_path_original_language, game_path_target_language = get_game_languages_path(game_path=game_path,
                                                                                     original_language=original_language,
                                                                                     target_language=target_language)
    original_hierarchy = get_original_localization_hierarchy(original_path=original_language_path)
    make_new_language_hierarchy(new_translation_path=new_translate_path, original_hierarchy=original_hierarchy,
                                original_language=original_language,
                                target_language=target_language)  # Создает иерархию папок, как в оригинальной директории, где потом можно создать объединенные файлы
    start_time = time.time()
    for step in original_hierarchy:
        game_path_original_language_full = os.path.join(game_path_original_language, step)
        game_path_target_language_full = os.path.join(game_path_target_language,
                                                      step.replace(original_language, target_language))
        game_original_language_dictionary, game_target_language_dictionary = get_game_original_language_dictionary(
            path_to_original=game_path_original_language_full, path_to_target=game_path_target_language_full)
        full_original_path = os.path.join(original_language_path, step)
        full_new_path = os.path.join(new_translate_path, step.replace(original_language, target_language))
        if previous_translate_path is not None and os.path.isfile(os.path.join(previous_translate_path, step.replace(original_language, target_language))):
            full_previous_path = os.path.join(previous_translate_path, step.replace(original_language, target_language))
            with open(file=full_previous_path, mode="r",
                      encoding="utf-8-sig") as previous_translate_file, \
                    open(file=full_original_path, mode="r",
                         encoding="utf-8-sig") as original_language_file, \
                    open(file=full_new_path, mode="w", encoding="utf-8-sig") as new_translate_file:

                original_language_lines = original_language_file.readlines()
                new_translate_list = ["" for _ in range(len(original_language_lines))]
                previous_translate_dictionary = {"lang": "l_" + target_language + ":\n"}
                previous_translate_file.readline()
                previous_translate_lines = previous_translate_file.readlines()
                for line in previous_translate_lines:
                    separated_line = re.findall(pattern=r"(.*:)(.*) (\".*\")", string=line)
                    if separated_line:
                        previous_translate_dictionary[separated_line[0][0]] = line

                original_language_dictionary = make_language_dictionary(
                    original_language_lines=original_language_lines)
                amount_lines = len(original_language_dictionary)
                for key, values in original_language_dictionary.items():
                    print(f"Обработка строки №{key}/{amount_lines}",
                          f"файла {os.path.basename(full_original_path)}")
                    values: dict
                    if key == 0:
                        new_translate_list[0] = previous_translate_dictionary["lang"]
                    else:
                        flag = False
                        value = game_original_language_dictionary.get(values["key"], None)
                        if value is not None:
                            if value == values["value"]:
                                new_translate_list[key] = game_target_language_dictionary.get(values["key"]) + "\n"
                                flag = True
                        if flag is False:
                            response = previous_translate_dictionary.get(values["key"], None)
                            if response is None and values["key"] != "not_program_data":
                                new_translate_list[key] = " ".join((values["key"], translate_line(translator=need_translate,
                                                                         line=values["value"])))
                            elif values["key"] == "not_program_data":
                                new_translate_list[key] = values["value"]
                            else:
                                new_translate_list[key] = previous_translate_dictionary[values["key"]]
                print(*new_translate_list, end="", sep="", file=new_translate_file)
        else:
            with open(file=full_original_path, mode="r", encoding="utf-8-sig") as original_language_file, \
                    open(file=full_new_path, mode="w", encoding="utf-8-sig") as new_translate_file:
                original_language_lines = original_language_file.readlines()
                original_language_dictionary = make_language_dictionary(
                    original_language_lines=original_language_lines)
                new_translate_list = ["" for _ in range(len(original_language_lines))]
                amount_lines = len(original_language_dictionary)
                for key, values in original_language_dictionary.items():
                    print(f"Обработка строки №{key + 1}/{amount_lines}",
                          f"файла {os.path.basename(full_original_path)}")
                    if key == 0:
                        new_translate_list[0] = "l_" + target_language + ":\n"
                    else:
                        flag = False
                        value = game_original_language_dictionary.get(values["key"], None)
                        target_value = game_target_language_dictionary.get(values["key"], None)
                        if value is not None and target_value is not None:
                            if value == values["value"]:
                                new_translate_list[key] = target_value + "\n"
                                flag = True
                        if flag is False:
                            if values["value"].rstrip() == "":
                                new_translate_list[key] = values["value"]
                            else:
                                new_translate_list[key] = translate_line(translator=need_translate,
                                                                         line=values["value"])
                print(*new_translate_list, sep="", end="", file=new_translate_file)
    print("Завершено за: ", time.strftime("%H:%M:%S", (time.gmtime(time.time() - start_time))))


if __name__ == "__main__":
    main()
