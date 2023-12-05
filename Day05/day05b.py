class AlmanacMap:
    almanacMaps = []
    def __init__(self,almanacMapParts, mapName):
        self.mapName = mapName
        self.almanacMapParts = almanacMapParts
        AlmanacMap.almanacMaps.append(self)

    @staticmethod
    def parseInputString(inputString):
        input_string_parts = inputString.split("\n")
        name = input_string_parts[0].replace(" map:","")
        alamanca_map_parts = []
        for input_string_parts_i in range(1,len(input_string_parts)):
            destination_source_range = input_string_parts[input_string_parts_i].split(" ")
            alamanca_map_parts.append(AlmanacMapPart(destination_source_range[1],destination_source_range[0],destination_source_range[2]))
        return AlmanacMap(alamanca_map_parts,name)

    def getOutcome(self,number):
        for alamancaMapPart in self.almanacMapParts:

            if alamancaMapPart.source<=number<=alamancaMapPart.source+alamancaMapPart.range:
                return number + (alamancaMapPart.destination - alamancaMapPart.source)
        return number

    def getReversedOutcome(self,number):
        for alamancaMapPart in self.almanacMapParts:
            if alamancaMapPart.destination<=number<=alamancaMapPart.destination+alamancaMapPart.range:
                return number - (alamancaMapPart.destination - alamancaMapPart.source)
        return number


class AlmanacMapPart:
    def __init__(self,source,destination,range):
        self.range = int(range)
        self.destination = int(destination)
        self.source = int(source)

    def __str__(self):
        return f"{self.destination} {self.source} {self.range}"

class Seed:
    seeds = []
    def __init__(self, number, seedrange):
        self.start = int(number)
        self.end = int(number) + int(seedrange)
        Seed.seeds.append(self)

    def __str__(self):
        return f"{self.start} till {self.end}"

    @staticmethod
    def parseSeedValues(inputString):
        seed_parts = inputString.split(" ")[1:]
        start = -1
        seeds = []
        for seed_part in seed_parts:
            if start == -1:
                start = int(seed_part)
                continue
            seed_range = int(seed_part)
            seeds.append(Seed(start,seed_range))
            start = -1
        return seeds

    @staticmethod
    def exists(number):
        for seed in Seed.seeds:
            if seed.start<=number<=seed.end:
                return True
        return False


class Location:
    def __init__(self,number):
        self.number = number

    def getOriginSeed(self):
        return Location.getOriginSeedByNumber(self.number)

    @staticmethod
    def getOriginSeedByNumber(number):
        current_value = number
        for alamancaMap in reversed(AlmanacMap.almanacMaps):
            current_value = alamancaMap.getReversedOutcome(current_value)
        return current_value

    @staticmethod
    def getFirstLocationWithSeed():
        current_location = 0
        while True:
            current_location+=1
            if Seed.exists(Location.getOriginSeedByNumber(current_location)):
                break
        return current_location





with open('./input.txt', 'r') as file:
    input_parts = file.read().split("\n\n")
    Seed.parseSeedValues(input_parts[0])
    # get the maps
    for map in range(1,len(input_parts)):
        map_as_string = input_parts[map]
        alamancaMap = AlmanacMap.parseInputString(map_as_string)
print(Location.getFirstLocationWithSeed())