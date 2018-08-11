import re


class Step:
    type = ""
    label = ""
    cases = []

    def __init__(self, type="", label="", cases=[]):
        self.type = type
        self.label = label
        self.cases = cases

    def __str__(self):
        return "  " + self.type + " " + self.label + "\n"

    def get_keyword(self):
        regex = re.search(r'(?<=<)[^>]*(?=>)', self.label, re.I)
        return regex.group()
