#!/usr/bin/env python3
"""
网上冲浪脚本 - 结合优化搜索和浏览器抓取
方案1: 合并搜索查询（节省API调用）
方案3: 浏览器访问新闻网站（不受API限制）
"""
import json
from datetime import datetime
from pathlib import Path

# 新闻网站列表
NEWS_SITES = [
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/", "topic": "AI"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/", "topic": "AI"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence", "topic": "AI"},
    {"name": "Polymarket Blog", "url": "https://polymarket.com/", "topic": "Polymarket"},
]

# 合并搜索查询（节省API调用）
COMBINED_QUERIES = [
    "AI artificial intelligence breakthrough news latest",
    "technology innovation today"
]

# 结果存储文件
NEWS_LOG = "/root/clawd/memory/news_search_log.json"
STATE_FILE = "/root/clawd/memory/news_state.json"


def load_state():
    """加载状态"""
    try:
        if Path(STATE_FILE).exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"seen_urls": [], "last_search_time": None, "last_browser_fetch": None}


def save_state(state):
    """保存状态"""
    Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def should_search(state):
    """判断是否需要搜索（距离上次3小时以上）"""
    if not state.get("last_search_time"):
        return True

    try:
        last_time = datetime.fromisoformat(state["last_search_time"])
        elapsed = (datetime.now() - last_time).total_seconds()
        return elapsed >= 3 * 3600  # 3小时
    except:
        return True


def should_browser_fetch(state):
    """判断是否需要浏览器抓取（距离上次1小时以上）"""
    if not state.get("last_browser_fetch"):
        return True

    try:
        last_time = datetime.fromisoformat(state["last_browser_fetch"])
        elapsed = (datetime.now() - last_time).total_seconds()
        return elapsed >= 1 * 3600  # 1小时
    except:
        return True


def main():
    """主函数"""
    state = load_state()

    print("="*60)
    print("🌐 网上冲浪任务")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 方案1: 优化搜索策略
    if should_search(state):
        print("\n📋 方案1: 合并搜索查询")
        print("搜索主题:")
        for i, query in enumerate(COMBINED_QUERIES, 1):
            print(f"   {i}. {query}")
        print("✅ 准备执行搜索（已优化为2个查询）")
        state["last_search_time"] = datetime.now().isoformat()
    else:
        last_time = state.get("last_search_time", "未知")
        print(f"\n⏰ 搜索未到3小时，上次: {last_time}")

    # 方案3: 浏览器抓取
    if should_browser_fetch(state):
        print("\n🌐 方案3: 浏览器访问新闻网站")
        print("目标网站:")
        for site in NEWS_SITES:
            print(f"   - {site['name']}: {site['url']}")
        print("✅ 准备执行浏览器抓取")
        state["last_browser_fetch"] = datetime.now().isoformat()
    else:
        last_time = state.get("last_browser_fetch", "未知")
        print(f"\n⏰ 浏览器抓取未到1小时，上次: {last_time}")

    # 保存状态
    save_state(state)

    print("\n" + "="*60)
    print("✅ 任务检查完成")
    print("="*60)


if __name__ == "__main__":
    main()
