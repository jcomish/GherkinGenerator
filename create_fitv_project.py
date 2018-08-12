from generator import TestCaseGenerator
import json
import sys


json_file_path = sys.argv[1]
with open(json_file_path) as f:
    json_string = json.dumps(json.load(f))
print("Creating Fitv Project structure")
tests = TestCaseGenerator(json_string).create_test_cases()
print("Finished creating Fitv Project")
