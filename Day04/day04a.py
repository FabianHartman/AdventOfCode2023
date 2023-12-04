class ScratchCard:
    def __init__(self,card_number, winning_numbers, card_numbers):
        self.card_numbers = card_numbers
        self.winning_numbers = winning_numbers
        self.card_number = card_number


    def __str__(self):
        return f"Card {self.card_number}: {self.winning_numbers} | {self.card_numbers}"

    def getCorrectNumbersOnCard(self):
        correct_numbers = []
        for scratched_number in self.card_numbers:
            if scratched_number in self.winning_numbers:
                correct_numbers.append(scratched_number)
        return correct_numbers

    def getCardWorth(self):
        if len(self.getCorrectNumbersOnCard()) == 0:
            return 0
        return pow(2,len(self.getCorrectNumbersOnCard())-1)

    @staticmethod
    def parseInputString(input_string):
        input_parts = input_string.split()
        card_number = input_parts[1].replace(":","")
        separator_index = input_parts.index("|")
        winning_numbers = convertListStringValuesToListIntValues(input_parts[2:separator_index])
        card_numbers = convertListStringValuesToListIntValues(input_parts[separator_index+1:])
        return ScratchCard(card_number,winning_numbers,card_numbers)

def convertListStringValuesToListIntValues(listWithNumericalStrings):
    list_with_numbers = []
    for numericalString in listWithNumericalStrings:
        list_with_numbers.append(int(numericalString))
    return list_with_numbers



scratch_cards = []
with open('./input.txt', 'r') as file:
    for line in file.read().splitlines():
        scratch_cards.append(ScratchCard.parseInputString(line))

total = 0
for scratch_card in scratch_cards:
    total+= scratch_card.getCardWorth()
print(total)
