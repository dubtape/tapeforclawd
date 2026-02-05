#!/usr/bin/env python3
"""
检查 QQ 邮箱未读邮件
"""
import imaplib
import email
from email.header import decode_header
import os

EMAIL_ADDR = os.getenv('QQ_EMAIL', '781291348@qq.com')
AUTH_CODE = os.getenv('QQ_EMAIL_AUTH', 'zklwmudvlnsabdce')

def decode_str(header_value):
    """解码邮件头部"""
    if not header_value:
        return ''
    decoded = []
    for content, encoding in decode_header(header_value):
        if isinstance(content, bytes):
            try:
                decoded.append(content.decode(encoding or 'utf-8', errors='ignore'))
            except:
                decoded.append(content.decode('utf-8', errors='ignore'))
        else:
            decoded.append(str(content))
    return ''.join(decoded)

def check_email():
    """检查未读邮件"""
    try:
        imap = imaplib.IMAP4_SSL('imap.qq.com', 993)
        imap.login(EMAIL_ADDR, AUTH_CODE)
        imap.select('INBOX')

        # 获取未读邮件
        status, messages = imap.search(None, 'UNSEEN')
        if not messages[0]:
            imap.logout()
            return []

        email_ids = messages[0].split()
        unseen_count = len(email_ids)

        # 获取最近 5 封未读邮件详情
        recent_ids = email_ids[-5:] if unseen_count > 5 else email_ids
        emails = []

        for eid in recent_ids:
            _, msg_data = imap.fetch(eid, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = decode_str(msg.get('Subject', ''))
            from_addr = decode_str(msg.get('From', ''))
            date = msg.get('Date', '')

            emails.append({
                'subject': subject,
                'from': from_addr,
                'date': date,
            })

        imap.logout()
        return {
            'unseen_count': unseen_count,
            'recent_emails': emails
        }

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    result = check_email()
    if 'error' in result:
        print(f'邮件检查失败: {result["error"]}')
    else:
        count = result['unseen_count']
        print(f'📧 未读邮件: {count} 封')
        for i, e in enumerate(result['recent_emails'], 1):
            print(f'  {i}. {e["subject"][:50]}... - {e["from"]}')
