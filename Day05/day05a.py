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


class AlmanacMapPart:
    def __init__(self,source,destination,range):
        self.range = int(range)
        self.destination = int(destination)
        self.source = int(source)

    def __str__(self):
        return f"{self.destination} {self.source} {self.range}"

class Seed:
    def __init__(self,number):
        self.number = int(number)

    def __str__(self):
        return f"{self.number}"

    def getLocation(self):
        current_value = self.number
        for alamancaMap in AlmanacMap.almanacMaps:
            current_value = alamancaMap.getOutcome(current_value)
        return current_value

        


input_seeds = []
with open('./input.txt', 'r') as file:
    input_parts = file.read().split("\n\n")
    # get the in input seeds
    for seed in input_parts[0].split(" ")[1:]:
        input_seeds.append(Seed(seed))
    # get the maps
    for map in range(1,len(input_parts)):
        map_as_string = input_parts[map]
        alamancaMap = AlmanacMap.parseInputString(map_as_string)

locations = []
for input_seed in input_seeds:
    locations.append(input_seed.getLocation())
print(min(locations))