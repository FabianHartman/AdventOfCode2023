class Coordinate:
    def __init__(self, column, row):
        self.column_coordinate = column
        self.row_coordinate = row

    def __str__(self):
        return f"({self.column_coordinate},{self.row_coordinate})"

    def getColumn(self):
        return self.column_coordinate

    def getRow(self):
        return self.row_coordinate

    def sumCoordinates(self, direction, cave):
        coordinate = Coordinate(self.column_coordinate + direction.getColumn(),
                                self.row_coordinate + direction.getRow())
        if coordinate.row_coordinate < 0 or coordinate.row_coordinate >= len(cave.rows):
            raise Exception("Result row is outside the cave")
        if coordinate.column_coordinate < 0 or coordinate.column_coordinate >= len(cave.rows[0]):
            raise Exception("Result column is outside the cave")
        return coordinate

    def isTouchingUpperBorder(self):
        return self.getRow() == 0

    def isTouchingLeftBorder(self):
        return self.getColumn() == 0

    def isTouchingRightBorder(self, searchedGrid):
        max_column = len(searchedGrid[0]) - 1
        return self.getColumn() == max_column

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.column_coordinate, self.row_coordinate) == (other.column_coordinate, other.row_coordinate)
        return NotImplemented


class Beam:
    def __init__(self, direction, location):
        self.direction = direction
        self.location = location

    def __eq__(self,other):
        if isinstance(other, Beam):
            return (self.direction, self.location) == (other.direction, other.location)
        return NotImplemented


class Cave:
    def __init__(self, rows):
        self.rows = rows

    @staticmethod
    def parseInput(input):
        rows = []
        for inputString in input.splitlines():
            rows.append([x for x in inputString])
        return Cave(rows)

    def __str__(self):
        string = ""
        for row in self.rows:
            string = string + "".join(row) + "\n"
        return string[:-1]

    def findValueForCoordinate(self, coordinate):
        return self.rows[coordinate.row_coordinate][coordinate.column_coordinate]

    def calculateAmountOfEnergizedTiles(self, start_location, start_direction):
        def tryToAppendQueueWithNewBeam(queue_to_append, coordinate, direction):
            try:
                new_coordinate = coordinate.sumCoordinates(direction, self)
                beam = Beam(direction, new_coordinate)
                queue_to_append.append(beam)
            finally:
                return queue_to_append

        new_queue = [Beam(start_direction, start_location)]
        energized_locations = []
        already_calculated_beams = []
        while len(new_queue) > 0:
            queue = new_queue.copy()
            new_queue = []
            for beam in queue:
                if beam in already_calculated_beams:
                    continue
                if beam.location not in energized_locations:
                    energized_locations.append(beam.location)
                already_calculated_beams.append(beam)

                match self.findValueForCoordinate(beam.location):
                    case ".":
                        new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, beam.direction)
                    case "|":
                        if beam.direction.row_coordinate != 0:
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, beam.direction)
                        else:
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, 1))
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, -1))
                    case "-":
                        if beam.direction.column_coordinate != 0:
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, beam.direction)
                        else:
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(1, 0))
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(-1, 0))
                    case "\\":
                        if beam.direction == Coordinate(1, 0):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, 1))
                        elif beam.direction == Coordinate(-1, 0):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, -1))
                        elif beam.direction == Coordinate(0, 1):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(1, 0))
                        elif beam.direction == Coordinate(0, -1):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(-1, 0))
                    case "/":
                        if beam.direction == Coordinate(1, 0):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, -1))
                        elif beam.direction == Coordinate(-1, 0):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(0, 1))
                        elif beam.direction == Coordinate(0, 1):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(-1, 0))
                        elif beam.direction == Coordinate(0, -1):
                            new_queue = tryToAppendQueueWithNewBeam(new_queue, beam.location, Coordinate(1, 0))

        return len(energized_locations)


STARTING_POINT = Coordinate(0, 0)
STARTING_DIRECTION = Coordinate(1, 0)

with open('./input.txt', 'r') as file:
    cave = Cave.parseInput(file.read())
    print(cave.calculateAmountOfEnergizedTiles(STARTING_POINT, STARTING_DIRECTION))
