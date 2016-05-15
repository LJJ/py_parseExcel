
import xlrd
import types
import xlwt
from Result import ValueResult



__author__ = 'lujiji'


def remove_null_data(a_list):
    result = []
    for value in a_list:
        if type(value) == types.FloatType and value > 13:
            if value/0.5 % 1 == 0:
                result.append(value)
    return result


class Utils:

    @classmethod
    def get_test_data(cls, path):
        test_data = xlrd.open_workbook(path)
        table = test_data.sheet_by_index(0)
        index = 0
        result = []
        while True:
            try:
                row = table.row_values(index)
                value = (row[0], row[1])
                index += 1
                if type(value[1]) == types.FloatType and value[1] > 13:
                    if value[1]/0.5 % 1 == 0:
                        result.append(value)
            except:
                break

        return result

    @classmethod
    def get_standard_data(cls, path):
        standard_data = xlrd.open_workbook(path)
        standard_table = standard_data.sheet_by_index(0)
        standard_list = []
        blank_num = 0
        for index in range(0, 100):
            code_list = remove_null_data(standard_table.row_values(index)[1:])
            if len(code_list) < 5 or code_list[0] == u"CODE":
                blank_num += 1
                if blank_num > 4:
                    break
            else:
                blank_num = 0
                standard_list.append(code_list)
        return standard_list

    @classmethod
    def save(cls, resultList):
        # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        # num_format_str='#,##0.00')

        excel = xlwt.Workbook()
        # excel.sty
        table = excel.add_sheet("result",cell_overwrite_ok=True)
        # table.write()
        first_wor = ["","","num","test","var","code","nm","zx","zx2"]

        n = 0
        for text in first_wor:
            table.write(0,n,text)
            n += 1

        base = 1
        for index in range(0,len(resultList)):
            cells = resultList[index].cells(index+1)
            for info in cells:
                y = index + base
                x = 0
                for text in info:
                    table.write(y, x, text)
                    x += 1
                base += 1
            base -= 1

        excel.save("./result.xls")
