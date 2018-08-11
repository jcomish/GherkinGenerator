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
# print(json_in)
