from functools import cache


class Row:
    def __init__(self, records, amounts_of_broken):
        self.records = records
        self.amounts_of_broken = amounts_of_broken

    @staticmethod
    def parseInputStrings(inputStrings):
        rows = []
        for inputString in inputStrings:
            inputString_parts = inputString.split(" ")
            pattern = "?".join([inputString_parts[0]] * 5)
            counts = tuple(int(x) for x in inputString_parts[1].split(",")) * 5
            rows.append(Row(pattern, counts))
        return rows


class RowArrangementCalculator:
    def __init__(self, records):
        self.rows = records

    @cache
    def calculate_arrangements(self, records, amounts_of_broken):
        if not records:
            return len(amounts_of_broken) == 0

        if not amounts_of_broken:
            return "#" not in records

        result = 0

        if records[0] in ".?":
            result += self.calculate_arrangements(records[1:], amounts_of_broken)

        if (
                records[0] in "#?"
                and amounts_of_broken[0] <= len(records)
                and "." not in records[: amounts_of_broken[0]]
                and (amounts_of_broken[0] == len(records) or records[amounts_of_broken[0]] != "#")
        ):
            result += self.calculate_arrangements(records[amounts_of_broken[0] + 1:], amounts_of_broken[1:])

        return result

    def calculate_total_arrangements(self):
        total = 0
        for row in self.rows:
            total += self.calculate_arrangements(row.records, row.amounts_of_broken)
        return total


with open("./input.txt", "r") as file:
    rows = Row.parseInputStrings(file.read().splitlines())

calculator = RowArrangementCalculator(rows)
total_arrangements = calculator.calculate_total_arrangements()
print(total_arrangements)
