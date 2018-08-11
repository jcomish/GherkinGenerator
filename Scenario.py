from FitvMethodMap import FITV_METHOD_MAP

class Scenario:
    feature_name = ""
    url = ""
    scenario_text = ""
    steps = []

    def __init__(self, feature_name, url, text="", steps=[]):
        self.steps = []
        self.scenario_text = text
        self.steps = steps
        self.url = url
        self.feature_name = feature_name

    def __str__(self):
        scenario = "\n" + "Scenario Outline: " + self. scenario_text + "\n"
        for step in self.steps:
            scenario += str(step)
        return scenario

    def get_cases(self):
        text = "\n  Examples:\n"
        # Headers
        text += "    | "
        for step in self.steps:
            text += step.keyword
            text += " | "
        text += "\n"

        for i in range(0, len(self.steps[0].cases)):
            text += "    | "
            for step in self.steps:
                text += str(step.cases[i])
                text += " | "
            text += "\n"

        return text

    def import_method_string(self, module):
        return "from Fitv.FitActions." + module + " import " + module

    def write_page_object(self, path):
        modules = set([])
        for step in self.steps:
            modules.add(FITV_METHOD_MAP[step.input_type][2])
        output_string = ("from Fitv.FitPage import FitPage\n" +
                          "\n".join([self.import_method_string(module) for module in modules]) +
                          "\n\n\nclass " + self.feature_name + "(FitPage):\n" +
                          "    Url = \"" + self.url + " \"\n\n")

        output_string += ("".join([step.write_page_object_locator(path) for step in self.steps]) + "\n")
        output_string += ("\n".join([step.write_page_object_method(path) for step in self.steps]))

        p = open(path, 'w')
        p.write(output_string)


    def write_steps(self, path):
        modules = set([])
        for step in self.steps:
            modules.add(FITV_METHOD_MAP[step.input_type][2])
        output_string = ("from behave import *\n" +
                         "from .PageObjects." + self.feature_name + "PO import *\n\n\n"
                        )

        for step in self.steps:
            output_string += step.write_step(path) + "\n"


        p = open(path, 'w')
        p.write(output_string)