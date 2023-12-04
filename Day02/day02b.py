class BlockCount:
    def __init__(self, amount, color):
        self.amount = amount
        self.color = color

    def toString(self):
        print(f"{self.amount} {self.color} blocks")

    def getColor(self):
        return self.color

    def getAmount(self):
        return self.amount


class Game:
    def __init__(self, shownBlockCounts, gameId):
        self.gameId = int(gameId.replace(":",""))
        self.shownBlockCounts = shownBlockCounts

    def toString(self):
        print(f"Game {self.gameId}: ")
        for blockCount in self.shownBlockCounts:
            blockCount.toString()


    def highestAmountOf(self,color):
        highest_amount = 0
        for block_count in self.shownBlockCounts:
            if color==block_count.getColor():
                if block_count.getAmount()>highest_amount:
                    highest_amount = block_count.getAmount()
        return highest_amount


    def isGamePossible(self,amountOfReds, amountOfBlues, amountOfGreens):
        if amountOfBlues< self.highestAmountOf("blue") or amountOfReds< self.highestAmountOf("red") or amountOfGreens< self.highestAmountOf("green"):
            return False
        return True


    def getGameIdIfGameIsPossible(self,amountOfReds, amountOfBlues, amountOfGreens):
        if self.isGamePossible(amountOfReds,amountOfBlues,amountOfGreens):
            return self.gameId
        return 0

    def calculatePower(self):
        return self.highestAmountOf("red")*self.highestAmountOf("green")*self.highestAmountOf("blue")

    @staticmethod
    def parseInputString(inputString):
        input_bits = inputString.split(" ")
        game_id = input_bits[1]
        shown_block_counts = []
        count = 0
        color = ""
        for input_bit in input_bits[2:]:
            if input_bit.isnumeric():
                count = int(input_bit)
            else:
                color = input_bit.replace(",","").replace(";","").replace("\n","")
                shown_block_counts.append(BlockCount(count,color))
        return Game(shown_block_counts,game_id)





Games = []
with open('./input.txt', 'r') as file:
    for line in file.readlines():
        Games.append(Game.parseInputString(line))

total = 0
for game in Games:
    total+= game.calculatePower()
print(total)


