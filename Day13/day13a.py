class Pattern:
    def __init__(self,rows):
        self.rows = rows

    @staticmethod
    def parsePattern(inputString):
        pattern_lines = inputString.split('\n')
        return Pattern(pattern_lines)

    def __str__(self):
        string = ""
        for row in self.rows:
            string += "\n"+"".join(row)
        return string

    def getMirrorScore(self, vertical_multiplier, horizontal_multiplier):
        total_mirror_score = 0
        vertical_score = self.findVerticalReflectionLine()
        horizontal_score = self.findHorizontalReflectionLine()
        if vertical_score > 0: total_mirror_score += (vertical_multiplier*vertical_score)
        if horizontal_score > 0: total_mirror_score += (horizontal_multiplier*horizontal_score)
        return total_mirror_score


    def findHorizontalReflectionLine(self):
        for row_i in range(0,len(self.rows)-1):
            mirror_here = True
            for column_i in range(0,len(self.rows[0])):
                column = ""
                for row_j in range(0,len(self.rows)):
                    column += self.rows[row_j][column_i]
                up_content = column[:row_i+1]
                down_content = column[row_i+1:]
                if len(up_content) < len(down_content):
                    if up_content != down_content[:len(up_content)][::-1]:
                        mirror_here = False
                        break
                else:
                    if down_content != up_content[-len(down_content):][::-1]:
                        mirror_here = False
                        break
            if mirror_here:
                return row_i+1
        return -1

    def findVerticalReflectionLine(self):
        for column_i in range(0,len(self.rows[0])-1):
            mirror_here = True
            for row in self.rows:
                left_content = row[:column_i + 1]
                right_content = row[column_i + 1:]
                if len(left_content) < len(right_content):
                    if left_content != right_content[:len(left_content)][::-1]:
                        mirror_here = False
                        break
                else:
                    if right_content != left_content[-len(right_content):][::-1]:
                        mirror_here = False
                        break
            if mirror_here:
                return column_i+1
        return -1


class Reflection:
    def __init__(self,index,column_or_row, pattern):
        self.index = index
        self.column_or_row = column_or_row
        self.pattern = pattern

    def __str__(self):
        return f"Reflection at {self.column_or_row} of {self.index} for pattern {self.pattern}"


with open('./input.txt', 'r') as file:
    patterns = []
    for line in file.read().split("\n\n"):
        patterns.append(Pattern.parsePattern(line))
    total = 0
    for pattern in patterns:
        total += pattern.getMirrorScore(1,100)
print(total)