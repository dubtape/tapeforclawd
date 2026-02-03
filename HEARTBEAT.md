# HEARTBEAT.md

定期检查任务（每次心跳执行2-4项，轮换）

**每次心跳开始时先运行**：
```bash
/root/clawd/scripts/auto_commit_memory.sh  # Git 备份记忆文件
```

## 执行顺序（轮换）
- 1. 检查邮件（QQ邮箱未读）
- 2. 检查天气（杭州）
- 3. 检查飞书日历（未来2天日程）
- 4. 检查飞书通知（@提及）
- 5. 检查 Moltbook（每4+小时，查看新帖子、通知）
- 6. **Moltbook 学习反馈**（每40分钟，分享学到了什么）
- 7. Git 备份记忆文件（每次心跳）

## 心跳规则
- 只在有重要信息时主动通知
- 邮件：有新未读或数量大幅增加时提醒
- 日历：有即将开始的事件（<2h）时提醒
- 飞书通知：@你时提醒
- Moltbook：每4+小时检查一次，**只学习不发帖**，分析哪些是真正的 AI，避免被人类伪装内容误导
- **Moltbook 学习反馈**：每40分钟主动分享学到的东西，记录到 `memory/moltbook-learning.md`

## 备份和弹性
- **GitHub 心跳备份**：https://raw.githubusercontent.com/Moltbook-Official/moltbook/main/heartbeat.md
- **Git 自动备份**：每次心跳自动提交记忆文件到 Git
- **通过冗余实现弹性**：关键配置要有备份
