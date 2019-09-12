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

#########################################################
#学生APP调用方法
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

def init_apply_delivery_info_data():
    '''
    在apply_delivery_info里新增一条初始化数据
    '''
    db =MyDB()
    db.connectDB('i61-hll-manager')
    delete_apply_delivery_info_data ='''delete from apply_delivery_info where user_id=6000079;'''
    db.executeSQL(delete_apply_delivery_info_data)
    insert_apply_delivery_info_data ='''INSERT INTO `i61-hll-manager`.`apply_delivery_info` (`user_id`, `apply_teacher_id`, `apply_standard_id`, `standard_pay_date`, `send_tools_package_id`, `send_tools_addition`, `apply_type`, `apply_state`, `receiver`, `phone`, `province`, `city`, `district`, `address`, `remark`, `applicant_sso_name`, `reason`, `certificate_imgs`, `responsible_party`, `reject_reason`, `reject_time`, `delay_apply_time`, `delay_end_time`, `delay_reason`, `express_company`, `express_number`, `express_price`, `deliver_channel`, `delivery_time`, `delivery_state`, `message_code`, `outbound_time`, `manager_sso_name`, `manager_check_time`, `gmt_create`, `gmt_modified`, `reject_express_number`) VALUES ('6000079', '3', '98', '2017-12-01', '1', '', '1', '2', '测试名', '13097324208', '广东省', '广州市', '天河区', '棠下村天辉大厦楼', '', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '', '13', '4', '2018-12-26 11:47:21', '3', '200', NULL, NULL, NULL, '2019-01-16 14:49:37', '2019-08-16 17:50:32', NULL);'''
    db.executeSQL(insert_apply_delivery_info_data)
    db.closeDB()

def delete_apply_delivery_info_data():
    '''
    删除apply_delivery_info里新增的初始化数据
    '''
    db = MyDB()
    db.connectDB('i61-hll-manager')
    delete_apply_delivery_data ='''delete from apply_delivery_info where user_id=6000079;'''
    db.executeSQL(delete_apply_delivery_data)
    db.closeDB()

################################################################
# web端调用方法
##################################################################

def init_common_config_data():
    '''
    在common_config里新增一条初始化数据
    '''
    db = MyDB()
    db.connectDB('i61-draw-course')
    search_config = '''SELECT * FROM config_common WHERE conf_key='test_config';'''
    cursor = db.executeSQL(search_config)
    config_data = db.get_all(cursor)

    if len(config_data) == 0:
        insert_data = '''INSERT INTO config_common (conf_key, conf_value, type, version, description) values ('test_config', 'this is test of config', 1, '1', 'test of description');'''
        db.executeSQL(insert_data)
    elif len(config_data) == 1:
        update_data = '''update config_common set conf_value='this is test of config', TYPE=1, version='1', description='test of description' WHERE conf_key='test_config';'''
        db.executeSQL(update_data)
    else:
        delete_data = '''delete from config_common WHERE conf_key='test_config';'''
        db.executeSQL(delete_data)
        insert_data = '''INSERT INTO config_common (conf_key, conf_value, type, version, description) values ('test_config', 'this is test of config', 1, '1', 'test of description');'''
        db.executeSQL(insert_data)

    db.closeDB()

def delete_config_data():
    '''
    删除新增的数据
    '''
    db = MyDB()
    db.connectDB('i61-draw-course')
    search_config = '''SELECT * FROM config_common WHERE conf_key='test_config';'''
    cursor = db.executeSQL(search_config)
    config_data = db.get_all(cursor)
    if len(config_data) != 0:
        delete_data = '''delete from config_common WHERE conf_key='test_config';'''
        db.executeSQL(delete_data)

    db.closeDB()


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
    # init_common_config_data()
    # delete_config_data()
