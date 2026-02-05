#!/usr/bin/env python3
"""
通过 QQ 邮箱发送邮件
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

EMAIL_ADDR = '781291348@qq.com'
AUTH_CODE = 'zklwmudvlnsabdce'

def send_email(to_email, subject, body, attachment_path=None):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDR
        msg['To'] = to_email
        msg['Subject'] = subject

        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

        # 发送邮件
        with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
            server.login(EMAIL_ADDR, AUTH_CODE)
            server.send_message(msg)

        print(f'✅ 邮件已发送至 {to_email}')
        return True

    except Exception as e:
        print(f'❌ 邮件发送失败: {e}')
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 4:
        print('用法: python3 send_email.py <收件人> <主题> <正文> [附件路径]')
        sys.exit(1)

    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None

    send_email(to_email, subject, body, attachment)
