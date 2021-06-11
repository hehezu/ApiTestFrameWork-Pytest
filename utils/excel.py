import openpyxl


def load_excel(path):
    """
    加载excel 工作簿对象
    :param path:
    :return:
    """
    return openpyxl.load_workbook(path)


def get_sheet_data(wb: openpyxl.workbook.Workbook, index=0, name=None):
    """

    :param wb: 工作簿对象
    :param index: 默认获取第一个sheet
    :param name: sheet名称
    :return:
    """
    st = wb[name] if name else wb.worksheets[index]
    sheet_data = []
    for row in list(st.rows)[1:]:
        row_data = []
        for cell in row:
            row_data.append(cell.value)
        sheet_data.append(row_data)
    return sheet_data


if __name__ == '__main__':
    workbook = load_excel("../data/test.xlsx")
    data = get_sheet_data(workbook, name='Sheet1')
    print(data)
