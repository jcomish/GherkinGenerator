from GherkinPage import GherkinPage
from Scenario import Scenario
from Step import Step
import jsonpickle

def getJSON():
    raw_test = GherkinPage()

    raw_test.tags = "@test"
    raw_test.scenarios.append(Scenario(text="I eat cucumbers"))
    raw_test.scenarios[0].steps.append(Step(type="Given", label="I have <start> cucumbers", cases=[10, 7, 12]))
    raw_test.scenarios[0].steps.append(Step(type="When", label="I eat <eat> cucumbers", cases=[5, 5, 5]))
    raw_test.scenarios[0].steps.append(Step(type="Then", label="I have <end> cucumbers", cases=[5, 2, 7]))

    raw_test.compile_gherkin()

    return jsonpickle.encode(raw_test)

def formAutomation(test_data):
    test = jsonpickle.decode(test_data)
    print(str(test))

if __name__ == "__main__":
    formAutomation(getJSON())