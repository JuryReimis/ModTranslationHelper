import googletrans
import os


def get_previous_new_path() -> [str, str, bool]:
    was_previous = input("У вас есть предыдущая версия локализации? y/n ")
    match was_previous.lower():
        case "y":
            previous_translate_path = input("""Введите путь к previous: """)
            new_translate_path = input("""Введите путь к папке new: """)

        case "n":
            previous_translate_path = None
            new_translate_path = input("""Введите путь к папке new: """)
        case _:
            print("Ответ не разборчив, повторите попытку")
            return get_previous_new_path()
    need_translate = need_translation()
    return previous_translate_path, new_translate_path, need_translate


def need_translation():
    need_translate = input("""Добавить машинный перевод строк? Будет записан рядом с оригинальной в <> y/n """)
    match need_translate.lower():
        case "y":
            return True
        case _:
            print(f"Ответ отрицательный или не обработан, вы ввели: {need_translate}, перевод не будет выполнен")
            return False


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


def make_original_language_dictionary(original_language_lines: list) -> dict:
    original_language_dictionary = {}
    num_str = 0
    for line in original_language_lines:
        if line.lstrip() != "":
            key = line.split()[0]
            value = line.rstrip()
        else:
            key = "transfer"
            value = "\n"
        original_language_dictionary[num_str] = {"key": key, "value": value}
        num_str += 1
    return original_language_dictionary


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
    print(*googletrans.LANGUAGES.values(), sep="\n")
    target_language = input(f"Выберите язык из списка выше, на который будет производиться локализация ")

    previous_translate_path, new_translate_path, need_translate = get_previous_new_path()
    original_hierarchy = get_original_localization_hierarchy(original_path=original_language_path)
    make_new_language_hierarchy(new_translation_path=new_translate_path, original_hierarchy=original_hierarchy,
                                original_language=original_language, target_language=target_language)  # Создает иерархию папок, как в оригинальной директории, где потом можно создать объединенные файлы
    for step in original_hierarchy:
        full_original_path = os.path.join(original_language_path, step)
        full_new_path = os.path.join(new_translate_path, step.replace(original_language, target_language))
        if previous_translate_path is not None:
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
                    if line.lstrip() != "":
                        previous_translate_dictionary[line.split()[0]] = line

                original_language_dictionary = make_original_language_dictionary(
                    original_language_lines=original_language_lines)
                for key, values in original_language_dictionary.items():
                    if key == 0:
                        new_translate_list[0] = previous_translate_dictionary["lang"]
                    else:
                        response = previous_translate_dictionary.get(values["key"], None)
                        if response is None and values["key"] != "transfer":
                            new_translate_list[key] = values["value"] + " #NT!\n"
                        elif values["key"] == "transfer":
                            new_translate_list[key] = values["value"]
                        else:
                            new_translate_list[key] = previous_translate_dictionary[values["key"]]
                print(*new_translate_list, end="", sep="", file=new_translate_file)
        else:
            with open(file=full_original_path, mode="r", encoding="utf-8-sig") as original_language_file, \
                    open(file=full_new_path, mode="w", encoding="utf-8-sig") as new_translate_file:
                original_language_lines = original_language_file.readlines()
                original_language_dictionary = make_original_language_dictionary(
                    original_language_lines=original_language_lines)
                new_translate_list = ["" for _ in range(len(original_language_lines))]
                for key, values in original_language_dictionary.items():
                    if key == 0:
                        new_translate_list[0] = "l_" + target_language + ":\n"
                    else:
                        if values["value"].rstrip() == "":
                            new_translate_list[key] = values["value"]
                        else:
                            new_translate_list[key] = values["value"] + " #NT!\n"
                print(*new_translate_list, sep="", end="", file=new_translate_file)


if __name__ == "__main__":
    main()
