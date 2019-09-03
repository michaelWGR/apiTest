import hashlib
import os
import random
import string

import yaml

from common.configDB import MyDB

parent_dir = os.path.dirname(os.path.realpath(__file__))
test_data_path = os.path.join(parent_dir, 'test_data.yml')


def yml(key):
    # 获取文件的数据
    with open(test_data_path, 'rb') as fp:
        d = yaml.load(fp, Loader=yaml.FullLoader)
        if str(key).__contains__('.'):
            keys = str(key).split('.')
            for k in keys:
                d = d[k]
            return d
        else:
            if d[key]:
                return d[key]
            else:
                return


def encrypt_md5(data):
    # MD5加密
    if data:
        str_data = str(data)
        m = hashlib.md5()
        b = str_data.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        return str_md5
    else:
        return data


def hook_print(msg):
    print(msg)


#########################################################
# 学生APP调用方法
###########################################################
def gen_random_string(len=1):
    ran_str = random.sample(string.ascii_letters + string.digits, len)
    str = "API-"
    for i in ran_str:
        str += i
    return str


def get_draw_money_rules_length(type):
    db = MyDB()
    db.connectDB('i61-draw-course')
    rulelist = []
    sql = '''select * from draw_money_rule where type = {}; '''.format(type)
    if type == 2 or type == 1:
        cursor = db.executeSQL(sql)
        rule = db.get_all(cursor)
        for i in rule:
            rulelist.append(i[2])

        db.closeDB()
        return len(rulelist)
    else:
        db.closeDB()
        return len(rulelist)


##################################################################
# 外呼系统调用方法
##################################################################


def update_version_info_of_config_in_call(isUpdate=0):
    # 设置外呼系统的版本信息
    db = MyDB()
    db.connectDB('i61-draw-course')
    if isUpdate == 0:
        global origin_info
        sql = '''select * from config_common where conf_key="headteacher_call_versionInfo";'''
        cursor = db.executeSQL(sql)
        origin_info = db.get_one(cursor)[2]

        update_info = '{"clientType":"Android","version":"1.0.2","code":10002,"downloadUrl":"https://appdev.61draw.com/dev_test/app/android/app-package_test.apk","packageSize":123456,"isCurrentLastest":0,"isNeedForceUpdate":0,"isNeedNotifyUser":1,"publishTime":1559214192694,"upgradeDes":"这是一条更新提示"}'
        sql_update = '''update config_common set conf_value = '{}' where conf_key='headteacher_call_versionInfo';'''.format(
            update_info)
        db.executeSQL(sql_update)

    if isUpdate == 1:
        sql_rollback = '''update config_common set conf_value = '{}' where conf_key='headteacher_call_versionInfo';'''.format(
            origin_info)
        db.executeSQL(sql_rollback)

    db.closeDB()


def open_audio(file_path):
    return open(file_path, 'rb')


def del_user_msg(user_id):
    db = MyDB()
    db.connectDB('i61-hll-manager')
    sql = '''delete from call_record where user_id = {}'''.format(user_id)
    db.executeSQL(sql)
    db.closeDB()


def select_user_info(response, user_id):
    rp_dict = response.json
    user_info = {}
    if rp_dict['data']:
        for i in rp_dict['data']:
            if i['id'] == int(user_id):
                user_info = i
    rp_dict['data'] = [user_info]
    response.json = rp_dict


def get_fileName_list():
    tp = ["mp3", "wma", "wav", "mod", "ra", "cd", "md", "asf", "aac", "vqf", "ape", "mid", "ogg", "m4a", "vqf", "amr"]
    fileName_list = []
    for i in tp:
        fileName = 'test.{}'.format(i)
        fileName_list.append(fileName)
    return fileName_list


if __name__ == '__main__':
    print(encrypt_md5('000000'))
