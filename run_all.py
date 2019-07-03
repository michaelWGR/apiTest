import os
from httprunner.api import HttpRunner
from httprunner.report import render_html_report
from httprunner import logger

parent_dir = os.path.dirname(os.path.realpath(__file__))
report_dir = os.path.join(parent_dir, 'reports')
if not os.path.isdir(report_dir):
    os.makedirs(report_dir)
log_path = os.path.join(report_dir, 'api.log')

def save_log(log_level):
    logger.setup_logger(log_level, log_path)

def run(path):
    runner = HttpRunner(failfast=False)
    runner.run(path)
    return runner.summary

def del_html():
    fl = os.listdir(report_dir)
    for f in fl:
        if f.endswith('.html'):
            f_path = os.path.join(report_dir, f)
            os.remove(f_path)

def main():
    # save_log('debug')
    logger.setup_logger('debug')

    path = 'testcases/call/callRecord_add.yml'
    # path = 'api/call/login.yml'
    # path = 'testsuites/'
    run(path)
    del_html()

if __name__ == '__main__':
    main()
