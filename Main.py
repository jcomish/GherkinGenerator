# from GherkinPage import GherkinPage
# from Scenario import Scenario
# from Step import Step
# import json
# import jsonpickle
#
# def getJSON():
#     raw_test = GherkinPage()
#
#     raw_test.tags = "@test"
#     raw_test.scenarios.append(Scenario(text="I eat cucumbers"))
#     raw_test.scenarios[0].steps.append(Step(type="Given", label="I have <start> cucumbers", cases=[10, 7, 12]))
#     raw_test.scenarios[0].steps.append(Step(type="When", label="I eat <eat> cucumbers", cases=[5, 5, 5]))
#     raw_test.scenarios[0].steps.append(Step(type="Then", label="I have <end> cucumbers", cases=[5, 2, 7]))
#
#     raw_test.compile_gherkin()
#
#     return jsonpickle.encode(raw_test)
#
# def formAutomation(test_data):
#     test = jsonpickle.decode(test_data)
#     print(str(test))
#
# if __name__ == "__main__":
#     formAutomation(getJSON())
from generator import TestCaseGenerator

import json


def x(i):
    expands = []
    # num_expands = max(i, (7-3))
    num_expands = i
    for x in range(0, num_expands):
        choices = x
        expands.append(expand(choices))
    return {
        "id":i,
        "name":"name" + str(i),
        "xpath":"path " + str(i),
        "inputType":"text",
        "expand":expands
    }


def expand(i):
    return {
        "id":i,
        "choice":"t" + str(i)
    }


json_in = []
input_size = 5
for i in range(1, input_size + 1):
    json_in.append(x(i))

json_in = json.dumps(json_in)

generator = TestCaseGenerator(json_in)
scenarios = generator.create_test_cases()
print(str(scenarios))
# print(json_in)
