import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, AnyStr


class SendEmail(object):

    def __init__(self, from_email: str = AnyStr, password: str = AnyStr, smtp: str = AnyStr,
                 port: int = int):

        self.from_email = from_email
        self.password = password
        self.smtp = smtp
        self.port = port

    def send_email(self, subject: str = Optional, to_email: list = list, message_email: str = AnyStr,
                   filename: str = None, path: str = None):
        """
        :param path:
        :param filename:
        :param message_email: Text message
        :param subject: Subject email
        :param to_email: To emails -> Not str
        :return:
        """
        message = MIMEMultipart('alternative')
        message['Subject'] = f'{subject}'
        message['From'] = self.from_email
        for email in to_email:
            message['To'] = email

        message.attach(MIMEText('# A Heading\nSomething else in the body', 'plain'))
        message.attach(MIMEText(message_email, 'html'))

        if filename:
            attachment = open(f'{path}/{filename}', 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            message.attach(part)
            attachment.close()

        server = smtplib.SMTP(self.smtp, self.port)
        server.starttls()
        server.login(self.from_email, self.password)
        for email in to_email:
            server.sendmail(self.from_email, email, message.as_string())
        server.quit()


