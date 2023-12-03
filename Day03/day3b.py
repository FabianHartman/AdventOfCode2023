class PartNumber:
    def __init__(self, part_number, most_left_coordinate, most_right_coordinate):
        self.most_right_coordinate = most_right_coordinate
        self.most_left_coordinate = most_left_coordinate
        self.part_number = part_number

    def __eq__(self, other):
        if isinstance(other, PartNumber):
            return (self.most_left_coordinate, self.most_right_coordinate, self.part_number) == (other.most_left_coordinate, other.most_right_coordinate, other.part_number)
        return NotImplemented


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

    def sumCoordinates(self,direction):
        return Coordinate(self.column_coordinate+direction.getColumn(),self.row_coordinate+direction.getRow())

    def isTouchingUpperBorder(self):
        return self.getRow()==0

    def isTouchingLeftBorder(self):
        return self.getColumn()==0

    def isInTopLeftCorner(self):
        return self.isTouchingUpperBorder() and self.isTouchingLeftBorder()

    def isTouchingRightBorder(self,searchedGrid):
        max_column = len(searchedGrid[0])-1
        return self.getColumn() == max_column

    def isInTopRightCorner(self,searchedGrid):
        return self.isTouchingRightBorder(searchedGrid) and self.isTouchingUpperBorder()

    def isTouchingBottomBorder(self, searchedGrid):
        max_row = len(searchedGrid)-1
        return self.getRow() == max_row

    def isInBottomLeftCorner(self,searchedGrid):
        return self.isTouchingBottomBorder(searchedGrid) and self.isTouchingLeftBorder()

    def isInBottomRightCorner(self,searchedGrid):
        return self.isTouchingBottomBorder(searchedGrid) and self.isTouchingRightBorder(searchedGrid)

    def getAdjacentCoordinates(self,searchedGrid):
        possible_directions = []
        if not self.isTouchingUpperBorder():
            possible_directions.append(Coordinate(0,-1))
        if not self.isTouchingLeftBorder():
            possible_directions.append(Coordinate(-1,0))
        if not self.isInTopLeftCorner():
            possible_directions.append(Coordinate(-1,-1))
        if not self.isTouchingRightBorder(searchedGrid):
            possible_directions.append(Coordinate(1,0))
        if not self.isInTopRightCorner(searchedGrid):
            possible_directions.append(Coordinate(1,-1))
        if not self.isTouchingBottomBorder(searchedGrid):
            possible_directions.append(Coordinate(0,1))
        if not self.isInBottomLeftCorner(searchedGrid):
            possible_directions.append(Coordinate(-1,1))
        if not self.isInBottomRightCorner(searchedGrid):
            possible_directions.append(Coordinate(1,1))
        adjacent_coordinates = []
        for direction in possible_directions:
            adjacent_coordinates.append(self.sumCoordinates(direction))
        return adjacent_coordinates

    def getAdjacentNumbersForGrid(self,searchedGrid):
        adjacent_numbers = []
        for coordinate in self.getAdjacentCoordinates(searchedGrid):
            adjacent_numbers.append(coordinate.getValueOnGrid(searchedGrid))
        return adjacent_numbers

    def getEntirePartNumberOnGrid(self,searchedGrid):
        most_right_coordinate = Coordinate(self.column_coordinate,self.row_coordinate)
        most_left_coordinate = Coordinate(self.column_coordinate,self.row_coordinate)
        part_number_parts = [self.getValueOnGrid(searchedGrid)]
        while True:
            if most_left_coordinate.column_coordinate == 0:
                break
            coordinate_to_left = most_left_coordinate.sumCoordinates(Coordinate(-1,0))
            left_value = coordinate_to_left.getValueOnGrid(searchedGrid)
            if left_value not in '1234567890':
                break
            part_number_parts.insert(0,left_value)
            most_left_coordinate = coordinate_to_left
        while True:
            if most_right_coordinate.column_coordinate+1>len(searchedGrid[0])-1:
                break
            coordinate_to_right = most_right_coordinate.sumCoordinates(Coordinate(1,0))
            right_value = coordinate_to_right.getValueOnGrid(searchedGrid)
            if right_value not in '1234567890':
                break
            part_number_parts.append(right_value)
            most_right_coordinate = coordinate_to_right
        return PartNumber(int("".join(part_number_parts)),most_left_coordinate,most_right_coordinate)



    def getAdjacentPartNumbersForGrid(self,searchedGrid):
        adjacent_part_numbers = []
        for coordinate in self.getAdjacentCoordinates(searchedGrid):
            if coordinate.getValueOnGrid(searchedGrid) in '1234567890':
                part_number = coordinate.getEntirePartNumberOnGrid(searchedGrid)
                if part_number not in adjacent_part_numbers:
                    adjacent_part_numbers.append(part_number)
        return adjacent_part_numbers

    def getGearRatio(self,searchedGrid):
        part_numbers = self.getAdjacentPartNumbersForGrid(searchedGrid)
        if len(part_numbers)!= 2:
            return 0
        return part_numbers[0].part_number*part_numbers[1].part_number


    def getValueOnGrid(self, searchedGrid):
        return searchedGrid[self.getRow()][self.getColumn()]

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return (self.column_coordinate, self.row_coordinate) == (other.column_coordinate, other.row_coordinate)
        return NotImplemented

grid = []
symbol_locations = []

with open('./input.txt', 'r') as file:
    for line in file.read().splitlines():
        line_chars = []
        for char in line:
            line_chars.append(char)
        grid.append(line_chars)

for row_coordinate in range(0,len(grid)):
    for column_coordinate in range(0,len(grid[row_coordinate])):
        if grid[row_coordinate][column_coordinate] == "*":
            symbol_locations.append(Coordinate(column_coordinate,row_coordinate))


total = 0
for location in symbol_locations:
    total+= location.getGearRatio(grid)

print(total)

