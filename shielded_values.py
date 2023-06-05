

class ShieldedValues:
    wrapped = [
        r"\[.*?\]",
        r"§\S*?§",
        r"§\S+?",
        r"\$\S*?\$",
        r"£\S*?£",
        r"£\S*[^\"]",
        r"#\S*[^\"|^ ]",
    ]

    @classmethod
    def get_common_pattern(cls):
        return '|'.join(cls.wrapped)
