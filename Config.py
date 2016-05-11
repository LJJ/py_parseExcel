import random
from Result import ValueResult


# kAmount = 3500
kStandardChar = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]


class Condition:
    name = ""
    percent = 0
    index = 0
    amount = 0
    amount_pre = False

    def __init__(self, name, percent):
        self.name = name
        self.percent = percent
        self.index = kStandardChar.index(name)

    def set_amount(self, amount):
        self.amount = amount
        self.amount_pre = True


class Calculator:
    separate = 0
    var_amount = 0
    has_nm = False
    use_nm = False
    last_var = 0
    last_per = 0.0
    average = 0
    one = 0.0
    nm = 0
    zx = 0
    value_left = 0.0
    nm_value = 3.5
    standards = []
    all_test_value = []
    conditions = []
    four_code_percentage = []
    actual_amount = 0
    result_list = []
    result_dic = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0}
    m_limit = 0

    def __init__(self, test_values, standard_list, var_amount, nm, zx, *conditions):
        self.separate = len(standard_list)/3
        self.nm = nm
        self.zx = zx
        self.var_amount = var_amount
        self.standards = [standard_list[0:self.separate], standard_list[self.separate:self.separate*2], standard_list[self.separate*2:]]
        total = sum(test_values) - self.nm_value*self.nm - 1.25 * self.zx
        self.value_left = 1.25*self.zx/len(test_values)
        self.average = total/self.var_amount
        if nm > 0:
            self.has_nm = True
            self.average_with_nm = (sum(test_values)*0.3-self.nm_value*self.nm- 1 * self.zx)/self.var_amount/0.3

        self.calculate_grade_percentage(test_values)
        print(self.actual_amount)
        self.all_test_value = test_values
        self.conditions = conditions

        other_sum = 0.0
        other_per = 0.0
        for condition in conditions:
            if condition.amount_pre:
                self.m_limit = condition.amount
            other_per += condition.percent
            other_sum += self.get_specified_var_everage(self.standards[1], condition.index)*self.var_amount*condition.percent
        self.last_var = int((total - other_sum)/(self.var_amount * (1-other_per)))
        print(self.last_var)
        self.last_per = 1.0 - other_per

    def calculate(self):
        left_amount = int(self.actual_amount*0.3)
        left_nm = self.nm
        self.result_list = []
        grade_amount = [0, 0, 0]

        for value in self.all_test_value:
            if left_nm > 0:
                self.use_nm = self.probably_get_true(0.3)
                tmp_left_amount = left_amount
                if left_amount <= 0:
                    tmp_left_amount = 1
                self.one = float(tmp_left_amount)/left_nm
                if self.one <= float(self.actual_amount*0.3)/self.nm:
                    self.one = 0.2
            else:
                self.has_nm = False
                self.one = 1000

            need = self.need_var(value)
            # index = self.get_index(need)
            grade = random.randrange(0, 3)
            result = self.calculate_one_var(value, grade, need)
            self.result_list.append(result)
            left_amount -= result.amount
            left_nm -= result.nm
            grade_amount[result.grade] += 1

            for key, num in result.result.items():
                self.result_dic[key] = self.result_dic[key] + num

        for amount in grade_amount:
            print "%0.3f" % (float(amount)/len(self.result_list))
        print "nm:%d amount:%d" %(self.nm-left_nm, self.actual_amount -left_amount)
        for key, num in self.result_dic.items():
            if num > 0 and key != "M":
                print "%s: %0.3f" % (key, float(num)/(self.actual_amount-left_amount))
            elif key == "M":
                print("M:", num)

    def calculate_one_var(self, value, grade, need):
        if need == 0:
            grade = len(self.standards)-1
            index = self.separate-1
            need = 1
        index = self.get_index(need)
        code = grade * self.separate + index + 1
        result = ValueResult(grade, code, value)
        rest = value
        result.index = index
        standard = self.standards[grade][index]

        for n in range(0,need):
            var = self.pop_variable(standard, rest, result.result)
            if var is not None:
                rest -= var[1]
                result.add_var(var[0])
            elif grade < 2:
                # if result.amount > self.last_var:
                return self.calculate_one_var(value, grade+1, need)

        if self.has_nm and self.use_nm:
            need_nm = int(result.amount/self.one) + 1
            for n in range(0, need_nm):
                if rest -3.5 > 0 and int((rest-3.5)*2) != 1:
                    result.nm += 1
                    rest -= 3.5

        can_add = self.canAdd(need)
        while rest >= standard[1] and int(2*(rest-standard[0]))!= 1:
            if can_add < 1:
                if index == 2:
                    print("alert")
                return self.calculate_one_var(value, grade, need+1)
            else:
                var = self.pop_variable(standard, rest, result.result)
                if var is None:
                    var = ("A", standard[0])
                can_add -= 1
                rest -= var[1]
                result.add_var(var[0])

        while rest > 0:
            if int(rest*2)%2 > 0:
                rest -= 1.5
                result.zx += 1
            elif rest >= 3:
                per = random.randrange(0, 4)
                if per == 0:
                    result.zx += 2
                    rest -= 3
                else:
                    result.zx2 += 1
                    rest -= 1
            else:
                if rest > 20:
                    print("alert",rest)
                # if rest >= 2:
                #     var_name = result.getMutableVar()
                #     var_value = standard[kStandardChar.index(var_name)]
                #     i = 0
                #     for target_value in standard:
                #         if var_value + rest < target_value:
                #             break
                #         else:
                #             i += 1
                #     i -= 1
                #     if i > 12:
                #         i = 12
                #     target_name = kStandardChar[i]
                #     if target_name != var_name:
                #         target = standard[i]
                #         rest -= target - var_value
                #         result.exchange_var(var_name, target_name)
                #     else:
                #         result.zx2 = rest
                #         rest = 0
                # else:
                result.zx2 = rest
                rest = 0
        return result

    def calculate_grade_percentage(self, test_values):
        if self.separate == 3:
            each_amount = [0,0,0]
            x = 0
            for value in test_values:
                need = self.need_var(value)
                self.actual_amount += need
                if 0 < need <= 5:
                    x = 1
                elif 5 < need <= 10:
                    x = 2
                else:
                    x = 3
                each_amount[x-1] += 1
            for amount in each_amount:
                self.four_code_percentage.append(float(amount)/len(test_values))
            return

        each_amount = [0,0,0,0]
        x = 0
        for value in test_values:
            need = self.need_var(value)
            self.actual_amount += need
            if 0 < need <= 5:
                x = 1
            elif 5 < need <= 10:
                x = 2
            elif 10 < need <= 20:
                x = 3
            else:
                x = 4
            each_amount[x-1] += 1

        for amount in each_amount:
            self.four_code_percentage.append(float(amount)/len(test_values))

    def get_specified_var_everage(self, standard, index):
        result = 0.0
        for x in range(0,len(self.standards)):
            result += standard[x][index] * self.four_code_percentage[x]
        return result

    def need_var(self, value):
        need = int(value/self.average)
        if self.use_nm is not True :
            need = int(value/self.average_with_nm)
        # if need == 0:
        #     need = 1
        return need

    def canAdd(self, amount):
        limit = 0
        if self.separate == 3:
            if amount < 6:
                limit = 5-amount
            elif amount < 11:
                limit = 10-amount
            else:
                limit = 100
            return limit

        if amount < 6:
            limit = 5-amount
        elif amount < 11:
            limit = 10-amount
        elif amount < 21:
            limit = 20-amount
        else:
            limit = 100
        return limit


    def get_index(self, need):
        index = 0
        if self.separate == 3:
            if need < 6:
                index = 0
            elif need < 11:
                index = 1
            else:
                index = 2
            return index
        if need < 6:
            index = 0
        elif need < 11:
            index = 1
        elif need < 21:
            index = 2
        else:
            index = 3
        return index

    def pop_variable(self, standard, limit, result_dic):
        denominator = 1000.0
        current_conditions = []
        for condition in self.conditions:
            diff = limit - standard[condition.index]
            if diff >= 0 and int(diff/0.5) != 1:
                if condition.amount_pre:
                    if condition.amount > 0 and self.need_var(limit) > 40 and self.result_dic['M']< self.m_limit and "M" not in result_dic.keys():
                        return condition.name, standard[condition.index]
                    else:
                        denominator -= condition.percent * 1000
                else:
                    current_conditions.append(condition)
            else:
                denominator -= condition.percent * 1000

        last_condition = Condition(self.__find_close_last_var(standard, max)[0], self.last_per)
        diff = limit - standard[last_condition.index]
        if diff >= 0 and int(diff/0.5) != 1:
            current_conditions.append(last_condition)

        n = random.randrange(1, int(denominator)+1)
        top = 0
        for condition in current_conditions:
            top += condition.percent * 1000
            if n <= top:
                return condition.name, standard[condition.index]

        return None

    @staticmethod
    def probably_get_true(percent):
        if random.randrange(1,1001) < percent*1000:
            return True
        else:
            return False

    def __find_close_last_var(self, standard, limit):
        index = 0
        for n in range(0,len(standard)):
            if standard[n] > self.last_var:
                index = n
                break
        if index > 0:
            up = standard[index]
            down = standard[index-1]
            if limit > up or down - self.last_var < up - self.last_var:
                index -= 1
        return kStandardChar[index], standard[index]





















