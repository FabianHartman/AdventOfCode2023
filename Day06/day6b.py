class Race:
    def __init__(self, time, record_distance):
        self.record = record_distance
        self.time = time

    @staticmethod
    def parseRaceFromInput(inputStrings):
        times_input = inputStrings[0].split(" ")
        times = []
        distances_input = inputStrings[1].split(" ")
        distances = []
        for time_input in times_input:
            if time_input == "Time:" or time_input == "": continue
            times.append(time_input)
        for distance_input in distances_input:
            if distance_input == "Distance:" or distance_input == "": continue
            distances.append(distance_input)
        return Race(int("".join(times)),int("".join(distances)))

    @staticmethod
    def calculatedMultipliedPossibilities(races):
        multiplied_result = 1
        for race in races:
            multiplied_result *= race.getAmountOfPossibilities()
        return multiplied_result



    def getPossibleHoldTimes(self):
        possible_hold_times = []
        for possible_hold_time in range(0,self.time):
            reached_distance = (self.time - possible_hold_time) * possible_hold_time
            if reached_distance > self.record:
                possible_hold_times.append(possible_hold_time)
        return possible_hold_times

    def getAmountOfPossibilities(self):
        return len(self.getPossibleHoldTimes())


with open('./input.txt', 'r') as file:
    race = Race.parseRaceFromInput(file.read().splitlines())
    print(Race.calculatedMultipliedPossibilities([race]))


