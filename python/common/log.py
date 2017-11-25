#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a log module '

__author__ = 'Sola'

import logging
from logging.handlers import TimedRotatingFileHandler, SMTPHandler, MemoryHandler

#MemoryHandler是将日志输出的内存中定制的buffer，一旦buffer存满就发送邮件
class SMTPMemoryHandler(MemoryHandler):
    def __init__(self, capacity, mailhost, fromaddr, toaddrs, subject,
                 credentials=None, secure=None, timeout=5.0):
        MemoryHandler.__init__(self, capacity, flushLevel=logging.INFO, target=None)
        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost, self.mailport = mailhost, None
        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.subject = subject
        self.secure = secure
        self.timeout = timeout

    def flush(self):
        if self.buffer != [] and len(self.buffer) >= self.capacity:
            content = ''
            for record in self.buffer:
                content += self.format(record) + '\n'

            self.send_mail(content)
            self.buffer = []

    def send_mail(self, record):
        try:
            print("send_mail", record)
            import smtplib
            from email.message import EmailMessage
            import email.utils

            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port, timeout=self.timeout)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.subject
            msg['Date'] = email.utils.localtime()
            msg.set_content(record)
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handleError(record)


def init_log(filename, loglv):
    logger = logging.getLogger()
    logger.setLevel(loglv)

    formatter = logging.Formatter('[%(levelname)s][%(name)s] %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    fh = TimedRotatingFileHandler(filename, when='D', interval=1, backupCount=30, utc=False)
    fh.setLevel(loglv)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    mh = SMTPMemoryHandler(20, 'smtp.qq.com', 'gongjg_fz@feiyu.com', 'gongjg_fz@feiyu.com', 'python web error mail', credentials=('gongjg_fz@feiyu.com', 'Icesola1'))
    mh.setLevel(logging.DEBUG)
    mh.setFormatter(formatter)
    logger.addHandler(mh)

    ch = logging.StreamHandler()
    ch.setLevel(loglv)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

