class Grid:
    def __init__(self, rows):
        self.rows = rows

    @staticmethod
    def parseGridFromInputStrings(inputStrings):
        rows = []
        for inputString in inputStrings:
            rows.append(Row.parseRowFromInputString(inputString))
        return Grid(rows)

    def getValueForCoordinate(self, coordinate):
        return self.rows[coordinate.row_coordinate].cells[coordinate.column_coordinate]

    def findStartingPoint(self):
        for row_i in range(0, len(self.rows)):
            row = self.rows[row_i]
            for cell_i in range(0, len(row.cells)):
                cell = row.cells[cell_i]
                if cell == "S":
                    return Coordinate(cell_i, row_i)

    def canGoUpFromStart(self):
        starting_point = self.findStartingPoint()
        if not self.isTouchingUpperBorder(starting_point):
            up_coordinate = starting_point.sumCoordinates(Coordinate(0, -1))
            return self.getValueForCoordinate(up_coordinate) in '|7F'
        return False


    def isTouchingUpperBorder(self, coordinate):
        return coordinate.row_coordinate == 0

    def isTouchingLeftBorder(self, coordinate):
        return coordinate.column_coordinate == 0

    def isInTopLeftCorner(self, coordinate):
        return self.isTouchingUpperBorder(coordinate) and self.isTouchingLeftBorder(coordinate)

    def isTouchingRightBorder(self, coordinate):
        max_column = len(self.rows[0].cells) - 1
        return coordinate.column_coordinate == max_column

    def isInTopRightCorner(self, coordinate):
        return self.isTouchingRightBorder(coordinate) and self.isTouchingUpperBorder(coordinate)

    def isTouchingBottomBorder(self, coordinate):
        max_row = len(self.rows) - 1
        return coordinate.row_coordinate == max_row

    def isInBottomLeftCorner(self, coordinate):
        return self.isTouchingBottomBorder(coordinate) and self.isTouchingLeftBorder(coordinate)

    def isInBottomRightCorner(self, coordinate):
        return self.isTouchingBottomBorder(coordinate) and self.isTouchingRightBorder(coordinate)

    def getAdjacentAccessibleTubeCoordinates(self, coordinate):
        adjacent_coordinates = []
        if not self.isTouchingUpperBorder(coordinate):
            adjacent_coordinate = coordinate.sumCoordinates(Coordinate(0, -1))
            if self.getValueForCoordinate(adjacent_coordinate) in '|7F':
                if self.getValueForCoordinate(coordinate) in 'S|JL':
                    adjacent_coordinates.append(adjacent_coordinate)
        if not self.isTouchingLeftBorder(coordinate):
            adjacent_coordinate = coordinate.sumCoordinates(Coordinate(-1,0))
            if self.getValueForCoordinate(adjacent_coordinate) in '-LF':
                if self.getValueForCoordinate(coordinate) in 'S-J7':
                    adjacent_coordinates.append(adjacent_coordinate)
        if not self.isTouchingRightBorder(coordinate):
            adjacent_coordinate = coordinate.sumCoordinates(Coordinate(1,0))
            if self.getValueForCoordinate(adjacent_coordinate) in '-J7':
                if self.getValueForCoordinate(coordinate) in 'S-FL':
                    adjacent_coordinates.append(adjacent_coordinate)
        if not self.isTouchingBottomBorder(coordinate):
            adjacent_coordinate = coordinate.sumCoordinates(Coordinate(0, 1))
            if self.getValueForCoordinate(adjacent_coordinate) in '|LJ':
                if self.getValueForCoordinate(coordinate) in 'S|F7':
                    adjacent_coordinates.append(adjacent_coordinate)
        return adjacent_coordinates

    def findFurthestRoute(self):
        starting_point = self.findStartingPoint()
        visited_coordinates = []
        new_coordinates_to_visit = [starting_point]
        steps = -1
        while len(new_coordinates_to_visit) > 0:
            coordinates_to_visit = new_coordinates_to_visit.copy()
            new_coordinates_to_visit = []
            steps+=1
            for coordinate_to_visit in coordinates_to_visit:
                for coordinate in self.getAdjacentAccessibleTubeCoordinates(coordinate_to_visit):
                    if (coordinate not in coordinates_to_visit) and (coordinate not in visited_coordinates) and (coordinate not in new_coordinates_to_visit):
                        new_coordinates_to_visit.append(coordinate)
                visited_coordinates.append(coordinate_to_visit)
        return steps

    def getTubeCoordinates(self):
        starting_point = self.findStartingPoint()
        visited_coordinates = []
        new_coordinates_to_visit = [starting_point]
        while len(new_coordinates_to_visit) > 0:
            coordinates_to_visit = new_coordinates_to_visit.copy()
            new_coordinates_to_visit = []
            for coordinate_to_visit in coordinates_to_visit:
                for coordinate in self.getAdjacentAccessibleTubeCoordinates(coordinate_to_visit):
                    if (coordinate not in coordinates_to_visit) and (coordinate not in visited_coordinates) and (coordinate not in new_coordinates_to_visit):
                        new_coordinates_to_visit.append(coordinate)
                visited_coordinates.append(coordinate_to_visit)
        return visited_coordinates

    def getAmountOfEnclosedCells(self):
        visited_coordinates = self.getTubeCoordinates()
        up_tube_types = ["\033[92m"+"|"+"\033[0m","\033[92m"+"L"+"\033[0m","\033[92m"+"J"+"\033[0m"]
        if self.canGoUpFromStart(): up_tube_types += ["\033[92m"+"S"+"\033[0m"]
        for visited_coordinate in visited_coordinates:
            self.rows[visited_coordinate.row_coordinate].cells[visited_coordinate.column_coordinate] = "\033[92m" + self.rows[visited_coordinate.row_coordinate].cells[visited_coordinate.column_coordinate] + "\033[0m"
        amount_of_enclosed_cells = 0
        for row_i in range(0,len(self.rows)):
            north_pipes = 0
            row = self.rows[row_i]
            for cell_i in range(0,len(row.cells)):
                cell = row.cells[cell_i]
                if Coordinate(cell_i,row_i) in visited_coordinates:
                    if cell in up_tube_types:
                        north_pipes += 1
                    continue
                if north_pipes % 2 == 1:
                    self.rows[row_i].cells[cell_i] = "I"
                    amount_of_enclosed_cells += 1
        print(self)
        return amount_of_enclosed_cells

    def __str__(self):
        string = ""
        for row in self.rows:
            string += str(row) + "\n"
        return string



class Row:
    def __init__(self, cells):
        self.cells = cells

    @staticmethod
    def parseRowFromInputString(inputString):
        chars = []
        for char in inputString:
            chars.append(char)
        return Row(chars)

    def __str__(self):
        colored_cells = []
        for cell in self.cells:
            if cell == "I":
                colored_cells.append("\033[91m" + cell)
            else:
                colored_cells.append("\033[0m"+cell)
        return ",".join(colored_cells)


class Coordinate:
    def __init__(self, column, row):
        self.column_coordinate = column
        self.row_coordinate = row

    def __str__(self):
        return f"({self.column_coordinate},{self.row_coordinate})"

    def sumCoordinates(self, direction):
        return Coordinate(self.column_coordinate + direction.column_coordinate,
                          self.row_coordinate + direction.row_coordinate)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.column_coordinate, self.row_coordinate) == (other.column_coordinate, other.row_coordinate)
        return NotImplemented


with open('./input.txt', 'r') as file:
    grid = Grid.parseGridFromInputStrings(file.read().splitlines())
    print(grid.getAmountOfEnclosedCells())
