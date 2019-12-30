from debugtalk import *
import hashlib
import requests
import json
import logging
from common import configDB
from run_all import *
import redis
import time

def encrypt_student_password(account, password):
    # 学生密码加密，直接写入数据库
    if account and password:
        account_byte = str(account).encode(encoding='utf-8')
        password_byte = str(password).encode(encoding='utf-8')

        md = hashlib.md5()
        md.update(password_byte)
        password_md5 = md.hexdigest()

        md = hashlib.md5()
        md.update(account_byte)
        account_md5 = md.hexdigest()

        # print('password_md5: '+ password_md5)
        # print('account_md5: '+account_md5)

        password_md5_byte = str(password_md5).encode(encoding='utf-8')

        md = hashlib.md5()
        md.update(password_md5_byte)
        password_double_md5 = md.hexdigest()
        # print('password_double_md5: '+password_double_md5)

        combination_str = ''
        for i in range(len(account_md5)):

            ascii_sum = ord(account_md5[i]) + ord(password_double_md5[i])       # ascii码数值之和
            combination_str = combination_str + str(ascii_sum)

        combination_byte = combination_str.encode(encoding='utf-8')
        md = hashlib.md5()
        md.update(combination_byte)
        combination_md5 = md.hexdigest()
        return combination_md5


def translate_code(rule):
    tran_rule = []
    rule_list = rule.strip().split(' ')
    for r in rule_list:
        if not r.replace('.', '').isdigit():
            db = configDB.MyDB()
            db.connectDB('i61-oa')

            sql = '''SELECT NAME FROM `i61-oa`.`a_attendance_tags` WHERE CODE='{}';'''.format(r)
            cursor = db.executeSQL(sql)
            name = db.get_one(cursor)

            tran_rule.append('{} '.format(name[0]))
            # print(name[0])
            db.closeDB()
        else:
            tran_rule.append('{} '.format(r))
            # print(r)

    # print(''.join(tran_rule).strip())
    return ''.join(tran_rule).strip()

def inser_sql(type, rule):
    tran_code = translate_code(rule)
    # print(type)
    # print(tran_code)
    # print(rule)
    db = configDB.MyDB()
    db.connectDB('i61-oa')

    sql = '''INSERT INTO `i61-oa`.`a_attendance_default_calculation_rule` (TYPE, rule_name, rule_code, gmt_create, gmt_modified) VALUES ({}, '{}', '{}', '2019-10-18 15:34:51', '2019-10-18 15:34:51');'''.format(type, tran_code, rule)
    cursor = db.executeSQL(sql)
    db.closeDB()
    # print(sql)

def ex_testcase():
    path1 = 'api/live/student/software_version/v1_student_app_checkUpdate.yml'
    path2 = 'testcases/live/student/software_version/v1_student_app_checkUpdate.yml'
    path3 = 'testsuites/live/teacher'

    run(path3, log_level='debug')
    # del_html()

def upload_aliyu():
    url = 'http://hualala-live.oss-cn-shenzhen.aliyuncs.com/pc/picture/screenshot/20191202/5644ba80-f96c-4463-91f6-56d904bb0788.png?Expires=1575269579&OSSAccessKeyId=LTAIq7paIVW5nzkF&Signature=H3OE8U3ELbP2N5U4jQsVzmTaAH4%3D'
    # data = {'img': ('screenshot.png', open(r'E:\michael\projectAll\apiTest\files\live\teacher\screenshot.png', 'rb'), 'image/png', {})}
    files = {'File': open(r'E:\michael\projectAll\adb_tool\data\20191029-10-46-57.png', 'rb')}
    params = {
        'Expires': '1575269579',
        'OSSAccessKeyId': 'LTAIq7paIVW5nzkF',
        'Signature': 'H3OE8U3ELbP2N5U4jQsVzmTaAH4%3D',
    }
    headers = {
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'hualala-live.oss-cn-shenzhen.aliyuncs.com',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'image/png',
        'Connection': 'keep-alive'
    }
    rp = requests.put(url=url, headers=headers, files=files)
    print(rp.content)
    # print(rp.content.body)


def main():
    l = [1,2,3,4,5,6]
    for i in list(reversed(l)):
        print(i)
    print(reversed(l))




if __name__ == '__main__':
    # main()
    # ex_testcase()
    e = encrypt_student_password('12300000010', '000000')
    print(e)
