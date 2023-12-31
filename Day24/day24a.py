import time

class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

class Direction:
    def __init__(self, dx, dy, dz):
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def __str__(self):
        return f"{self.dx}, {self.dy}, {self.dz}"

class Path:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return f"{self.position} @ {self.velocity}"

    @staticmethod
    def parseInput(input):
        paths = []
        for line in input.splitlines():
            pos, velo = line.split(" @ ")
            pos = Location(*map(int, pos.split(", ")))
            velo = Direction(*map(int, velo.split(", ")))
            paths.append(Path(pos, velo))
        return paths

    def intersects(self, other, match_range):
        startPositionPath1, velocityPath1 = self.position.x, self.position.y
        endPositionPath1_x = startPositionPath1 + self.velocity.dx
        endPositionPath1_y = velocityPath1 + self.velocity.dy

        startPositionPath2, velocityPath2 = other.position.x, other.position.y
        endPositionPath2_x = startPositionPath2 + other.velocity.dx
        endPositionPath2_y = velocityPath2 + other.velocity.dy

        # if the paths don't have the same direction
        denominator = (startPositionPath1 - endPositionPath1_x) * (velocityPath2 - endPositionPath2_y) - (velocityPath1 - endPositionPath1_y) * (startPositionPath2 - endPositionPath2_x)
        if denominator != 0:
            px = ((startPositionPath1 * endPositionPath1_y - velocityPath1 * endPositionPath1_x) * (startPositionPath2 - endPositionPath2_x) - (startPositionPath1 - endPositionPath1_x) * (startPositionPath2 * endPositionPath2_y - velocityPath2 * endPositionPath2_x)) / denominator
            py = ((startPositionPath1 * endPositionPath1_y - velocityPath1 * endPositionPath1_x) * (velocityPath2 - endPositionPath2_y) - (velocityPath1 - endPositionPath1_y) * (startPositionPath2 * endPositionPath2_y - velocityPath2 * endPositionPath2_x)) / denominator

            is_after_path_1 = (px > startPositionPath1) == (endPositionPath1_x > startPositionPath1)
            is_after_path_2 = (px > startPositionPath2) == (endPositionPath2_x > startPositionPath2)

            if is_after_path_1 and is_after_path_2:
                if match_range[0] <= px <= match_range[1] and match_range[0] <= py <= match_range[1]:
                    return True

        return False

    @staticmethod
    def count_intersections(paths, match_range):
        intersections_in_area = 0

        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                if paths[i].intersects(paths[j], match_range):
                    intersections_in_area += 1

        return intersections_in_area

before = time.perf_counter()

with open("./input.txt", "r") as file:
    paths = Path.parseInput(file.read())
    print(Path.count_intersections(paths, [2e14, 4e14]))
