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
            records = "?".join([inputString_parts[0]] * 5)
            amounts_of_broken = ",".join(5*[inputString_parts[1]])
            rows.append(Row(records, amounts_of_broken))
        return rows


# made a calculator instead of a method on an object to make caching easier
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

        amounts_of_broken_list = amounts_of_broken.split(",")
        if (
                records[0] in "#?"
                and int(amounts_of_broken_list[0] )<= len(records)
                and "." not in records[: int(amounts_of_broken_list[0])]
                and (int(amounts_of_broken_list[0]) == len(records) or records[int(amounts_of_broken_list[0])] != "#")
        ):
            result += self.calculate_arrangements(records[int(amounts_of_broken_list[0]) + 1:], ",".join(amounts_of_broken_list[1:]))

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
