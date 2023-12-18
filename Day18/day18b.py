class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Direction:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class Instruction:
    def __init__(self, direction, amount_of_blocks):
        self.direction = direction
        self.amount_of_blocks = amount_of_blocks

    @staticmethod
    def parse_instruction_string(instruction_string):
        instruction_parts = instruction_string.split()
        hex = instruction_parts[2].replace(")", "").replace("(", "").replace("#", "")
        hex_amount = hex[:-1]
        amount_of_blocks = int(hex_amount, 16)
        hex_direction = hex[-1]
        dirs = {
            "0":"R",
            "1":"D",
            "2":"L",
            "3":"U"
        }
        direction_str = dirs[hex_direction]
        dx, dy = DigPlan.dirs[direction_str]
        direction = Direction(dx, dy)
        return Instruction(direction, amount_of_blocks)

class DigPlan:
    dirs = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    def __init__(self, data, instructions, corners,border_length):
        self.data = data
        self.instructions = instructions
        self.corners = corners
        self.border_length = border_length

    @staticmethod
    def parseInput():
        data = open("./input.txt", 'r').read().strip().split('\n')
        instructions = []
        corners = []
        x, y = 0, 0
        for row in data:
            instruction = Instruction.parse_instruction_string(row)
            instructions.append(instruction)

            corners.append(Coordinate(x,y))
            dx, dy = instruction.direction.dx*instruction.amount_of_blocks, instruction.direction.dy*instruction.amount_of_blocks
            x, y = x + dx, y + dy
        total_border_length = sum(instruction.amount_of_blocks for instruction in instructions)
        return DigPlan(data,instructions,corners,total_border_length)

    def calculate_area(self):
        area = 0
        for i in range(len(self.corners) - 1):
            x1, y1 = self.corners[i].x, self.corners[i].y
            x2, y2 = self.corners[i + 1].x, self.corners[i + 1].y
            area += x1 * y2 - x2 * y1

        edge_length = self.border_length
        interior_area = abs(area) // 2 - edge_length // 2 + 1
        return interior_area + edge_length

digplan = DigPlan.parseInput()
print(digplan.calculate_area())

