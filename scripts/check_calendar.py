#!/usr/bin/env python3
"""
检查飞书日历事件
"""
import requests
import json
from datetime import datetime, timedelta

# 飞书应用配置
APP_ID = "cli_a90aa0be57b81bd1"
APP_SECRET = "MfsbAnzRazZsuHgrYhT8HhsYSaw4nEwN"
USER_OPEN_ID = "ou_d16d9d6c458395733e87d62c5adc3cdc"

FEISHU_BASE_URL = "https://open.feishu.cn/open-apis"

def get_tenant_token():
    """获取 tenant_access_token"""
    url = f"{FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    resp = requests.post(url, json=payload)
    data = resp.json()
    if data.get("code") == 0:
        return data.get("tenant_access_token")
    return None

def get_primary_calendar_id(token):
    """获取主日历ID"""
    url = f"{FEISHU_BASE_URL}/calendar/v4/calendars"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "user_id_type": "open_id",
        "page_size": 50
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    if data.get("code") == 0:
        calendars = data.get("data", {}).get("calendar_list", [])
        for cal in calendars:
            if cal.get("type") == "primary":
                return cal.get("calendar_id")
    return None

def get_calendar_events(token, days=2):
    """获取未来几天的事件"""
    calendar_id = get_primary_calendar_id(token)
    if not calendar_id:
        return None

    url = f"{FEISHU_BASE_URL}/calendar/v4/calendars/{calendar_id}/events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 计算时间范围（毫秒时间戳）
    now = datetime.now()
    start_time = int(now.timestamp() * 1000)
    end_time = int((now + timedelta(days=days)).timestamp() * 1000)

    params = {
        "page_size": 50,
        "time_min": start_time,
        "time_max": end_time
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    if data.get("code") == 0:
        events = data.get("data", {}).get("items", [])
        return events
    else:
        return None

def check_calendar():
    """检查日历"""
    token = get_tenant_token()
    if not token:
        return {"error": "获取 token 失败"}

    events = get_calendar_events(token)
    if events is None:
        return {"error": "获取日历事件失败"}

    if not events:
        return {"event_count": 0, "events": []}

    formatted_events = []
    for e in events:
        title = e.get("summary", "无标题")
        start = e.get("start_time", {})
        end = e.get("end_time", {})

        # 处理时间
        if "datetime" in start:
            start_time_str = start["datetime"][:16].replace("T", " ")
        else:
            start_time_str = "全天"

        formatted_events.append({
            "title": title,
            "start_time": start_time_str,
        })

    return {
        "event_count": len(formatted_events),
        "events": formatted_events
    }

if __name__ == '__main__':
    result = check_calendar()
    if 'error' in result:
        print(f'日历检查失败: {result["error"]}')
    else:
        count = result['event_count']
        print(f'📅 未来2天有 {count} 个日程')
        for i, e in enumerate(result['events'][:5], 1):
            print(f'  {i}. {e["title"]} - {e["start_time"]}')
