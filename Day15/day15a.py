class Appendix:
    def __init__(self,sequences):
        self.sequences = sequences

    @staticmethod
    def parseInput(input):
        sequences = input.split(",")
        return Appendix(sequences)

    def __str__(self):
        return ",".join(self.sequences)

    def getSumHashScore(self):
        def getHashScore(sequence):
            current_value = 0
            for character in sequence:
                current_value += ord(character)
                current_value *= 17
                current_value %= 256
            return current_value
        sum_hash_score = 0
        for sequence in self.sequences:
            starting_score = getHashScore(sequence)
            sum_hash_score += starting_score
        return sum_hash_score




with open('./input.txt', 'r') as file:
    appendix = Appendix.parseInput(file.read())
    print(appendix.getSumHashScore())
