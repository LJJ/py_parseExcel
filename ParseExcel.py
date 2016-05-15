from Config import Calculator
from Config import Condition
from Utils import Utils
import json
import insertUser
import os


# # file_path = os.path.join(BASE_DIR, 'Test_Data')
# elements = BASE_DIR.split("/")
# # elements.pop()
# path = "/".join(elements)
# print(path)

if __name__ == '__main__':
    # BASE_DIR = os.path.dirname(__file__)

    verify = insertUser.verify()
    if verify:
        BASE_DIR = './File/'

        json_file = file(BASE_DIR+"config.json")
        conf = json.load(json_file)

        allTestValue = Utils.get_test_data(BASE_DIR+conf["file1"])
        allTestValue.extend(Utils.get_test_data(BASE_DIR + conf["file2"]))
        standardList = Utils.get_standard_data(BASE_DIR + conf["standard"])

        conditions = []
        for key, value in conf["con"].items():
            conditions.append(Condition(key, value))

        condition3 = Condition("M", conf["M"]/conf["amount"])
        condition3.set_amount(conf["M"])
        conditions.append(condition3)
        nm = conf["nm"]

        config = Calculator(allTestValue, standardList, conf["amount"], nm, 1000, conditions)
        config.calculate()
        Utils.save(config.result_list)

        # x = raw_input("please enter")

