from config import default_language_path, previous_translate_path

with open(file=default_language_path, mode="r",
          encoding="utf-8-sig") as new_language, \
        open(file=previous_translate_path, mode="r",
             encoding="utf-8-sig") as default_language:

    default_language_dictionary = {}
    default_language_lines = default_language.readlines()

    new_language_list = ["" for _ in range(len(default_language_lines))]
    new_language_dictionary = {"lang": new_language.readline()}
    new_language_lines = new_language.readlines()

    for line in new_language_lines:
        ls = line.lstrip()
        if line.lstrip() != "":
            new_language_dictionary[line.split()[0]] = line

    num_str = 0
    for line in default_language_lines:
        if line.replace(" ", "") != "\n":
            key = line.split()[0]
            value = line.lstrip()
        else:
            key = "transfer"
            value = "\n"
        default_language_dictionary[num_str] = {"key": key, "value": value}
        num_str += 1
    for key, values in default_language_dictionary.items():
        if key == 0:
            new_language_list[0] = new_language_dictionary["lang"]
        else:
            response = new_language_dictionary.get(values["key"], None)
            if response is None:
                new_language_list[key] = values["value"]
            else:
                new_language_list[key] = new_language_dictionary[values["key"]]
