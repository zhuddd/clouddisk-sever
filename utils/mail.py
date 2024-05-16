import os
import smtplib

from future.backports.email.encoders import encode_base64
from future.backports.email.mime.base import MIMEBase
from future.backports.email.mime.multipart import MIMEMultipart
from future.backports.email.mime.text import MIMEText
from future.backports.email.utils import COMMASPACE, formatdate

# https://blog.csdn.net/cheng9587/article/details/110221232  配置教程
def send_mail2(mail_to, mail_from, subject, text, files=[], server="localhost", subtype='plain'):
    assert type(mail_to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = COMMASPACE.join(mail_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # 如果 text 是html，则需要设置 _subtype='html'
    # 默认情况下 _subtype='plain'，即纯文本
    msg.attach(MIMEText(text, _subtype=subtype, _charset='utf-8'))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.close()
