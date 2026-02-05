#!/bin/bash
# 检查是否需要 Moltbook 学习反馈

HEARTBEAT_STATE="/root/clawd/memory/heartbeat-state.json"
LEARNING_FILE="/root/clawd/memory/moltbook-learning.md"

# 获取当前时间和上次反馈时间
CURRENT_TIME=$(date +%s)
LAST_FEEDBACK=$(grep "moltbookLearningFeedback" "$HEARTBEAT_STATE" | grep -o '[0-9]*' | head -1)

# 如果没有记录，使用当前时间
if [ -z "$LAST_FEEDBACK" ]; then
  LAST_FEEDBACK=$CURRENT_TIME
fi

# 计算时间差（秒）
TIME_DIFF=$((CURRENT_TIME - LAST_FEEDBACK))
# 40分钟 = 2400秒
SHOULD_FEEDBACK=$((TIME_DIFF >= 2400))

if [ $SHOULD_FEEDBACK -eq 1 ]; then
  echo "⏰ 到了 Moltbook 学习反馈时间！"
  echo "距离上次反馈：$((TIME_DIFF / 60)) 分钟"
  echo ""
  echo "请运行：bash /root/clawd/skills/moltbook-interact/scripts/moltbook.sh hot 5"
  echo "然后更新 $LEARNING_FILE"
else
  echo "✓ 还未到反馈时间"
  echo "距离上次反馈：$((TIME_DIFF / 60)) 分钟 / 40 分钟"
fi

exit $SHOULD_FEEDBACK
