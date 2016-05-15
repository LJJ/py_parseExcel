__author__ = 'lujiji'

kStandardChar = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]

class ValueResult:
    name = ""
    result = {}
    grade = 0
    code = 0
    amount = 0
    nm = 0
    zx = 0
    zx2 = 0
    sum = 0
    index = 0
    originalValue = 0.0

    def __init__(self, grade, code, originalValue):
        self.result = {}
        self.grade = grade
        self.code = code
        self.originalValue = originalValue

    def add_var(self, name):
        self.amount += 1
        if name in self.result.keys():
            x = self.result[name]
            self.result[name] = x + 1
        else:
            self.result[name] = 1

    def __str__(self):
        des = "%d %d" % (self.amount, self.index+1)
        return self.result.__str__() + des

    def cells(self, index):
        isFirst = True
        list = []
        for key, value in self.result.items():
            if value == 0:
                continue
            if isFirst:
                isFirst = False
                list.append([index,self.name, self.originalValue, key, value, self.code, self.nm, self.zx, self.zx2])
            else:
                list.append(["","","",key,value, "","","",""])

        return list

    def getMutableVar(self):
        target = []
        var_name = "M"
        for key, value in self.result.items():
            if key == "E" or key == "F" or key == "M":
                continue
            elif value > 0:
                target.append(key)
        if len(target) == 0:
            if "E" in self.result.keys() and self.result["E"] > 0:
                var_name = "E"
            elif "F" in self.result.keys() and self.result["F"] > 0:
                var_name = "F"
            # else:
            #     var_name = None
        else:
            for name in target:
                if kStandardChar.index(name) <= kStandardChar.index(var_name):
                    var_name = name
        return var_name

    # def getMutableVar(self):
    #     target = self.result.keys()
    #     for key in target:
    #         if kStandardChar.index(key)

    def exchange_var(self,var1_name, var2_name):
        try:
            index =self.result[var1_name]
        except:
            print("alert")
        else:
            self.result[var1_name] -= 1
            self.add_var(var2_name)
            self.amount -= 1
