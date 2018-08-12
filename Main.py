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

json_dict = [
    {
        "feature_settings":[
            {
                "feature_name":"tet",
                "start_loc":"test"
            }
        ],
        "testinputs":[
            {
                "order":0,
                "name":"name0",
                "xpath":"path 0",
                "inputType":'button',
                "expand":[
                    {
                        "id":1,
                        "choice":"test1"
                    },
                    {
                        "id":2,
                        "choice":"test2"
                    }
                ],
                "step_type":"Given"
            },
            {
                "order":1,
                "name":"name1",
                "xpath":"path 1",
                "inputType":'text',
                "expand":[
                    {
                        "id":1,
                        "choice":"test1"
                    },
                    {
                        "id":2,
                        "choice":"test2"
                    }
                ]
            },
            {
                "order":2,
                "name":"name2",
                "xpath":"path 2",
                "inputType":'textarea',
                "expand":[
                    {
                        "id":1,
                        "choice":"test1"
                    },
                    {
                        "id":2,
                        "choice":"test2"
                    }
                ]
            },
            {
                "order":3,
                "name":"name3",
                "xpath":"path 3",
                "inputType":'select',
                "expand":[
                    {
                        "id":1,
                        "choice":"test1"
                    },
                    {
                        "id":2,
                        "choice":"test2"
                    }
                ]
            },
            {
                "order":4,
                "name":"name4",
                "xpath":"path 4",
                "inputType":'text',
                "expand":[
                    {
                        "id":1,
                        "choice":"test1"
                    },
                    {
                        "id":2,
                        "choice":"test2"
                    }
                ]
            }
        ]
    }
]


json_in = []
input_size = 5
for i in range(1, input_size + 1):
    json_in.append(x(i))

json_in = json.dumps(json_dict)

generator = TestCaseGenerator(json_in)
scenarios = generator.create_test_cases()
# print(json.loads(json_in)[0]['testinputs'])
