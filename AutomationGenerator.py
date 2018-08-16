import os
from pathlib import Path

class AutomationGenerator:
    outputLocation = Path();
    tags = ""
    feature_name = ""
    feature_as = ""
    feature_action = ""
    feature_outcome = ""

    string_repr = ""

    scenarios = []

    def __init__(self, feature_as="", feature_action="", feature_outcome="", tags=tags):
        self.feature_as = feature_as
        self.feature_outcome = feature_outcome
        self.feature_action = feature_action
        self.tags = tags

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

    def create_project_structure(self):
        (self.outputLocation / "PageObjects").mkdir(parents=True, exist_ok=True)
        (self.outputLocation / "steps").mkdir(parents=True, exist_ok=True)
        (self.outputLocation / "features").mkdir(parents=True, exist_ok=True)

    def write_static_files(self):
        environment_file = (self.outputLocation / "environment.py")
        settings_file = (self.outputLocation / "settings.py")
        if not environment_file.exists():
            with Path("./Templates/environment.py").open("r", encoding="utf-8") as r:
                fileOutput = r.read()
            with environment_file.open("w", encoding="utf-8") as f:
                f.write(fileOutput)

        if not settings_file.exists():
            with Path("./Templates/Settings.py").open("r", encoding="utf-8") as r:
                fileOutput = r.read()
            with settings_file.open("w", encoding="utf-8") as f:
                f.write(fileOutput)


    def write_step_file(self, overwrite=True):
        file_path = self.outputLocation / "features" / (self.scenarios[0].feature_name + ".feature")

        if overwrite:
            with file_path.open("w", encoding="utf-8") as f:
                f.write(str(self))
        else:
            if not file_path.exists():
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(str(self))



    def generate_fitv_project(self, rootDirectoryName="./FitvProject"):
        self.outputLocation /= rootDirectoryName
        self.create_project_structure()
        self.write_static_files()
        self.compile_gherkin()
        self.write_step_file()

        for scenario in self.scenarios:
            scenario.write_page_object(Path(self.outputLocation / "PageObjects" / (scenario.feature_name + "PO.py")))

        for scenario in self.scenarios:
            scenario.write_steps(Path(self.outputLocation / "steps" / (scenario.feature_name + ".py")))


