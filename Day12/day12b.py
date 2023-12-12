from functools import cache


class Row:
    def __init__(self, pattern, counts):
        self.pattern = pattern
        self.counts = counts

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
        self.records = records

    @cache
    def calculate_arrangements(self, pattern, counts):
        if not pattern:
            return len(counts) == 0

        if not counts:
            return "#" not in pattern

        result = 0

        if pattern[0] in ".?":
            result += self.calculate_arrangements(pattern[1:], counts)

        if (
                pattern[0] in "#?"
                and counts[0] <= len(pattern)
                and "." not in pattern[: counts[0]]
                and (counts[0] == len(pattern) or pattern[counts[0]] != "#")
        ):
            result += self.calculate_arrangements(pattern[counts[0] + 1:], counts[1:])

        return result

    def calculate_total_arrangements(self):
        total = 0
        for row in self.records:
            total += self.calculate_arrangements(row.pattern, row.counts)
        return total


with open("./input.txt", "r") as file:
    rows = Row.parseInputStrings(file.read().splitlines())

calculator = RowArrangementCalculator(rows)
total_arrangements = calculator.calculate_total_arrangements()
print(total_arrangements)
