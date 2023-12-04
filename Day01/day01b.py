with open('./input.txt', 'r') as file:
    data = file.readlines();

number_dict = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

calibrationValues = []
for i in range(0,len(data)):
    numbers = []
    currentAlphaNumber = ""
    for char in data[i]:
        if char in '1234567890':
            numbers.append(char)
        else:
            currentAlphaNumber+=char
            for word, num in number_dict.items():
                if word in currentAlphaNumber:
                    numbers.append(num)
                    currentAlphaNumber=""



    calibrationValues.append(numbers[0]+numbers[-1])

calibrationValueSum = 0
for calibrationValue in calibrationValues:
    calibrationValueSum += int(calibrationValue)

print(calibrationValueSum)



