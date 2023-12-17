class Visited:
    def __init__(self):
        self.visited_set = set()

    def has_visited(self, current, direction, streak):
        return (current, direction, streak) in self.visited_set

    def mark_visited(self, current, direction, streak):
        self.visited_set.add((current, direction, streak))


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


class Route:
    def __init__(self, cost, current, direction, streak):
        self.cost = cost
        self.current = current
        self.direction = direction
        self.streak = streak


class Map:
    @staticmethod
    def parse_input(input_lines):
        height = len(input_lines)
        width = len(input_lines[0])
        grid = {Coordinate(x, y): int(n) for y, line in enumerate(input_lines) for x, n in enumerate(line)}
        return Map(height, width, grid)

    def __init__(self, height, width, grid):
        self.height = height
        self.width = width
        self.grid = grid

    def least_heat(self, minimum_streak=0, maximum_streak=10):
        start_positions = [Route(self.grid[Coordinate(1, 0)], Coordinate(1, 0), Coordinate(1, 0), 0),
                           Route(self.grid[Coordinate(0, 1)], Coordinate(0, 1), Coordinate(0, 1), 0)]
        visited = Visited()
        target = Coordinate(self.width - 1, self.height - 1)

        while start_positions:
            start_positions.sort(key=lambda x: x.cost)
            current_route = start_positions.pop(0)
            if current_route.current == target and minimum_streak <= current_route.streak:
                return current_route.cost
            if visited.has_visited(current_route.current, current_route.direction, current_route.streak):
                continue
            visited.mark_visited(current_route.current, current_route.direction, current_route.streak)
            if current_route.streak < (maximum_streak - 1):
                next_position = current_route.current + current_route.direction
                if next_position in self.grid:
                    straight_cost = current_route.cost + self.grid[next_position]
                    start_positions.append(Route(straight_cost, next_position, current_route.direction, current_route.streak + 1))
            if minimum_streak <= current_route.streak:
                left_direction = Coordinate(-current_route.direction.y, current_route.direction.x)
                right_direction = Coordinate(current_route.direction.y, -current_route.direction.x)
                left_position = current_route.current + left_direction
                if left_position in self.grid:
                    left_cost = current_route.cost + self.grid[left_position]
                    start_positions.append(Route(left_cost, left_position, left_direction, 0))
                right_position = current_route.current + right_direction
                if right_position in self.grid:
                    right_cost = current_route.cost + self.grid[right_position]
                    start_positions.append(Route(right_cost, right_position, right_direction, 0))

with open("./input.txt") as file:
    input_lines = file.read().splitlines()
map_instance = Map.parse_input(input_lines)
print(map_instance.least_heat(3, 10))

