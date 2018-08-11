import sys
from generator import TestCaseGenerator

json_string = sys.argv[1]
print("Creating Fitv Project structure")
tests = TestCaseGenerator(json_string).create_test_cases()
print("Finished creating Fitv Project")
