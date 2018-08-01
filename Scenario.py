class Scenario:
    scenario_text = ""
    steps = []

    def __init__(self, text="", steps=[]):
        self.steps = []
        self.scenario_text = text
        self.steps = steps

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
            text += step.get_keyword()
            text += " | "
        text += "\n"

        for i in range(0, len(self.steps[0].cases)):
            text += "    | "
            for step in self.steps:
                text += str(step.cases[i])
                text += " | "
            text += "\n"

        return text

