import re
from FitvMethodMap import FITV_METHOD_MAP

class Step:
    feature_name = ""
    step_type = ""
    label = ""
    keyword = ""
    input_type = ""
    x_path = ""
    cases = []

    def __init__(self, feature_name, step_type, label, cases, x_path=None, input_type=None):
        self.feature_name = feature_name
        self.step_type = step_type
        self.label = label
        self.cases = cases
        self.keyword = self.get_keyword()
        self.input_type = input_type
        self.x_path = x_path

    def __str__(self):
        return "  " + self.step_type + " " + self.label + "\n"

    def get_keyword(self):
        regex = re.search(r'(?<=<).*(?=>)', self.label, re.I)
        if regex:
            return regex.group()
        else:
            raise ValueError("Label MUST contain a keyword ex:(\"<example>\"")

    def write_page_object_locator(self, path):
        output_string = ("    " + self.input_type.upper() + "_" + self.keyword.upper() + " = " )
        if self.x_path:
            output_string += ("\"" + self.x_path + "\"")
        else:
            output_string += ("\"*\"")

        return output_string + "\n"

    def write_page_object_method(self, path):
        output_string = "    def interact_" + self.keyword + "(self, " + self.keyword + "):\n" + \
                          "        " + FITV_METHOD_MAP[self.input_type][2] + "." + FITV_METHOD_MAP[self.input_type][0] + \
                            "(self." + self.input_type.upper() + "_" + self.keyword.upper() + \
                          ", " + self.keyword
        # TODO: Expand prev line to support multiple args
        if self.keyword == "select" or self.keyword == "mselect":
            output_string += ".split(',')"

        output_string += ")\n"

        return output_string



    def write_step(self, path):
        tempLabel = self.label.replace('<', '{')
        tempLabel = tempLabel.replace('>', '}')
        output_string = ("@" + self.step_type + "('" + tempLabel + "')\n" +
                          "def step_impl(" + "context, " + self.keyword + "):\n" +
                          "\tinteract_" + self.keyword + "(" + self.keyword + ")\n"
                          )

        return output_string