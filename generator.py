import json
from allpairspy import AllPairs
from AutomationGenerator import AutomationGenerator
from Scenario import Scenario
from Step import Step


class TestCaseGenerator:
    cases = []
    element_expands = []
    raw_test = AutomationGenerator(tags="@test")

    def __init__(self, tests_input_string):
        self.__all_inputs = None
        if TestCaseGenerator.__is_json(tests_input_string):
            self.__all_inputs = json.loads(tests_input_string)
        if self.__all_inputs is None:
            # raise error is input is not valid json
            raise InvalidInputException('Input is not a valid json format')
        self.elements = [WebElement(element) for element in self.__all_inputs[0]['testinputs']]
        self.feature_name = self.__all_inputs[0]['feature_settings'][0]['feature_name']
        self.url = self.__all_inputs[0]['feature_settings'][0]['start_loc']
        self.__num_elements = len(self.elements)

    def create_test_cases(self):
        self.__make_element_expands()
        for pair in AllPairs(self.element_expands):
            case = TestCase()
            case.add_expands(pair)
            self.cases.append(case)
        self.__update_raw_tests()
        self.raw_test.generate_fitv_project()
        return self.raw_test

    def __make_element_expands(self):
        for i in range(self.__num_elements):
            self.element_expands.append(self.elements[i].expands)

    def __update_raw_tests(self):
        self.raw_test.scenarios.append(Scenario(url=self.url, feature_name=self.feature_name, text="Example test scenario"))
        for choice in self.cases[0].selected_expands:
            self.raw_test.scenarios[0].steps.append(
                Step(step_type=choice.parent.step_type, feature_name=self.feature_name, x_path=choice.parent.xpath,
                     input_type=choice.parent.input_type, cases=[],
                     label="Element " + choice.parent.name + " has value <choice{}>".format(choice.parent.id)))

        for case in self.cases:
            for i, choice in enumerate(case.selected_expands):
                self.raw_test.scenarios[0].steps[i].cases.append(choice.choice)

    @staticmethod
    def __is_json(json_string):
        try:
            json.loads(json_string)
        except ValueError:
            return False
        return True


class WebElement:
    def __init__(self, root_dict):
        self.id = root_dict["order"]
        self.name = root_dict["name"]
        self.xpath = root_dict["xpath"]
        self.input_type = root_dict["inputType"]
        self.expands = [WebElement.ExpandObject(expand, self) for expand in root_dict["expand"]]
        if 'step_type' in root_dict.keys():
            self.step_type = root_dict["step_type"]
        else:
            self.step_type = "Given"
        # when the element only has one choice the allpairspy library does not like that so this adds another
        # identical choice if there's only one
        if len(self.expands) == 1:
            self.expands += self.expands
        self.num_test_cases = len(self.expands)
        self.selected_expands = set()

    class ExpandObject:
        def __init__(self, expand_dict, element):
            self.id = expand_dict["id"]
            self.choice = expand_dict["choice"]
            self.parent = element


class TestCase:
    def __init__(self):
        self.selected_expands = []

    def add_expands(self, expands):
        self.selected_expands += expands
        self.__sort_expands()

    def __sort_expands(self):
        self.selected_expands.sort(key=lambda expand: expand.parent.id)

    def get_test_values(self):
        return list(map(lambda expand: expand.choice, self.selected_expands))


class InvalidInputException(Exception):
    def __init__(self, message):
        super().__init__(message)
