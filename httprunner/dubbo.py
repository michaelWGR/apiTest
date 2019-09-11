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
        command_str = "invoke {0}.{1}({2})".format(
            service_name, method_name, json.dumps(arg))
        self.command(DubboTester.prompt, command_str)
        data = self.command(DubboTester.prompt, "")
        data = data.decode(DubboTester.coding, errors='ignore').split('\n')[0].strip()
        return data

    def do(self, arg):
        command_str = arg
        self.command(DubboTester.prompt, command_str)
        data = self.command(DubboTester.prompt, command_str)
        data = data.decode(DubboTester.coding, errors='ignore').split('\r\n')
        return data


if __name__ == '__main__':
    conn = DubboTester('10.60.7.253', 20885)
    json_params = {6000662}
    # result = conn.invoke(
    #     "com.i61.live.hll.api.HllGetUserCourseHourService",
    #     "getUserCourseHour",
    #     json_params
    # )
    result = str(conn.do('ls')).replace(', ', '\n')
    print(result)
    conn.close()
