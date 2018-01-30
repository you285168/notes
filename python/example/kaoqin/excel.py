#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple

class Excel:
    #读取excel
    @staticmethod
    def read_excel(filename, sheetname=None):
        rbook = xlrd.open_workbook(filename)
        if sheetname:
            sheet = rbook.sheet_by_name(sheetname)
        else:
            sheet = rbook.sheet_by_index(0)
        return sheet

    @staticmethod
    def save_excel(filename, data, sheetname='sheet1'):
        wbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
        style.alignment = alignment
        sheet = wbook.add_sheet(sheetname, cell_overwrite_ok=True)
        for i,temp in enumerate(data):
            for j,v in enumerate(temp):
                sheet.write(i, j, v, style)
        wbook.save(filename)

    #转换成时间格式
    @staticmethod
    def strftime(cell, format='%Y-%m-%d %H:%M:%S'):
        date = datetime(*xldate_as_tuple(float(cell), 0))
        return date.strftime(format)

    # excel转成table
    @staticmethod
    def excel_to_dict(table):
        """
        :rtype : object
        :return dict
        """
        dict2 = {}
        for i in range(1, table.nrows):
            row_content = table.row_values(i, 0, table.ncols)
            dict1 = dict(zip(table.row_values(0), row_content))
            dict2[i] = dict1
        return dict2