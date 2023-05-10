#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：stock 
@File    ：mail.py
@Author  ：Xie Zhongzhao
@Date    ：2023/2/1 11:26 
'''
import smtplib
from email.mime.text import MIMEText
#处理多种形态的邮件主体我们需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
#处理图片需要 MIMEImage 类
from email.mime.image import MIMEImage
from log import console_logger, file_logger

#设置服务器所需信息
fromaddr = 'xiezhongzhao@qq.com' #邮件发送方邮箱地址
password = 'hrjkfemiaatweadc'  #密码(部分邮箱为授权码)
toaddrs = ['2234309583@qq.com'] #邮件接受方邮箱地址

def emailSendInfo(subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')

    msg['From'] = Header("xiezhongzhao <xiezhongzhao@qq.com>")
    msg['To'] = Header("2234309583@qq.com")
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP('smtp.qq.com')
        server.login(fromaddr, password) #登录发信邮箱
        server.sendmail(fromaddr, toaddrs, msg.as_string()) #发送邮件
        file_logger.info("the email was sent successfully !!!")
        server.quit()
    except smtplib.SMTPException as e:
        file_logger.info("error: {}".format(e))

# if __name__ == '__main__':
#     content = "hello, this is email content."
#     emailSendInfo(content)


