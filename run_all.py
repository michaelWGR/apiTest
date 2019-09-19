import os
import time

from httprunner.api import HttpRunner
from httprunner import logger
from httprunner import locusts
from common.configemail import send_email

parent_dir = os.path.dirname(os.path.realpath(__file__))
report_dir = os.path.join(parent_dir, 'reports')
if not os.path.isdir(report_dir):
    os.makedirs(report_dir)


def run(path, gen_report_name=True):
    """
    运行测试用例，返回报告路径
    Args:
        path(str): 测试用例路径，以当前run_all.py的父目录为根目录
        gen_report_name(bool): 是否以用例名来生成测试报告，等于False时使用时间戳来命名测试报告
    """
    runner = HttpRunner(failfast=False)
    report_path = runner.run(path, gen_report_name=gen_report_name)
    return report_path


def main():
    '''
    执行所用测试用例，并发送报告
    '''
    log_path = os.path.join(report_dir, 'api.log')
    logger.setup_logger('debug', log_path)

    path = 'testsuites/'
    report_path = run(path)
    send_email(file_path=report_path)


if __name__ == '__main__':
    # main()

    # logger.setup_logger('info')
    for t in range(0, 100):
        for i in range(0, 200):
            run('testcases/live/liveMonitor/deviceInfo.yml')
        for i in range(0, 100):
            run('testcases/live/liveMonitor/ipinfo.yml')
            run('testcases/live/liveMonitor/dynamicMonitor_android.yml')
            run('testcases/live/liveMonitor/dynamicMonitor_ios.yml')
            run('testcases/live/liveMonitor/warn.yml')
