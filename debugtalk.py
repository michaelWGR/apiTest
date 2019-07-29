import os
import yaml
import hashlib
import json
from common.configDB import MyDB

parent_dir = os.path.dirname(os.path.realpath(__file__))
test_data_path = os.path.join(parent_dir, 'test_data.yml')

def yml(key):
    # 获取文件的数据
    with open(test_data_path, 'rb') as fp:
        d = yaml.load(fp, Loader=yaml.FullLoader)
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

def encrypt_student_password(account, password):
    # 学生密码加密
    if account and password:
        account_byte = str(account).encode(encoding='utf-8')
        password_byte = str(password).encode(encoding='utf-8')
        # print(account_byte)
        # print(password_byte)
        md = hashlib.md5()

        md.update(password_byte)
        password_md5 = md.hexdigest()[8:24]
        # print(len(password_md5))

        md.update(account_byte)
        account_md5 = md.hexdigest()

        print(password_md5)
        print(account_md5)

        password_md5_byte = str(password_md5).encode(encoding='utf-8')
        md.update(password_md5_byte)
        password_double_md5 = md.hexdigest()
        print(password_double_md5)

        combination_str = ''
        for i in range(len(account_md5)):
            combination_str = combination_str + account_md5[i] + password_double_md5[i]
        print(combination_str)

        combination_byte = combination_str.encode(encoding='utf-8')
        md.update(combination_byte)
        combination_md5 = md.hexdigest()
        print(combination_md5)

##################################################################
#外呼系统调用方法
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
        sql_update = '''update config_common set conf_value = '{}' where conf_key='headteacher_call_versionInfo';'''.format(update_info)
        db.executeSQL(sql_update)

    if isUpdate == 1:
        sql_rollback = '''update config_common set conf_value = '{}' where conf_key='headteacher_call_versionInfo';'''.format(origin_info)
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
    # s = 123456
    # print(len(encrypt_md5(s)))
    # print(encrypt_md5(s))
    # print(yml('user_id'))
    # del_user_msg(306955)
    # print(get_fileName_list())
    encrypt_student_password('13097301001','000000')
    print(len('726d2161d72e38e7cfd3972e599c46d1'))