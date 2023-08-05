import re


class Util:

    @staticmethod
    def remove_non_digits(string):
        return re.sub('\\D', '', string)
