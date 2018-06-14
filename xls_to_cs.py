#! /usr/bin/env python
# coding=utf-8
import codecs
import copy
import os
import traceback
from itertools import groupby

import time,datetime

import sys
from jinja2 import Environment, FileSystemLoader
import xlrd


def get_action_fullname(onerow,offset=0):
    """获取完整名称

    :param onerow: 一行数据
    :param offset: 是否需要反向
    """
    header= "" if not onerow[4] else "%s2%s_" % (onerow[4+offset][0],onerow[5-offset][0])
    body=onerow[3]
    footer=""
    if onerow[6]==1 and onerow[7]==1:  # 同时满足是actor并且有返回消息时才加后缀
        footer = "Request" if offset == 0 else "Response"
    return header+body+footer


file_template_path = "template"
env = Environment(loader=FileSystemLoader(file_template_path))
env.filters['get_action_fullname'] = get_action_fullname  # 自定义过滤器
excel_file=xlrd.open_workbook('config.xlsx')


def create_files_by_messagetype(excel_sheets, filename):
    sheet = excel_sheets.sheet_by_name(filename)
    sheet_list = [sheet.row_values(i) for i in range(2, sheet.nrows)]
    temple = env.get_template('Opcode.txt')
    get_str = temple.render(sheet=sheet_list,message_type=filename)
    new_file = codecs.open("gen/%sOpcode.cs"%filename, 'w', "utf-8")
    new_file.write(get_str)
    new_file.close()
    # 生成
    temple = env.get_template('Message.template')
    get_str = temple.render(sheet=sheet_list)
    new_file = codecs.open("gen/%sMessage.cs"%filename, 'w', "utf-8")
    new_file.write(get_str)
    new_file.close()
    for onerow in sheet_list:
        if onerow[2]:
            temple = env.get_template('Message.template')


# 热更相关
create_files_by_messagetype(excel_file,"Hotfix")
