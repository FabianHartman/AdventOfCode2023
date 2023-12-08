from math import lcm


class Node:
    all_nodes = {}

    def __init__(self, name, to_left, to_right):
        self.to_right = to_right
        self.to_left = to_left
        self.name = name
        Node.all_nodes[name] = self

    @staticmethod
    def parseNodes(input_node_strings):
        for input_node_string in input_node_strings:
            Node.parseNode(input_node_string)

    @staticmethod
    def parseNode(input_node_string):
        input_node_parts = input_node_string.replace("=", "").replace("(", "").replace(")", "").replace(",",
                                                                                                        "").replace(
            "  ", " ").split(" ")
        return Node(input_node_parts[0], input_node_parts[1], input_node_parts[2])

    def __str__(self):
        return f"{self.name} = ({self.to_left},{self.to_right})"


class Instructions:
    def __init__(self, instructions):
        self.instructions = instructions

    def getPlacesToGoFromBeginToEnd(self, instructions, begin, end):
        visited_nodes = []
        current_node = Node.all_nodes[begin]
        visited_nodes.append(current_node)
        while True:
            for instruction in instructions.instructions:
                if instruction == "L":
                    current_node = Node.all_nodes[current_node.to_left]
                if instruction == "R":
                    current_node = Node.all_nodes[current_node.to_right]
                visited_nodes.append(current_node)
                if current_node.name == end:
                    return visited_nodes

    def getAmountOfStepsToGoFromBeginToEnd(self, instructions, begin, end):
        return len(self.getPlacesToGoFromBeginToEnd(instructions, begin, end)) - 1

    def getAmountOfStepsForAllToEndOnZ(self, instructions):
        amount_of_steps_per_node = []
        amount_of_steps = 0
        current_nodes = []
        for node in Node.all_nodes:
            node = Node.all_nodes[node]
            if node.name[2] == "A":
                current_nodes.append(node)
        while True:
            for instruction in instructions.instructions:
                amount_of_steps += 1
                next_nodes = []
                for current_node in current_nodes:
                    if instruction == "L":
                        next_nodes.append(Node.all_nodes[current_node.to_left])
                    if instruction == "R":
                        next_nodes.append(Node.all_nodes[current_node.to_right])

                for next_node in next_nodes:
                    if next_node.name[2] == "Z":
                        next_nodes.remove(next_node)
                        amount_of_steps_per_node.append(amount_of_steps)
                if len(next_nodes)==0: return lcm(*amount_of_steps_per_node)

                current_nodes = next_nodes


with open('./input.txt', 'r') as file:
    inputStrings = file.read().splitlines()
    instructions = Instructions(inputStrings[0])
    Node.parseNodes(inputStrings[2:])
    print(instructions.getAmountOfStepsForAllToEndOnZ(instructions))
