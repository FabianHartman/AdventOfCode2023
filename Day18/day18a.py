class Edge:
    def __init__(self,coordinate,angle):
        self.coordinate = coordinate
        self.angle = angle

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

class Instruction:
    def __init__(self,direction,amountOfBlocks,color):
        self.direction = direction
        self.amountOfBlocks = amountOfBlocks
        self.color = color

    @staticmethod
    def parseInstructionString(instructionString):
        instructionStringParts = instructionString.split()
        return Instruction(instructionStringParts[0],int(instructionStringParts[1]),instructionStringParts[2].replace(")","").replace("(",""))

    def __str__(self):
        return f"{self.direction} {self.amountOfBlocks} ({self.color})"

class DigPlan:
    def __init__(self,instructions):
        self.instructions = instructions

    @staticmethod
    def parseInput(input):
        instructions = []
        for inputLine in input.splitlines():
            instructions.append(Instruction.parseInstructionString(inputLine))
        return DigPlan(instructions)

    def __str__(self):
        string = ""
        for instruction in self.instructions:
            string = string + str(instruction) + "\n"
        return string[:-1]

    def getLagoonEdgeAndCorners(self):
        edge_locations = [Coordinate(0,0)]
        last_location = Coordinate(0,0)
        for instruction in self.instructions:
            for i in range(instruction.amountOfBlocks):
                direction = instruction.direction
                match direction:
                    case "R": new_location = last_location.__add__(Coordinate(1,0))
                    case "L": new_location = last_location.__add__(Coordinate(-1,0))
                    case "U": new_location = last_location.__add__(Coordinate(0,1))
                    case "D": new_location = last_location.__add__(Coordinate(0,-1))


                if new_location not in edge_locations:
                    edge_locations.append(new_location)
                last_location = new_location
        return edge_locations

    def calculateInnerLagoonSize(self):
        edge_locations = self.getLagoonEdgeAndCorners()

        # Calculate the area of the convex hull (internal space of the lagoon) using the shoelace formula
        area = 0.0
        n = len(edge_locations)

        for i in range(n):
            j = (i + 1) % n
            area += edge_locations[i].x * edge_locations[j].y
            area -= edge_locations[j].x * edge_locations[i].y

        area = abs(area) / 2.0

        return area



with open('./input.txt', 'r') as file:
    digplan = DigPlan.parseInput(file.read())
    print(digplan.calculateInnerLagoonSize())
