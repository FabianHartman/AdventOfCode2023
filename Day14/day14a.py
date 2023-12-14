class Dish:
    def __init__(self, columns):
        self.columns = columns

    @staticmethod
    def parseDishFromInput(read_input):
        splitted_input = read_input.splitlines()
        columns = []
        for i in range(0, len(splitted_input)):
            columns.append("")
        for column_i in range(0,len(splitted_input[0])):
            for inputString in splitted_input:
                columns[column_i] = columns[column_i]+inputString[column_i]

        return Dish(columns)

    def __str__(self):
        string = ""
        for row in self.columns:
            string+="\n"
            for element in row:
                string+=element
        return string[1:]

    def moveNorth(self):
        columns = self.columns.copy()
        new_columns = []
        for column in columns:
            column_locations_map = {}
            new_column = ""
            lowest_occupied = -1
            for nth_cell_from_north in range(0,len(column)):
                if column[nth_cell_from_north] == 'O':
                    lowest_occupied +=1
                    column_locations_map[lowest_occupied] = "O"
                    continue
                if column[nth_cell_from_north] == "#":
                    lowest_occupied = nth_cell_from_north
                    column_locations_map[lowest_occupied] = "#"
            for key in column_locations_map:
                while len(new_column)<key:
                    new_column = new_column + "."
                new_column = new_column + column_locations_map[key]
            while len(new_column)<len(column):
                new_column = new_column + "."
            new_columns.append(new_column)
        return Dish(new_columns)

    def calculateTotalNorthLoad(self):
        total_load = 0
        north_dish = self.moveNorth()
        for column in north_dish.columns:
            col_length = len(column)
            for cell_i in range(0,len(column)):
                cell = column[cell_i]
                if cell == 'O':
                    total_load += (col_length-cell_i)
        return total_load

with open('./input.txt', 'r') as file:
    dish = Dish.parseDishFromInput(file.read())
    print(dish.calculateTotalNorthLoad())
