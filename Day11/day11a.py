class Image:
    def __init__(self,rows):
        self.rows = rows

    @staticmethod
    def parseInputStrings(inputStrings):
        rows = []
        empty_columns = []
        for inputString in inputStrings:
            rows += Row.parseInputString(inputString)
        for column_i in range(len(rows[0].cells)):
            all_empty = True
            for row_i in range(len(rows)):
                if rows[row_i].cells[column_i] != ".": all_empty = False
            if all_empty: empty_columns.append(column_i)
        while len(empty_columns) > 0:
            column_i = empty_columns.pop()
            for row in rows:
                row.cells.insert(column_i, ".")
        return Image(rows)

    def __str__(self):
        string = ""
        for row in self.rows:
            string+=str(row)+"\n"
        return string

    def findGalaxies(self):
        galaxy_coordinates = {}
        for row_i in range(0,len(self.rows)):
            row = self.rows[row_i]
            for cell_i in range(0,len(row.cells)):
                cell = row.cells[cell_i]
                if cell == "#":
                    galaxy_coordinates[len(galaxy_coordinates)] = Coordinate(cell_i,row_i)
        return galaxy_coordinates

class Row:
    def __init__(self, cells):
        self.cells = cells

    @staticmethod
    def parseInputString(inputString):
        cells = []
        all_empty = True
        for inputCharacter in inputString:
            if inputCharacter != '.': all_empty = False
            cells.append(inputCharacter)
        if all_empty:
            return [Row(cells.copy()),Row(cells.copy())]
        return [Row(cells)]

    def __str__(self):
        return ",".join(self.cells)

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

class Path:
    def __init__(self, startCoordinate, endCoordinate):
        self.startCoordinate = startCoordinate
        self.endCoordinate = endCoordinate

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.startCoordinate in [other.startCoordinate, other.endCoordinate] and self.endCoordinate in [other.startCoordinate, other.endCoordinate]
        return NotImplemented

    @staticmethod
    def parsePathsFromGalaxyDictionary(galaxyDictionary):
        paths = []
        galaxies = list(galaxyDictionary.keys())
        for i in range(len(galaxies)):
            for j in range(i + 1, len(galaxies)):
                start_galaxy = galaxies[i]
                end_galaxy = galaxies[j]
                path = Path(galaxyDictionary[start_galaxy], galaxyDictionary[end_galaxy])
                paths.append(path)
        return paths

    def __str__(self):
        return f"from {self.startCoordinate} to {self.endCoordinate}"

    def calculateLength(self):
        vertical_difference = abs(self.endCoordinate.row_coordinate - self.startCoordinate.row_coordinate)
        horizontal_difference = abs(self.endCoordinate.column_coordinate - self.startCoordinate.column_coordinate)
        return vertical_difference + horizontal_difference

with open('./input.txt', 'r') as file:
    image = Image.parseInputStrings(file.read().splitlines())
    galaxies = image.findGalaxies()
    paths = Path.parsePathsFromGalaxyDictionary(galaxies)
    total = 0
    for path in paths:
        total += path.calculateLength()
print(total)