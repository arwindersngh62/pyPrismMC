"""This module holds the code for prism file generation from a model of a layer"""

from pathlib import Path


class FileWriterMain:
    """Class responsible for creating a prism file for the given model"""

    def __init__(self, name, model=None):
        self.filename = name
        self.initBoolString = ": bool init false; \n"
        self.all_lines = []

    def writeMDP(self, data):
        layers = data.security_layers
        goals = data.goals

        self.all_lines.append("mdp \n \n \n")
        self.all_lines.append(f"module {self.filename.upper()} \n")
        for layer in layers:
            self.all_lines.append(f"{layer.name.upper()} {self.initBoolString}")
        self.all_lines.append(
            f"attackerBudget:[0..{data.attacker_budget}] init {data.attacker_budget};\n"
        )
        for goal in goals.values():
            print(goal.is_trivial)
            if goal.is_trivial:
                self.all_lines.append(
                    f"[Comp{goal.name.upper()}]  {goal.name.upper()}= false & attackerBudget>{int(goal.sec_layer_strength*100)} ->"
                )
                self.all_lines.append(
                    f"(1-{goal.sec_layer_strength}):(attackerBudget'=attackerBudget-{int(goal.sec_layer_strength*100)} & {goal.name.upper()}'= true) + "
                )
                self.all_lines.append(
                    f"({goal.sec_layer_strength}):(attackerBudget'=attackerBudget-{int(goal.sec_layer_strength*100)} & {goal.name.upper()}'= false); \n"
                )

        self.all_lines.append(
            f"endmodule \n \n system \n {self.filename.upper()} \n endsystem"
        )
        self.push_to_file()

    def push_to_file(self):
        file_path = Path(__file__).absolute().parent
        file = open(file_path / "generated_files" / "test.prism", "a+")
        for line in self.all_lines:
            file.writelines(line)

        # layers = data.sec_layers
        # file = open(f"{self.filename}.prism", "a+")
        # file.writelines("mdp \n \n \n")
        # file.writelines(f"module {self.filename.upper()} \n")
        # for layer in layers:
        #     file.writelines(f"{layer.name.upper()} {self.initBoolString}")
        # attacker_budget = f"attackerBudget:[0..{data.attacker_budget}] init {data.attacker_budget};\n"
        # file.writelines(attacker_budget)

        # file.writelines(f"endmodule \n \n system \n {self.filename.upper()} \n endsystem")
