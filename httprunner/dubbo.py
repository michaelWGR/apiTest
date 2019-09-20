import socket
import telnetlib
import json


class DubboTester(telnetlib.Telnet):
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        try:
            super().__init__(host, port, timeout)
            self.write(b'\n')
        except Exception as e:
            print(e)

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def invoke(self, service_name, method_name, arg):
        # command_str = 'invoke {0}.{1}('.format(service_name, method_name)
        if isinstance(arg, str) or isinstance(arg, dict):
            arg = json.dumps(arg)
        elif isinstance(arg, list):
            tmp = ''
            for param in arg:
                tmp += str(param).replace("\'", '"') + ','
            arg = tmp[0:-1]
        command_str = "invoke {0}.{1}({2})".format(service_name, method_name, arg)
        self.command(DubboTester.prompt, command_str)
        data = self.command(DubboTester.prompt, "")
        data = data.decode(DubboTester.coding, errors='ignore').split('\n')[0].strip()
        return data

    def do(self, arg):
        command_str = arg
        self.command(DubboTester.prompt, command_str)
        data = self.command(DubboTester.prompt, command_str)
        data = data.decode(DubboTester.coding, errors='ignore').split('\n')
        return data

    def get_method_info(self, package=None):
        input_type, output_type = None, None
        command_str = 'ls'
        if package is not None:
            command_str += ' -l %s' % package
        methods_list: list = self.do(command_str)
        methods_list.pop()
        return input_type, output_type


if __name__ == '__main__':
    conn = DubboTester('10.60.7.222', 20885)
    json_data = {
        "class": "com.i61.live.hll.vo.RegisterUserRpcVO",
        "schoolDistrict": "总部",
        "account": "正式课",
        "realName": "曾三十",
        "username": "zengsanshi",
        "stageName": "曾三十",
        "cmsDepartment": "笑笑组",
        "crmDepartment": None,
        "gender": "男",
        "graduateSchool": "华农",
        "graduateCollege": "数轴",
        "jobPhone": "18819258064",
        "role": "班主任",
        "jobNumber": "9201707",
        "employeeCatagory": "全职 - 已转正",
        "remark": None,
        "headPhoto": "https: //static.dingtalk.com/media/lAHPBE1XYUWXIY_M8Mzw_240_240.gif",
        "wechatPhoto": "https://static.dingtalk.com/media/lADPBE1XYUWXm-PNAavNApY_662_427.jpg",
        "attachment": None
    }
    result = conn.invoke(
        "com.i61.live.hll.api.AccountInfoRpcService",
        "register",
        json_data
    )
    # conn.get_method_info()
    # conn.get_method_info('com.i61.live.hll.api.GroupInfoRpcService')
    print(result)
    conn.close()
