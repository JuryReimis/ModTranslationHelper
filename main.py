from config import default_language_path, new_language_path

with open(file=default_language_path, mode="r",
          encoding="utf-8-sig") as new_language, \
        open(file=new_language_path, mode="r",
             encoding="utf-8-sig") as default_language:
    default_language_dictionary = {}
    num_str = 0
    for line in default_language.readlines():
        if line != "\n":
            key = line.split()[0]
            value = line
        else:
            key = "transfer"
            value = "\n"
        default_language_dictionary[num_str] = {"key": key, "value": value}
        num_str += 1
