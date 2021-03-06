import os
from httprunner.api import HttpRunner
from httprunner import logger
from common.configemail import send_email

parent_dir = os.path.dirname(os.path.realpath(__file__))
report_dir = os.path.join(parent_dir, 'reports')
if not os.path.isdir(report_dir):
    os.makedirs(report_dir)

def run(path):
    '''
    运行测试用例，返回报告路径
    '''
    runner = HttpRunner(failfast=False)
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
    logger.setup_logger('info', log_path)

    path = 'testsuites/'
    report_path = run(path)
    send_email(file_path=report_path)

if __name__ == '__main__':
    # main()

    logger.setup_logger('debug')
    path = 'testcases/call/login.yml'
    report_path = run(path)
    # del_html()
