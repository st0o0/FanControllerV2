#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText

class Mail:
    __smtpHost: str
    __smtpPort: int
    __smtpUser: str
    __smtpCode: str
    __mailSender: str
    __mailReceiver: str

    def __init__(self, smpthost: str, smtpPort: int, smtpUser: str, smtpCode: str, mailSender: str, mailReceiver: str):
        self.__smtpHost = smpthost
        self.__smtpPort = smtpPort
        self.__smtpUser = smtpUser
        self.__smtpCode = smtpCode
        self.__mailSender = mailSender
        self.__mailReceiver = mailReceiver

    def send(self,message: str, subject: str):
        server = smtplib.SMTP(self.__smtpHost, self.__smtpPort)
        server.starttls()
        server.login(self.__smtpUser, self.__smtpCode)
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.__mailSender
        msg['To'] = self.__mailReceiver
        server.sendmail(self.__mailSender, self.__mailReceiver, msg.as_string())
        server.quit()