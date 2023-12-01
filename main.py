import json

with open('./Day01/input.txt', 'r') as file:
    data = file.readlines();

calibrationValues = []
for i in range(0,len(data)):
    numbers = []
    for char in data[i]:
        if char in '1234567890':
            numbers.append(char)
    calibrationValues.append(numbers[0]+numbers[-1])

calibrationValueSum = 0
for calibrationValue in calibrationValues:
    calibrationValueSum += int(calibrationValue)

print(calibrationValueSum)



