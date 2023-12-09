class History:
    def __init__(self, numbers):
        self.numbers = numbers

    @staticmethod
    def parseInputStrings(inputStrings):
        histories = []
        for inputString in inputStrings:
            histories.append(History.parseInputString(inputString))
        return histories
    @staticmethod
    def parseInputString(inputString):
        history_numbers_as_string = inputString.split(" ")
        history_numbers_as_int = []
        for history_number_as_string in history_numbers_as_string:
            history_numbers_as_int.append(int(history_number_as_string))
        return History(history_numbers_as_int)

    def __str__(self):
        return f"{self.numbers}"

    @staticmethod
    def getDifferencesInSequence(sequence):
        differences = []
        for number_i in range(0,len(sequence)-1):
            difference = sequence[number_i+1]-sequence[number_i]
            differences.append(difference)
        return differences

    @staticmethod
    def getDifferencesInSequenceWithDifferencesInDifferences(sequence):
        def sequenceDifferencesArentFullyCalculated(latest_sequence):
            for sequence_value in latest_sequence:
                if sequence_value != 0: return True
            return False
        differences = [History.getDifferencesInSequence(sequence),]
        while sequenceDifferencesArentFullyCalculated(differences[-1]):
            differences.append(History.getDifferencesInSequence(differences[-1]))
        return differences

    def getExtrapolatedValue(self):
        differences = History.getDifferencesInSequenceWithDifferencesInDifferences(self.numbers)
        total_difference_for_extrapolated_value = 0
        for difference_sequence in differences:
            total_difference_for_extrapolated_value+= difference_sequence[-1]
        return self.numbers[-1]+total_difference_for_extrapolated_value

with open('./input.txt', 'r') as file:
    histories = History.parseInputStrings(file.read().splitlines())

total = 0
for history in histories:
    total+= history.getExtrapolatedValue()
print(total)