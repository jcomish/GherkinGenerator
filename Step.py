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
        i = 0
        j = 0
        for i in range(0, len(self.label)):
            if self.label[i] == "<":
                for j in range(i, len(self.label)):
                    if self.label[j] == ">":
                        break
                break
        return self.label[i + 1:j]