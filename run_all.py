import os
from httprunner.api import HttpRunner
from common.configemail import send_email

parent_dir = os.path.dirname(os.path.realpath(__file__))
report_dir = os.path.join(parent_dir, 'reports')
if not os.path.isdir(report_dir):
    os.makedirs(report_dir)


def run(path, log_level="INFO", log_file=None):
    """
    运行测试用例，返回报告路径
    Args:
        path(str): 测试用例路径，以当前run_all.py的父目录为根目录
    """
    runner = HttpRunner(log_level=log_level, log_file=log_file)
    report_path = runner.run(path)
    return report_path

def del_html():
    '''
    删除html报告
    '''
    fl = os.listdir(report_dir)
    for f in fl:
        if f.endswith('.html'):
            f_path = os.path.join(report_dir, f)
            os.remove(f_path)

def main():
    '''
    执行所用测试用例，并发送报告
    '''
    log_path = os.path.join(report_dir, 'api.log')
    # logger.setup_logger('debug', log_path)

    path = 'testsuites/'
    report_path = run(path, log_file=log_path)
    send_email(file_path=report_path)


if __name__ == '__main__':
    # main()

    # logger.setup_logger('info')
    # for t in range(0, 100):
    #     for i in range(0, 200):
    #         run('testcases/live/liveMonitor/deviceInfo.yml')
    #     for i in range(0, 100):
    #         run('testcases/live/liveMonitor/ipinfo.yml')
    #         run('testcases/live/liveMonitor/dynamicMonitor_android.yml')
    #         run('testcases/live/liveMonitor/dynamicMonitor_ios.yml')
    #         run('testcases/live/liveMonitor/warn.yml')
    path = 'testcases/call/login.yml'
    run(path)
