class Coordinate:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return f"row: {self.row}, column: {self.column}"

    def getUpCoordinate(self):
        up_coordinate = Coordinate(self.row - 1, self.column)
        if map.getContentForCoordinate(up_coordinate) == "#":
            raise Exception("The rock")
        return up_coordinate

    def getLeftCoordinate(self):
        left_coordinate = Coordinate(self.row, self.column - 1)
        if map.getContentForCoordinate(left_coordinate) == "#":
            raise Exception("The rock")
        return left_coordinate

    def getDownCoordinate(self, map):
        down_coordinate = Coordinate(self.row + 1, self.column)
        if map.getContentForCoordinate(down_coordinate) == "#":
            raise Exception("The rock")
        return down_coordinate

    def getRightCoordinate(self, map):
        right_coordinate = Coordinate(self.row, self.column + 1)
        if map.getContentForCoordinate(right_coordinate) == "#":
            raise Exception("The rock")
        return right_coordinate

    def getAdjacentCoordinates(self, map):
        adjacent_coordinates = []
        try:
            adjacent_coordinates.append(self.getUpCoordinate())
        finally:
            try:
                adjacent_coordinates.append(self.getLeftCoordinate())
            finally:
                try:
                    adjacent_coordinates.append(self.getDownCoordinate(map))
                finally:
                    try:
                        adjacent_coordinates.append(self.getRightCoordinate(map))
                    finally:
                        return adjacent_coordinates

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.row, self.column) == (other.row, other.column)
        return NotImplemented


class Map:
    def __init__(self, rows):
        self.rows = rows

    @staticmethod
    def parseMap(input):
        rows = []
        for inputString in input.splitlines():
            rows.append([x for x in inputString])
        return Map(rows)

    def __str__(self):
        string = "Map:"
        for row in self.rows:
            string = string + "\n" + "".join(row)
        return string

    def getStartingLocation(self):
        for row_i, row in enumerate(self.rows):
            for col_i, cell in enumerate(row):
                if cell == "S":
                    return Coordinate(row_i, col_i)

    def getContentForCoordinate(self, coordinate):
        return self.rows[coordinate.row%len(self.rows)][coordinate.column%len(self.rows[coordinate.row])]

    def getLocationsAfterNIterations(self, n):
        new_locations = [self.getStartingLocation()]
        for iteration in range(1,n+1):
            print(iteration)
            locations = new_locations
            new_locations = []
            for location in locations:
                for new_location in location.getAdjacentCoordinates(self):
                    if new_location not in new_locations:
                        new_locations.append(new_location)
        return new_locations

    def getAmountOfLocationsAfterNIterations(self, n):
        return len(self.getLocationsAfterNIterations(n))


with open('./input.txt', 'r') as file:
    map = Map.parseMap(file.read())
    print(map.getAmountOfLocationsAfterNIterations(26501365))
