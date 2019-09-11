import hashlib
import os
import random
import string
import time

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


# 获取当前的时间戳，默认返回毫秒级，参数为False返回秒级
def cur_time_stamp(is_ms=True):
    cur_time = time.time()
    t = cur_time
    if is_ms:
        t = int(cur_time * 1000)
    else:
        t = int(cur_time)
    return t


user_ip = []
user_device = []
cur_user = 600001
device_list = [('00cfe0492bad4456', 2), ('12730A52-7FA9-4C74-8AA0-43737043CEC3', 3),
               ('12BECBDD-0EEB-4200-87C9-93E32C792221', 3), ('12c97a016a7e2f93', 2),
               ('189EFD97-ADD5-44E8-9EDB-5712280CD226', 3), ('22F8DEB2-1560-4F3A-8E17-6278D5D27D4F', 3),
               ('315A38FC-C6F8-47B9-8E06-016E4DD6A1F7', 3), ('3FDBF95F-09F1-4AB2-B663-BE64B2C77ED3', 3),
               ('5463A036-D03A-4753-B687-7D95A12A0AEB', 3), ('864243035516674', 2),
               ('6ff9909825612da8', 2), ('50b3fefb29353f31', 2), ('5c99c145755fb252', 2),
               ('e68a6251a95b71c2', 2), ('863328039813473', 2), ('A00000711126F2', 2),
               ('865810034050852', 2), ('b7cf2e59ae98243f', 2), ('f9c0be009cd78cd0', 2),
               ('41d681f8cd33b48d', 2), ('00cfe0492bad4456', 2), ('58e3e143e8667057', 2),
               ('5463A036-D03A-4753-B687-7D95A12A0AEB', 3), ('949a63b8e145f0c8', 2),
               ('FFCF86DA-81CB-44AC-9A51-85A67EF17677', 3), ('a48798517a1c7d0d', 2)]


def get_next_user():
    global cur_user
    user = cur_user
    cur_user += 1
    return user


def get_random_user(device_type=None):
    user_id = random.randint(600001, 600020)
    if device_type is None:
        pass
    else:
        (k, v) = device_list[(user_id - 600001) % len(device_list)]
        if device_type == 'android' and v != 2:
            return get_random_user('android')
        elif device_type == 'ios' and v != 3:
            return get_random_user('ios')
    print('random user: %d' % user_id)
    return user_id


def get_user_name(user_id):
    num = user_id - 600000
    user_name = 'test%s' % str(num)
    print('user name: %s' % user_name)
    return user_name


def random_ip():
    a = random.randint(24, 255)
    b = random.randint(192, 255)
    c = random.randint(10, 255)
    d = random.randint(10, 255)
    ip = "%d.%d.%d.%d" % (a, b, c, d)
    return ip


def get_user_ip(user_id):
    ip = None
    for (key, value) in user_ip:
        if key == user_id:
            ip = value
    if ip is None:
        ip = random_ip()
        user_ip.append((user_id, ip))
    print('ip: %s' % ip)
    return ip


def get_user_device(user_id):
    # index = int(user_id) - 600000 - 1
    device_id = None
    if user_device.__len__() > 0:
        for (key, value) in user_device:
            if key == user_id:
                device_id = value
    if device_id is None:
        index = random.randint(0, device_list.__len__() - 1)
        (key, value) = device_list[index]
        device_id = key
        user_device.append((user_id, key))
    print('device: %s' % device_id)
    return device_id


def get_device_type(device_id):
    for (key, value) in device_list:
        if key == device_id:
            return value


def get_random_float(min_num=30, max_num=100, pure_decimal=True):
    f = get_random_int(min_num, max_num)
    if pure_decimal:
        f = f / 100
        return '%.2f' % f
    else:
        return f


def get_random_int(min_num=1, max_num=6):
    return random.randint(min_num, max_num)


def sum_two(first, second):
    num = float(first) + float(second)
    if num > 100:
        num = 100
    return str(num)


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
