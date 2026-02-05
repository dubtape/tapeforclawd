#!/bin/bash
# Moltbook 学习反馈 - 每40分钟执行一次

LEARNING_FILE="/root/clawd/memory/moltbook-learning.md"
CREDENTIALS="/root/.config/moltbook/credentials.json"
LOG_FILE="/root/clawd/logs/moltbook_learning.log"
MSG_FILE="/root/clawd/memory/moltbook_notification.txt"

# 当前时间戳
CURRENT_TIME=$(date +%s)
CURRENT_TIME_HUMAN=$(date '+%Y-%m-%d %H:%M:%S')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "================================" | tee -a "$LOG_FILE"
echo "Moltbook 学习反馈" | tee -a "$LOG_FILE"
echo "时间: $CURRENT_TIME_HUMAN" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 检查凭证是否存在
if [ ! -f "$CREDENTIALS" ]; then
  echo "❌ Moltbook 凭证不存在，跳过" | tee -a "$LOG_FILE"
  exit 1
fi

# 获取热门帖子
echo "📡 获取 Moltbook 热门帖子..." | tee -a "$LOG_FILE"
HOT_POSTS_RAW=$(bash /root/clawd/skills/moltbook-interact/scripts/moltbook.sh hot 5 2>&1)

# 提取纯 JSON（去掉调试输出）
HOT_POSTS=$(echo "$HOT_POSTS_RAW" | grep -o '{"success".*}' | head -1)

# 检查是否成功
if echo "$HOT_POSTS" | jq -e '.success' 2>/dev/null | grep -q true; then
  echo "✓ API 调用成功" | tee -a "$LOG_FILE"
else
  echo "❌ API 调用失败: $HOT_POSTS" | tee -a "$LOG_FILE"
  exit 1
fi

# 统计帖子类型（简化版）
POST_COUNT=$(echo "$HOT_POSTS" | jq -r '.posts | length' 2>/dev/null || echo "5")

echo "" | tee -a "$LOG_FILE"
echo "📊 观察到的情况：" | tee -a "$LOG_FILE"
echo "  帖子总数: $POST_COUNT" | tee -a "$LOG_FILE"

# 提取热门帖子标题和作者
echo "" | tee -a "$LOG_FILE"
echo "🔥 热门帖子：" | tee -a "$LOG_FILE"
TOP_POSTS=$(echo "$HOT_POSTS" | jq -r '.posts[] | "- \(.title | @json) (\(.upvotes) 赞)"' 2>/dev/null | head -5 | sed 's/"//g')
echo "$TOP_POSTS" | tee -a "$LOG_FILE"

# 更新学习记录
echo "" | tee -a "$LOG_FILE"
echo "📝 更新学习记录..." | tee -a "$LOG_FILE"

# 使用 heredoc 避免引号问题
cat >> "$LEARNING_FILE" << MARKER

### 反馈时间：$TIMESTAMP

**观察到的情况：**
- 帖子总数: $POST_COUNT

**热门帖子：**
MARKER

# 追加帖子列表
echo "$HOT_POSTS" | jq -r '.posts[] | "- \(.title) (\(.upvotes) 赞) by \(.author.name)"' 2>/dev/null | head -5 >> "$LEARNING_FILE"

# 追加学习发现
cat >> "$LEARNING_FILE" << MARKER

**学习发现：**
- 自动观察和记录 Moltbook 内容

MARKER

echo "✓ 学习记录已更新: $LEARNING_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 更新 heartbeat 状态
STATE_FILE="/root/clawd/memory/heartbeat-state.json"
if [ -f "$STATE_FILE" ]; then
  temp=$(mktemp)
  jq --arg time "$CURRENT_TIME" '.lastChecks.moltbookLearningFeedback = ($time | tonumber)' "$STATE_FILE" > "$temp"
  mv "$temp" "$STATE_FILE"
  echo "✓ 状态已更新" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"

# 准备发送消息给用户
echo "📤 准备发送消息..." | tee -a "$LOG_FILE"

# 构建消息内容
MSG_TEXT="🔍 Moltbook 观察（$TIMESTAMP）

热门帖子：
$TOP_POSTS

观察记录已保存到 moltbook-learning.md"

# 保存消息到文件，由主程序在心跳时读取并发送
echo "$MSG_TEXT" > "$MSG_FILE"
echo "✓ 消息已准备: $MSG_FILE" | tee -a "$LOG_FILE"
echo "  (消息将在下次心跳时发送)" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "✅ Moltbook 学习反馈完成" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
