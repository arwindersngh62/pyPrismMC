import fileWriter
from typing import Tuple


class PerceptionLayerModel:
    def __init__(self):
        self.secerts = []
        self.security_layers = {}
        self.goals = {}
        # self.file_writer = fileWriter.FileWriterMain("Phyicallayer")
        self.attacker_budget = 100

    def build_trivial_goals(self):
        print("----Building trivial goals-------")
        for layer in self.security_layers:
            self.add_trivial_goal(layer.name, layer.strength)

    def add_all_layers(self, layers):
        self.security_layers = layers

    def create_mdp(self):
        """create an MDP of the given model"""
        self.file_writer.writeMDP(self)

    def compare_coonfigs(self, config2, goal):
        """Compare two configs for one or more goals"""
        pass

    def _build_model(self):
        """build a prism model"""
        pass

    def add_secrets_to_layers(self, layer_name, secrets):
        self.security_layers[layer_name].add_secrets(secrets)
        self.secrets += secrets

    def add_trivial_goal(self, goal_name, strength):
        goal = Goal(goal_name)
        goal.sec_layer_strength = strength
        self.goals[f"SG_{goal_name}"] = goal

    def add_complex_goal(self, goal_name, mapping, is_mapping_to_layers=False):
        # TODO: check keys exist
        goal_mapping = []
        if is_mapping_to_layers:
            for layer_name in mapping:
                goal_mapping.append(self.goals[f"SG_{layer_name}"])
        else:
            for goal in mapping:
                goal_mapping.append(goal)

        self.goals[goal_name] = Goal(goal_name, False, goal_mapping)
        
    def __repr__(self):
        return f"Perception Layer Model \n Secrets: \n {self.secerts} \n Layers: \n {self.security_layers} \n Goals: \n{self.goals} \n Attacker Budget:\n {self.attacker_budget}"


class Layer:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
        self.secrets = []

    def add_secrets(self, secrets):
        self.secrets += secrets

    def __repr__(self):
        return f"Security Layer: \n Name: {self.name} \n Strength: {self.strength} \n Secrets: {self.secrets}  \n"


class Goal:
    def __init__(self, name, is_trivial: bool = True, goals_mapped_to=None):
        self.name = f"SG_{name}"
        self.is_trivial = is_trivial
        self.goals_mapped_to = goals_mapped_to
        self.sec_layer_strength = 0
        if not is_trivial and self.goals_mapped_to == None:
            raise Exception("Missing mappings for a complex goal")

    def __repr__(self):
        return f"Security Goal:\n Name: {self.name} \n Type: {self.is_trivial} \n Strength {self.sec_layer_strength} \n, Goals mapped to: \n{self.goals_mapped_to}]"


if __name__ == "__main__":
    pl = PerceptionLayerModel()
    layer = Layer("L1", 0.1)
    layer2 = Layer("L2", 0.5)
    layer3 = Layer("L3", 0.4)
    layer4 = Layer("L4", 0.4)
    layer5 = Layer("L5", 0.4)
    layers = [layer, layer2, layer3, layer4, layer5]
    pl.add_all_layers(layers)
    pl.build_trivial_goals()
    pl.add_complex_goal("key_leak", ("L1", "L2", "L3"), True)
    print(pl)
    # pl.create_mdp()
