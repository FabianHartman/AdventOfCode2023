class Row:
    def __init__(self, amounts_of_broken, records):
        self.amounts_of_broken = amounts_of_broken
        self.records = records

    @staticmethod
    def parseInputStrings(inputStrings):
        rows = []
        for inputString in inputStrings:
            inputString_parts = inputString.split(" ")
            rows.append(Row(inputString_parts[1], inputString_parts[0]))
        return rows

    def __str__(self):
        return f"{self.records} {self.amounts_of_broken}"

    def getDefinitelyBrokenSprings(self):
        return self.records.count("#")

    def calculateAmountOfBrokenSpringsToFind(self):
        return self.calculateTotalAmountOfBrokenSprings() - self.getDefinitelyBrokenSprings()

    def calculateTotalAmountOfBrokenSprings(self):
        total_broken_springs = 0
        broken_spring_counts = self.amounts_of_broken.split(",")
        for broken_spring_count in broken_spring_counts:
            total_broken_springs += int(broken_spring_count)
        return total_broken_springs

    def getAmountOfCorrectPossibilities(self):
        amount_of_correct_possibilities = 0
        for possibility in self.getAllBruteForcedPossibilities():
            if self.isRowCorrect(possibility):
                amount_of_correct_possibilities += 1
        return amount_of_correct_possibilities

    @staticmethod
    def countConsecutiveHashes(record):
        consecutiveString = ""
        current_consecutive = 0
        for char in record:
            if char == "#":
                current_consecutive += 1
            else:
                if current_consecutive > 0:
                    consecutiveString += f",{current_consecutive}"
                current_consecutive = 0
        if current_consecutive > 0:
            consecutiveString += f",{current_consecutive}"
        return consecutiveString[1:]

    def isRowCorrect(self,possibility):
        return self.amounts_of_broken == Row.countConsecutiveHashes(possibility)

    def getAllBruteForcedPossibilities(self):
        return Row.generate_options(self.records,self.calculateAmountOfBrokenSpringsToFind())


    @staticmethod
    def generate_options(record, num_hashes, current_index=0):
        if num_hashes == 0:
            return [record]

        options = []

        for i in range(current_index, len(record)):
            if record[i] == '?':
                new_record = record[:i] + '#' + record[i + 1:]
                options.extend(Row.generate_options(new_record, num_hashes - 1, i + 1))

        return options


with open('./input.txt', 'r') as file:
    rows = Row.parseInputStrings(file.read().splitlines())
    total = 0
    for row in rows:
        total+= row.getAmountOfCorrectPossibilities()
    print(total)
