from functools import cache

def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

class Dish:
    def __init__(self, columns):
        self.columns = columns

    def __eq__(self, other):
        if isinstance(other, Dish):
            return self.columns == other.columns
        return NotImplemented

    def __hash__(self):
        return hash(tuple(tuple(column) for column in self.columns))



    @staticmethod
    def parseDishFromInput(read_input):
        splitted_input = read_input.splitlines()
        columns = []
        for i in range(0, len(splitted_input)):
            columns.append("")
        for column_i in range(0, len(splitted_input[0])):
            for inputString in splitted_input:
                columns[column_i] = columns[column_i] + inputString[column_i]
        return Dish(columns)

    def __str__(self):
        string = ""
        for row_i in range(0,len(self.columns[0])):
            row_string = ""
            for column in self.columns:
                row_string = row_string + column[row_i]
            string = string + row_string + "\n"
        return string[:-1]


    def rotate(self):
        amount_of_rows = len(self.columns[0])
        cols = len(self.columns)

        rotated_grid = [['' for _ in range(amount_of_rows)] for _ in range(cols)]

        for i in range(amount_of_rows):
            for j in range(cols):
                new_i = amount_of_rows - 1 - j
                new_j = i

                rotated_grid[new_i][new_j] = self.columns[i][j]

        rotated_dish = Dish(rotated_grid)
        return rotated_dish

    @cache
    def moveNorth(self):
        columns = self.columns.copy()
        new_columns = []
        for column in columns:
            column_locations_map = {}
            new_column = ""
            lowest_occupied = -1
            for nth_cell_from_north in range(0, len(column)):
                if column[nth_cell_from_north] == 'O':
                    lowest_occupied += 1
                    column_locations_map[lowest_occupied] = "O"
                    continue
                if column[nth_cell_from_north] == "#":
                    lowest_occupied = nth_cell_from_north
                    column_locations_map[lowest_occupied] = "#"
            for key in column_locations_map:
                while len(new_column) < key:
                    new_column = new_column + "."
                new_column = new_column + column_locations_map[key]
            while len(new_column) < len(column):
                new_column = new_column + "."
            new_columns.append(new_column)
        return Dish(new_columns)

    @cache
    def fullRotation(self):
        grid = self
        for i in range(0, 4):
            north_moved_grid = grid.moveNorth()
            grid = north_moved_grid.rotate()
        return grid

    def calculateTotalNorthLoad(self):
        total_load = 0
        for column in self.columns:
            col_length = len(column)
            for cell_i in range(0, len(column)):
                cell = column[cell_i]
                if cell == 'O':
                    total_load += (col_length - cell_i)
        return total_load

    def rotateNTimes(self, n):
        grid = self
        i = 0
        previous_rotations = {}
        skipped_loop = False
        while i < n:
            i += 1
            grid = grid.fullRotation()
            if grid not in previous_rotations.values():
                previous_rotations[i] = grid
            else:
                if skipped_loop: continue
                origin =find_key_by_value(previous_rotations, grid)
                loop_size = i-origin
                still_needed_rotations = n - origin
                i = origin
                amount_of_loops_that_fit = still_needed_rotations//loop_size
                i+=(amount_of_loops_that_fit*loop_size)
                skipped_loop = True
        return grid


with open('./input.txt', 'r') as file:
    dish = Dish.parseDishFromInput(file.read())
    rotated_dish = dish.rotateNTimes(1000000000)
    print(rotated_dish.calculateTotalNorthLoad())
