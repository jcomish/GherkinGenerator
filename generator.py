import json
from allpairspy import AllPairs


class TestCaseGenerator:
    scenarios = []
    element_expands = []

    def __init__(self, tests_input_string):
        if TestCaseGenerator.__is_json(tests_input_string):
            self.__all_inputs = json.loads(tests_input_string)
        if self.__all_inputs is None:
            # raise error is input is not valid json
            raise InvalidInputException('Input is not a valid json format')
        self.elements = [WebElement(element) for element in self.__all_inputs]
        self.__num_elements = len(self.elements)

    def create_test_cases(self):
        self.__make_element_expands()
        for pair in AllPairs(self.element_expands):
            scenario = TestCase()
            scenario.add_expands(pair)
            self.scenarios.append(scenario)
        return self.scenarios

    def __make_element_expands(self):
        for i in range(self.__num_elements):
            self.element_expands.append(self.elements[i].expands)

    @staticmethod
    def __is_json(json_string):
        try:
            json.loads(json_string)
        except ValueError:
            return False
        return True


class WebElement:
    def __init__(self, root_dict):
        self.id = root_dict["id"]
        self.name = root_dict["name"]
        self.xpath = root_dict["xpath"]
        self.input_type = root_dict["inputType"]
        self.expands = [WebElement.ExpandObject(expand, self) for expand in root_dict["expand"]]
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

    def get_test_values(self):
        return list(map(lambda expand: expand.choice, self.selected_expands))


class InvalidInputException(Exception):
    def __init__(self, message):
        super().__init__(message)
