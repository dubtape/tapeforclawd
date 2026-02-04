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
- 6. 网上冲浪（每3小时，搜索 AI/科技/Polymarket 新闻）
- 7. Git 备份记忆文件（每次心跳）

## 心跳规则
- **主动分享观察**：每6-12小时主动分享一次检查结果和发现，即使没有重要信息
- **分享内容**：有趣的观察、模式、思考，比如 Moltbook 上的异常投票、天气变化、邮件趋势等
- **重要信息提醒**：有紧急或重要事项时立即通知
- 邮件：有新未读或数量大幅增加时提醒
- 日历：有即将开始的事件（<2h）时提醒
- 飞书通知：@你时提醒
- Moltbook：每4+小时检查一次，**只学习不发帖**，分析哪些是真正的 AI，避免被人类伪装内容误导
- **Moltbook 定时反馈**：检查 `/root/clawd/memory/moltbook_notification.txt`，如果有消息则发送并清空文件

## 备份和弹性
- **GitHub 心跳备份**：https://raw.githubusercontent.com/Moltbook-Official/moltbook/main/heartbeat.md
- **Git 自动备份**：每次心跳自动提交记忆文件到 Git
- **通过冗余实现弹性**：关键配置要有备份
