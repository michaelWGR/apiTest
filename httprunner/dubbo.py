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
        if isinstance(arg, str):
            arg = json.dumps(arg)
        elif isinstance(arg, list):
            tmp = ''
            for param in arg:
                tmp += str(param).replace("\'", '"') + ','
            arg = tmp[0:len(tmp) - 1]
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
        methods_list.pop(methods_list.__len__() - 1)
        return input_type, output_type


if __name__ == '__main__':
    conn = DubboTester('10.60.7.253', 20885)
    json_params = [1, 2, 3]
    result = conn.invoke(
        "com.i61.draw.core.auth.service.WorkGroupService",
        "queryTeacherId2WorkGroupName",
        json_params
    )
    # conn.get_method_info('com.i61.live.hll.api.UserInfoRpcService')
    conn.get_method_info('com.i61.live.hll.api.GroupInfoRpcService')
    print(result)
    conn.close()
