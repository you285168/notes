#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, logging
from log import init_log
import functools
from excel import Excel
from globals import CEnum, Dict
import math
from functools import reduce
from tkinter.filedialog import askopenfilename

init_log('./errlog', logging.DEBUG)

#加载配置
def load_static():
    table = Excel.read_excel('static.xlsx')
    tempfunc = functools.partial(Excel.strftime, format='%Y-%m-%d')
    holiday = list(map(tempfunc, table.col_values(0)[1:]))
    workday = list(filter(lambda x: x!= '', table.col_values(1)[1:]))
    workday = list(map(tempfunc, workday))
    return holiday, workday

# 是否为工作日
SATURDAY = '星期六'
SUNDAY = '星期天'
holiday = None
workday = None
def is_work_day(cell):
    global holiday
    global workday
    if not holiday or not workday:
        holiday, workday = load_static()
    if cell[ExcelIndex.date] in workday:
        return True
    if cell[ExcelIndex.date] in holiday:
        return False
    return cell[ExcelIndex.weekday] != SATURDAY and cell[ExcelIndex.weekday] != SUNDAY

#字段枚举
ExcelIndex = CEnum(
    section = 0,     #部门
    name = 1,        #名字
    jobnumber = 2,   #工号
    date = 3,        #日期
    weekday = 4,     #星期几
    punch1 = 5,      #打卡1
    punch2 = 6,      #打卡2
    workday = 7,     #工作日
    overtime = 8,    #加班时间
    absence = 9,     #缺勤时间
    forget = 10,     #漏打卡时间
    remark = 11,     #备注
)

#计算考勤时间
def cal_over_time(b, e, n=None, m=None):
    if n:
        b = max(b, n)
    if m:
        e = min(e, m)
    if b >= e:
        return 0
    return (int(e[:2]) - int(b[:2])) * 60 + (int(e[3:]) - int(b[3:]))

def main(filename):
    table = Excel.read_excel(filename)
    templist = []
    for i in range(1, table.nrows):
        temp = table.row_values(i, 0, table.ncols)
        val = None
        while temp[ExcelIndex.punch1] != '' and temp[ExcelIndex.punch1] < '06:00':
            val = temp.pop(ExcelIndex.punch1)
        if val:
            #凌晨6点前打卡算作昨天的
            index = len(templist)
            hour = int(val[:2]) + 24
            val = str(hour) + val[2:]
            if index >= 1:
                last = templist[index - 1]
                if last[ExcelIndex.name] == temp[ExcelIndex.name]:
                    if last[ExcelIndex.punch1] != '':
                        last[ExcelIndex.punch2] = val
                    else:
                        last[ExcelIndex.punch1] = val
                else:
                    logging.error('找不到昨天打卡的信息')
            else:
                logging.error('找不到昨天打卡的信息')
        #且只取最大和最小
        index = ExcelIndex.punch2 + 1
        while temp[index] != '':
            temp[ExcelIndex.punch2] = temp[index]
            index += 1

        templist.append(temp[:ExcelIndex.punch2+1])

    #去掉没有打卡数据且不是工作日的信息
    templist = list(filter(lambda param: param[ExcelIndex.punch1] != '' or is_work_day(param), templist))

    #完善考勤信息
    totaldata = Dict()
    for temp in templist:
        #添加工作日标记
        name = temp[ExcelIndex.name]
        if name not in totaldata.keys():
            totaldata[name] = Dict(
                forget = [],     #漏打卡
                late = [],       #迟到时间
                worktime = 0,    #工作日加班时间
                holidaytime = 0, #假日加班时间
                striketime = 0,  #罢工时间
                name = name,
                section = temp[ExcelIndex.section],
            )
        data = totaldata[name]

        iswork = is_work_day(temp)
        if iswork:
            temp.append('是')
        else:
            temp.append('否')

        #采集漏打卡信息
        over = temp[ExcelIndex.punch2]
        begin = temp[ExcelIndex.punch1]
        forgetstr = ''
        if iswork and begin != '' and over == '':
            # 漏打卡
            if len(data.forget) < 5:
                data.forget.append(int(date[-2:]))
                if begin > '18:00':
                    over = begin
                    begin = '09:00'
                    forgetstr = begin
                else:
                    over = '18:00'
                    forgetstr = over
            else:#超过5次就当作缺勤一整天了
                begin = ''

        # 添加加班时间
        overtime = 0
        if begin != '' and over != '':
            # 计算加班时间
            if not iswork:
                #周末加班时间
                overtime += cal_over_time(begin, over, '09:00', '12:00')
                overtime += cal_over_time(begin, over, '13:30', '18:00')
                overtime += cal_over_time(begin, over, '19:00')
            elif over > '19:00':
                #工作日加班时间
                overtime += cal_over_time(begin, over, '19:00')

        overtime = (overtime - overtime % 30) / 60
        temp.append(overtime)
        if iswork:
            data.worktime += overtime
        else:
            data.holidaytime += overtime

        #添加缺勤时间
        date = temp[ExcelIndex.date]
        absence = 0
        if iswork:
            #工作日才要计算缺勤时间
            if begin == '' or over == '':
                absence = 7.5 * 60
            else:
                #早上迟到了
                if begin > '09:05' and begin < '09:30':
                    #迟到机会
                    if len(data.late) < 3:
                        data.late.append(int(date[-2:]))
                    else:
                        absence += 1 * 60
                else:
                    absence += cal_over_time('09:05', begin, '09:05', '12:00')
                    absence += cal_over_time('13:30', begin, '13:30', '18:00')
                absence += cal_over_time(over, '12:00', '09:05', '12:00')
                absence += cal_over_time(over, '18:00', '13:30', '18:00')
                absence = math.ceil(absence / 60) * 60
            absence = min(absence, 7.5 * 60) / 60
        temp.append(absence)
        data.striketime += absence
        temp.append(forgetstr)

    #统计一个月汇总信息
    newlist = []
    for name,data in totaldata.items():
        temp = []
        temp.append(data.section)
        temp.append(data.name)
        if len(data.late) > 0:
            temp.append(len(data.late))
        else:
            temp.append('')
        if data.striketime == 0:
            data.striketime = ''
        if data.worktime == 0:
            data.worktime = ''
        if data.holidaytime == 0:
            data.holidaytime = ''
        temp.append(data.striketime)
        temp.append(data.worktime)
        temp.append(data.holidaytime)
        latestr = ''
        if len(data.late) > 0:
            latestr += str(reduce(lambda x, y: str(x) + '、' + str(y), data.late))
            latestr += '日迟到机会，'
        for info in templist:
            absence = info[ExcelIndex.absence]
            if info[ExcelIndex.name] == name and absence > 0:
                date = info[ExcelIndex.date]
                latestr += str(int(date[-2:])) + '日' + str([str(absence),int(absence)][int(absence) == absence]) + 'h，'
        temp.append(latestr)
        forgetstr = ''
        if len(data.forget) > 0:
            forgetstr += str(reduce(lambda x, y: str(x) + '、' + str(y), data.forget))
            forgetstr += '日漏打卡'
        temp.append(forgetstr)
        newlist.append(temp)

    #存储到excel
    caption = table.row_values(0, 0, ExcelIndex.punch2+1)
    caption.append('工作日')
    caption.append('加班时间')
    caption.append('缺勤时间')
    caption.append('漏打卡时间')
    templist.insert(0, caption)
    Excel.save_excel('明细表.xls', templist, 'sheet1')

    caption = []
    caption.append('组别')
    caption.append('姓名')
    caption.append('9:30前迟到（3次及以内）')
    caption.append('本月累积缺勤时间')
    caption.append('工作日加班时间')
    caption.append('节假日加班时间')
    caption.append('请假说明')
    caption.append('漏打卡说明')
    newlist.insert(0, caption)
    Excel.save_excel('汇总.xls', newlist, 'sheet2')


filename = askopenfilename(initialdir = ".",title = "choose your file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
if filename:
    main(filename)