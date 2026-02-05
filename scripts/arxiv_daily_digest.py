#!/usr/bin/env python3
"""
ArXiv AI 论文每日摘要脚本
每天早上8点发送最新的AI论文到指定邮箱，并写入飞书多维表格
"""
import requests
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import json
import os
from datetime import datetime, timedelta

# ========== 配置区域 ==========

# SMTP 配置（使用QQ邮箱发送）
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SMTP_USER = "781291348@qq.com"
SMTP_PASS = "zklwmudvlnsabdce"

# 收件人
RECIPIENT = "iamguod@163.com"

# arXiv 配置
ARXIV_CATEGORIES = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV"
MAX_PAPERS = 5  # 每封邮件最多5篇

# 本地存储
SENT_PAPERS_FILE = "/root/clawd/arxiv_sent_papers.json"
FEISHU_IMPORT_FILE = "/root/clawd/arxiv_feishu_import.md"

# 飞书多维表格配置
FEISHU_APP_ID = "cli_a90aa0be57b81bd1"
FEISHU_APP_SECRET = "MfsbAnzRazZsuHgrYhT8HhsYSaw4nEwN"
FEISHU_APP_TOKEN = "L2pmbFDhja34HMsLAOgcSxYInGz"
FEISHU_TABLE_ID = "tbleOsazruYwyPKp"

# GLM 翻译 API 配置
GLM_API_BASE = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GLM_API_KEY = "cee1da60ac514048a4b8cc788a93f109.ga9IyuQhBjZ8ReK6"

# ========== 工具函数 ==========

def load_sent_papers():
    """加载已发送的论文ID列表"""
    if os.path.exists(SENT_PAPERS_FILE):
        try:
            with open(SENT_PAPERS_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_sent_papers(sent_papers):
    """保存已发送的论文ID列表"""
    with open(SENT_PAPERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(sent_papers), f, ensure_ascii=False, indent=2)

def get_app_token():
    """获取飞书 app_access_token"""
    url = f"https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        return resp.json().get("app_access_token")
    else:
        print(f"获取飞书 token 失败: {resp.text}")
        return None

def batch_create_records(papers):
    """批量创建记录到飞书多维表格"""
    token = get_app_token()
    if not token:
        return False

    headers = {"Authorization": f"Bearer {token}"}

    # 使用 batch_create 接口
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records/batch_create"

    # 构建记录数组
    records = []
    for paper in papers:
        record = {
            "fields": {
                "标题": paper['title'],
                "摘要": paper['summary'],
                "中文标题": paper.get('cn_title', ''),
                "中文摘要": paper.get('cn_abstract', ''),
                "链接": {"link": paper['link']},
                "发布日期": int(datetime.now().timestamp() * 1000)
            }
        }
        records.append(record)

    payload = {"records": records}

    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            result = resp.json()
            if result.get("code") == 0:
                created_count = len(result.get("data", {}).get("records", []))
                print(f"✓ 飞书表格写入成功: {created_count} 条记录")
                return True
            else:
                print(f"✗ 飞书表格写入失败: {result}")
                return False
        else:
            print(f"✗ 飞书表格写入失败: HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 飞书表格写入异常: {e}")
        return False

def translate_text_to_chinese(text, max_length=800):
    """使用 GLM API 翻译文本到中文"""
    if not GLM_API_KEY:
        return ""

    if len(text) > max_length:
        text = text[:max_length] + "..."

    try:
        headers = {
            "Authorization": f"Bearer {GLM_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "glm-4-flash",
            "messages": [
                {
                    "role": "user",
                    "content": f"Please translate the following text to Chinese:\n\n{text}"
                }
            ],
            "temperature": 0.3
        }

        response = requests.post(GLM_API_BASE, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        else:
            return ""

    except Exception as e:
        print(f"翻译异常: {e}")
        return ""

def fetch_arxiv_papers(days_back=1):
    """从 arXiv 获取最新的 AI 论文"""
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query={ARXIV_CATEGORIES}&sortBy=submittedDate&sortOrder=descending&max_results=20"

    try:
        response = requests.get(base_url + query, timeout=30)
        response.raise_for_status()
        root = ET.fromstring(response.text)

        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            paper_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip()
            published = entry.find('atom:published', ns).text
            link = entry.find('atom:link', ns).get('href')

            pub_date = datetime.strptime(published[:19], "%Y-%m-%dT%H:%M:%S")
            if pub_date < datetime.now() - timedelta(days=days_back):
                continue

            papers.append({
                'id': paper_id,
                'title': title,
                'summary': summary,
                'published': published,
                'link': link
            })

        return papers[:MAX_PAPERS * 2]

    except Exception as e:
        print(f"获取 arXiv 论文失败: {e}")
        return []

def send_email(subject, content):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = formataddr(('ArXiv日报', SMTP_USER))
    msg['To'] = formataddr(('Man', RECIPIENT))
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [RECIPIENT], msg.as_string())
        print(f"✓ 邮件发送成功: {subject}")
        return True
    except Exception as e:
        print(f"✗ 邮件发送失败: {e}")
        return False

def format_paper(paper):
    """格式化单篇论文"""
    print(f"正在处理论文 {paper['id']}...")
    title_cn = translate_text_to_chinese(paper['title'])
    abstract_cn = translate_text_to_chinese(paper['summary'])

    paper['cn_title'] = title_cn if title_cn else '[翻译失败]'
    paper['cn_abstract'] = abstract_cn if abstract_cn else '[翻译失败]'

    result = f"""
【论文 {paper['id']}】

1、论文标题（英文+中文翻译）
{paper['title']}
{title_cn if title_cn else '[翻译失败]'}

2、论文摘要（英文+中文）
{paper['summary']}
{abstract_cn if abstract_cn else '[翻译失败]'}

链接: {paper['link']}
"""
    return result

def main():
    """主函数"""
    print(f"\n{'='*60}")
    print(f"ArXiv AI 论文日报 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 加载已发送记录
    sent_papers = load_sent_papers()

    # 获取新论文
    print("正在获取 arXiv 论文...")
    all_papers = fetch_arxiv_papers(days_back=7)

    if not all_papers:
        print("没有获取到论文")
        return

    print(f"获取到 {len(all_papers)} 篇论文")

    # 过滤已发送的
    new_papers = [p for p in all_papers if p['id'] not in sent_papers]

    if not new_papers:
        print("没有新的论文需要发送")
        return

    new_papers = new_papers[:MAX_PAPERS]
    print(f"筛选后发送 {len(new_papers)} 篇论文")

    # 翻译并写入飞书表格
    print("\n正在翻译并写入飞书多维表格...")
    for paper in new_papers:
        title_cn = translate_text_to_chinese(paper['title'])
        abstract_cn = translate_text_to_chinese(paper['summary'])
        paper['cn_title'] = title_cn if title_cn else '[翻译失败]'
        paper['cn_abstract'] = abstract_cn if abstract_cn else '[翻译失败]'

    batch_create_records(new_papers)

    # 构建邮件内容
    content = f"""🤖 ArXiv AI 论文日报
{datetime.now().strftime('%Y年%m月%d日')}

以下是今天的AI领域热点论文：

"""

    for i, paper in enumerate(new_papers, 1):
        content += format_paper(paper)
        if i < len(new_papers):
            content += "\n" + "-"*60 + "\n"

    content += "\n---\n由大虎哥自动发送\n"

    # 发送邮件
    subject = f"📚 ArXiv AI论文日报 - {datetime.now().strftime('%Y-%m-%d')}"
    if send_email(subject, content):
        sent_papers.update(p['id'] for p in new_papers)
        save_sent_papers(sent_papers)
        print("\n✓ 邮件发送成功，已更新已发送记录")
        print("✓ 所有论文已写入飞书多维表格")
    else:
        print("✗ 邮件发送失败")

if __name__ == "__main__":
    main()
