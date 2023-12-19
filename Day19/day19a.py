class Workflow:
    def __init__(self,name,criteria):
        self.name = name
        self.criteria = criteria

    @staticmethod
    def parseWorkflows(input):
        workflows = []
        for inputString in input.split():
            criteria = []
            inputStringParts = inputString.split("{")
            name = inputStringParts[0]
            criteria_part = inputStringParts[1].replace("}","")
            criteria_parts = criteria_part.split(",")
            for criteria_part in criteria_parts:
                criterium = Criterium.parseInput(criteria_part)
                criteria.append(criterium)
            workflows.append(Workflow(name, criteria))
        return workflows

    def __str__(self):
        string = f"{self.name}"
        for criterium in self.criteria:
            string = string +" "+ str(criterium)
        return string

    @staticmethod
    def findWorkflowWithLabel(workflows,label):
        for workflow in workflows:
            if workflow.name == label:
                return workflow

    @staticmethod
    def findStartingWorkflow(workflows):
        for workflow in workflows:
            if workflow.name == "in":
                return workflow

    def solveWorkflow(self,xmasItem,workflows):
        for criterium in self.criteria:
            if criterium.isCriteriaMet(xmasItem):
                if criterium.next_criterium == "R":
                    return
                if criterium.next_criterium == "A":
                    return xmasItem
                return Workflow.findWorkflowWithLabel(workflows,criterium.next_criterium).solveWorkflow(xmasItem,workflows)

class Criterium:
    def __init__(self,variable,smaller_greater,comparison_value,next_criterium):
        self.variable = variable
        self.smaller_greater = smaller_greater
        self.comparison_value = comparison_value
        self.next_criterium = next_criterium

    @staticmethod
    def parseInput(input):
        smaller_greater = ""
        if ">" in input:
            smaller_greater = ">"
        if "<" in input:
            smaller_greater = "<"
        if smaller_greater == "":
            return Criterium("","","",input)
        variable = input[:input.index(smaller_greater)]
        comparison_value = input[input.index(smaller_greater)+1:input.index(":")]
        next_criterium = input[input.index(":")+1:]
        return Criterium(variable,smaller_greater,comparison_value,next_criterium)

    def hasCondition(self):
        return self.smaller_greater != ""

    def isCriteriaMet(self,xmasItem):
        if not self.hasCondition(): return True
        xmasItemVariableValue = xmasItem.getVariableValue(self.variable)
        if self.smaller_greater == "<":
            return xmasItemVariableValue<int(self.comparison_value)
        if self.smaller_greater == ">":
            return xmasItemVariableValue>int(self.comparison_value)



    def __str__(self):
        return f"{self.variable} {self.smaller_greater} {self.comparison_value} {self.next_criterium}"

class XMASItem:
    def __init__(self,x,m,a,s):
        self.x=x
        self.m=m
        self.a=a
        self.s=s

    @staticmethod
    def parseInput(input):
        xmasItems = []
        for inputString in input.splitlines():
            inputString = inputString.replace("}","").replace("{","")
            inputStringParts = inputString.split(",")
            x = int(inputStringParts[0][2:])
            m = int(inputStringParts[1][2:])
            a = int(inputStringParts[2][2:])
            s = int(inputStringParts[3][2:])
            xmasItems.append(XMASItem(x,m,a,s))
        return xmasItems

    def __str__(self):
        return f"{self.x} {self.m} {self.a} {self.s}"

    def getVariableValue(self,variable):
        match variable:
            case "x": return self.x
            case "m" : return self.m
            case "a" : return self.a
            case "s" : return self.s

    def getSum(self):
        return self.a+self.m+self.s+self.x


class Worker:
    def __init__(self,workflows,xmasItems):
        self.workflows = workflows
        self.xmasItems = xmasItems

    def getAcceptedPartSumTotal(self):
        sumTotal = 0
        starting_workflow = Workflow.findStartingWorkflow(self.workflows)
        for xmasItem in self.xmasItems:
            current_workflow = starting_workflow
            solvedItem = current_workflow.solveWorkflow(xmasItem,workflows)
            if solvedItem != None:
                sumTotal += solvedItem.getSum()
        return sumTotal





with open('./input.txt', 'r') as file:
    data = file.read().split("\n\n")
    workflows = Workflow.parseWorkflows(data[0])
    xmasItems = XMASItem.parseInput(data[1])
    worker = Worker(workflows,xmasItems)
    print(worker.getAcceptedPartSumTotal())