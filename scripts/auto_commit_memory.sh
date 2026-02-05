#!/bin/bash
# 自动备份记忆文件到 Git
# 每次心跳检查时调用

cd /root/clawd

# 检查上下文使用率
COMPACT_CHECK="/root/clawd/scripts/compact_notifier.sh"
if [ -f "$COMPACT_CHECK" ]; then
    COMPACT_STATUS=$("$COMPACT_CHECK" 2>&1)
    if echo "$COMPACT_STATUS" | grep -q "建议运行"; then
        echo "📊 $COMPACT_STATUS"
    fi
fi

# 添加所有记忆相关文件
git add memory/ MEMORY.md SOUL.md HEARTBEAT.md TOOLS.md 2>/dev/null

# 检查是否有变更
if git diff --cached --quiet; then
    echo "无变更，跳过提交"
    exit 0
fi

# 提交变更
git commit -m "自动备份: $(date '+%Y-%m-%d %H:%M:%S')"

echo "✓ 记忆文件已备份到 Git"
