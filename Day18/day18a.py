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
        direction_str, amount_str = instruction_parts[0], instruction_parts[1]
        dx, dy = DigPlan.dirs[direction_str]
        direction = Direction(dx, dy)
        amount_of_blocks = int(amount_str)
        return Instruction(direction, amount_of_blocks)

class DigPlan:
    dirs = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    def __init__(self, data, instructions, borders):
        self.data = data
        self.instructions = instructions
        self.borders = borders

    @staticmethod
    def parseInput():
        data = open("./input.txt", 'r').read().strip().split('\n')
        instructions = []
        borders = []
        x, y = 0, 0
        for row in data:
            instruction = Instruction.parse_instruction_string(row)
            instructions.append(instruction)

            dx, dy = instruction.direction.dx, instruction.direction.dy
            for _ in range(instruction.amount_of_blocks):
                borders.append(Coordinate(x, y))
                x, y = x + dx, y + dy
        return DigPlan(data,instructions,borders)

    def process_data(self):
        x, y = 0, 0
        for row in self.data:
            instruction = Instruction.parse_instruction_string(row)
            self.instructions.append(instruction)

            dx, dy = instruction.direction.dx, instruction.direction.dy
            for _ in range(instruction.amount_of_blocks):
                self.borders.append(Coordinate(x, y))
                x, y = x + dx, y + dy

    def calculate_area(self):
        area = 0
        for i in range(len(self.borders) - 1):
            x1, y1 = self.borders[i].x, self.borders[i].y
            x2, y2 = self.borders[i + 1].x, self.borders[i + 1].y
            area += x1 * y2 - x2 * y1

        edge_length = len(self.borders)
        interior_area = abs(area) // 2 - edge_length // 2 + 1
        return interior_area + edge_length

digplan = DigPlan.parseInput()
print(digplan.calculate_area())
