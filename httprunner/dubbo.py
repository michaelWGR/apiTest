#! /usr/bin/python3
import socket
import telnetlib
import json

class DubboTester(telnetlib.Telnet):
    prompt = 'dubbo>'
    coding = 'utf-8'
    host = ''
    port = ''
    service_dict = {}

    def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        super().__init__(host, port, timeout)
        self.write(b'\n')
        self.host = host
        self.port = port
        for service in self._get_service_list():
            service_name = service.split('.')[-1]
            self.service_dict[service_name] = service

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def _parse_args(self, args):
        if isinstance(args, str) or isinstance(args, dict):
            args = json.dumps(args)
        elif isinstance(args, list):
            tmp = ''
            for param in args:
                tmp += json.dumps(param) + ','
            args = tmp[0:-1]
        return args

    def invoke(self, service_name, method_name, arg, parse=True):
        # command_str = 'invoke {0}.{1}('.format(service_name, method_name)
        if parse:
            arg = self._parse_args(arg)
        if '.' not in service_name:
            service_name = self.service_dict[service_name]
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

    def _get_service_list(self):
        service_list = self.do('ls')
        service_list.pop()
        result = []
        for service in service_list:
            result.append(service[:-1])
        return result

    def _get_method_list(self, service_name, detail=False):
        if '.' not in service_name:
            service_name = self.service_dict[service_name]
        if detail:
            method_list = self.do('ls -l %s' % service_name)
        else:
            method_list = self.do('ls %s' % service_name)
        method_list.pop()
        result = []
        for method in method_list:
            result.append(method[:-1])
        return result

    def print_method_list(self, package=None):
        if package:
            title = '* 服务%s的方法列表：' % package.split('.')[-1]
            result = self._get_method_list(package, True)
        else:
            title = '* %s:%s 的服务列表：' % (self.host, self.port)
            result = self.service_dict.values()
        print('=' * 80)
        print(title)
        print('-' * 80)
        for item in result:
            print('*', item)
        print('=' * 80)


if __name__ == '__main__':
    try:
        # telnet连接服务器
        conn = DubboTester('10.60.7.222', 20885)

        # 查看服务列表
        conn.print_method_list()

        # 查看服务的方法详情列表
        conn.print_method_list('HllGetUserCourseHourService')

        # 调用接口
        result = ''
        service = "HllGetUserCourseHourService"
        method = "getUserCourseInfoDetail"
        params = [600010, True, True, 1, 10]

        result = conn.invoke(service, method, params)

        # 打印结果
        print('执行结果：')
        print(json.loads(result))

        # 关闭连接
        conn.close()
    except TimeoutError:
        print('连接超时，请检查ip和端口!')
    except json.JSONDecodeError:
        # 解析json失败，打印原始输出
        print(result)