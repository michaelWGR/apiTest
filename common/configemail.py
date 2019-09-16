import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from httprunner import logger
from common import get_conf


mail_dict = get_conf('MAIL')
sender = mail_dict['sender']
receivers = mail_dict['receivers']
mail_host = mail_dict['mail_host']
mail_pass = mail_dict['mail_pass']
content = mail_dict['content']
subject = mail_dict['subject']


def set_message(sender, receivers, subject, content, file_path=None):
    '''
    设置发送的邮件内容
    '''
    try:
        message = MIMEMultipart()
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = Header(subject, 'utf-8')

        if file_path:
            if os.path.exists(file_path):
                attr = MIMEText(open(file_path, 'r', encoding='utf-8').read())
                attr['Content-Type'] = 'application/octet-stream'
                attr['Content-Disposition'] = 'attachment; filename = ' + os.path.basename(file_path)
                message.attach(attr)
            else:
                logger.log_error('{} does not exist'.format(file_path))

        return message

    except Exception as ex:
        logger.log_error(str(ex))
        return

def send_email(sender=sender, receivers=receivers, mail_host=mail_host, mail_pass=mail_pass, subject=subject, content=content, file_path=None):
    '''
    发送邮件请求
    '''
    try:
        msg = set_message(sender, receivers, subject, content, file_path)

        smtp = smtplib.SMTP(mail_host, 465)
        smtp.starttls()

        mail_user = sender
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receivers.split(';'), msg.as_string())
        logger.log_info('send email successfully')
        print('send email successfully')

    except Exception as ex:
        logger.log_error(str(ex))

    
if __name__ == '__main__':
    # file_path = '../reports/1567566217.html'
    # send_email(file_path=file_path)
    smtp = smtplib.SMTP('61s2.ad61v1.com', 465)
    smtp.ehlo()
    max_limit_in_bytes = int(smtp.esmtp_features['size'])
    print(smtp.esmtp_features['size'])