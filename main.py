import googletrans


def get_previous_new_path() -> [str, str, bool]:
    was_previous = input("У вас есть предыдущая версия локализации? y/n ")
    match was_previous.lower():
        case "y":
            previous_translate_path = input("""Введите путь к previous: """)
            new_translate_path = input("""Введите путь к папке new: """)

        case "n":
            previous_translate_path = new_translate_path = input("""Введите путь к папке new: """)
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
    default_language_path = input("Введите путь к папке original. Должна заканчиваться на /localization ")
    print(*googletrans.LANGUAGES.values(), sep="\n")
    translate_localization = input(f"Выберите язык из списка выше, на который будет производиться локализация ")
    previous_translate_path, new_translate_path, need_translate = get_previous_new_path()
    with open(file=previous_translate_path, mode="r",
              encoding="utf-8-sig") as previous_translate, \
            open(file=default_language_path, mode="r",
                 encoding="utf-8-sig") as default_language, \
            open(file=new_translate_path, mode="w", encoding="utf-8-sig") as new_translate:
        default_language_dictionary = {}
        default_language_lines = default_language.readlines()

        new_translate_list = ["" for _ in range(len(default_language_lines))]
        previous_translate_dictionary = {"lang": previous_translate.readline()}
        previous_translate_lines = previous_translate.readlines()

        for line in previous_translate_lines:
            if line.lstrip() != "":
                previous_translate_dictionary[line.split()[0]] = line

        num_str = 0
        for line in default_language_lines:
            if line.lstrip() != "":
                key = line.split()[0]
                value = line.lstrip()
            else:
                key = "transfer"
                value = "\n"
            default_language_dictionary[num_str] = {"key": key, "value": value}
            num_str += 1
        for key, values in default_language_dictionary.items():
            if key == 0:
                new_translate_list[0] = previous_translate_dictionary["lang"]
            else:
                response = previous_translate_dictionary.get(values["key"], None)
                if response is None and values["key"] != "transfer":
                    new_translate_list[key] = "#NT! " + values["value"]
                elif values["key"] == "transfer":
                    new_translate_list[key] = values["value"]
                else:
                    new_translate_list[key] = previous_translate_dictionary[values["key"]]
        print(*new_translate_list, end="", sep="", file=new_translate)


if __name__ == "__main__":
    main()
