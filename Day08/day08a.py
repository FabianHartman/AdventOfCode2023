class Node:
    all_nodes = {}
    def __init__(self,name,to_left,to_right):
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
        input_node_parts = input_node_string.replace("=","").replace("(","").replace(")","").replace(",","").replace("  "," ").split(" ")
        return Node(input_node_parts[0],input_node_parts[1],input_node_parts[2])

    def __str__(self):
        return f"{self.name} = ({self.to_left},{self.to_right})"


class Instructions:
    def __init__(self,instructions):
        self.instructions = instructions

    def getPlacesToGoToZZZ(self,instructions):
        visited_nodes = []
        current_node = Node.all_nodes['AAA']
        visited_nodes.append(current_node)
        while True:
            for instruction in instructions.instructions:
                if instruction == "L":
                    current_node = Node.all_nodes[current_node.to_left]
                if instruction == "R":
                    current_node = Node.all_nodes[current_node.to_right]
                visited_nodes.append(current_node)
                if current_node.name == 'ZZZ':
                    return visited_nodes
    def getAmountOfSetpsToGoToZZZ(self,instructions):
        return len(self.getPlacesToGoToZZZ(instructions))-1

with open('./input.txt', 'r') as file:
    inputStrings = file.read().splitlines()
    instructions = Instructions(inputStrings[0])
    Node.parseNodes(inputStrings[2:])
    print(instructions.getAmountOfSetpsToGoToZZZ(instructions))
