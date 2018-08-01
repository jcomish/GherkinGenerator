
class GherkinPage:
    tags = ""
    feature_name = ""
    feature_as = ""
    feature_action = ""
    feature_outcome = ""

    string_repr = ""

    scenarios = []

    def __str__(self):
        return self.string_repr

    def compile_gherkin(self):
        self.string_repr += self.tags
        if (self.feature_outcome != "" and self.feature_as != ""
                and self.feature_name != "" and self.feature_action != ""):
            self.string_repr = "Scenario Outline: " + self.feature_name + "\n" +\
                   self.feature_as + "\n" +\
                   self.feature_action + "\n" +\
                   self.feature_outcome + "\n"

        for scenario in self.scenarios:
            self.string_repr += str(scenario)

        for scenario in self.scenarios:
            self.string_repr += scenario.get_cases()
        return self.prettify_gherkin()

    @staticmethod
    def find_examples_table(lines):
        for i in range(0, len(lines)):
            if "Examples:" in lines[i]:
                return i + 1

    def prettify_gherkin(self):
        lines = self.string_repr.split('\n')
        col_widths = [0 for i in range(self.find_examples_table(lines), (len(lines) - 1))]

        for i in range(self.find_examples_table(lines), len(lines) - 1):
            cols = lines[i].split('|')
            del cols[0]
            del cols[-1]
            for j in range(0, len(cols)):
                if len(cols[j]) > col_widths[j]:
                    col_widths[j] = len(cols[j])

        for i in range(self.find_examples_table(lines), len(lines) - 1):
            cols = lines[i].split('|')
            del cols[0]
            del cols[-1]
            for j in range(0, len(cols)):
                cols[j] += " " * (col_widths[j] - len(cols[j]))
            lines[i] = "    |" + "|".join(cols) + "|"

        self.string_repr = "\n".join(lines)




