from config import default_language_path, previous_translate_path, new_translate_path

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
