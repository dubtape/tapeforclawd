#!/bin/bash
# 自动检查并在需要时建议 compact
# 在心跳前调用

MEMORY_DIR="/root/clawd/memory"
THRESHOLD_TOKENS=60000  # 60k tokens 时建议 compact
STATUS_FILE="$MEMORY_DIR/context-status.json"

# 检查上下文使用情况（通过 clawdbot sessions list）
CONTEXT_INFO=$(clawdbot sessions list 2>/dev/null | grep -A 1 "agent:main:main" | grep "totalTokens" | head -1)

if [ -z "$CONTEXT_INFO" ]; then
    echo "无法获取上下文信息"
    exit 0
fi

# 提取 token 数量（简化的解析）
TOKENS=$(echo "$CONTEXT_INFO" | grep -oP 'totalTokens":\s*\K\d+' || echo "0")

# 记录状态
cat > "$STATUS_FILE" << EOF
{
  "lastCheck": "$(date -Iseconds)",
  "estimatedTokens": $TOKENS,
  "threshold": $THRESHOLD_TOKENS,
  "needsCompact": $([ $TOKENS -gt $THRESHOLD_TOKENS ] && echo "true" || echo "false")
}
EOF

# 如果超过阈值，提醒用户
if [ "$TOKENS" -gt "$THRESHOLD_TOKENS" ]; then
    echo "⚠️  上下文较大: ~$TOKENS tokens"
    echo "建议运行 /compact 清理"
fi

exit 0
