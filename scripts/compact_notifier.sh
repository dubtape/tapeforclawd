#!/bin/bash
# 上下文使用率检查和提醒脚本

# 解析 clawdbot sessions list 的表格输出
LINE=$(clawdbot sessions list 2>&1 | grep "direct agent:main:main" | grep "glm-4.7")

if [ -z "$LINE" ]; then
    echo "❌ 无法获取会话信息"
    exit 1
fi

# 解析 token 信息，格式如: "2.0k/205k (1%)"
TOKENS_STR=$(echo "$LINE" | grep -oP '\d+[kK]?/\d+[kK]? \(\d+%\)' | head -1)

if [ -z "$TOKENS_STR" ]; then
    echo "❌ 无法解析 token 信息"
    exit 1
fi

# 提取百分比
PERCENT=$(echo "$TOKENS_STR" | grep -oP '\(\K\d+(?=%\))')

THRESHOLD=60  # 60% 时提醒

if [ "$PERCENT" -gt "$THRESHOLD" ]; then
    echo "⚠️ 上下文使用率: $PERCENT% ($TOKENS_STR)"
    echo "🧹 建议运行 /compact 清理对话历史"
    exit 1
else
    echo "✅ 上下文正常: $PERCENT% ($TOKENS_STR)"
    exit 0
fi
