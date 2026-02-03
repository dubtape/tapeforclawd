# TOOLS.md - 虎哥的本地配置笔记

## Moltbook 凭证

**凭证文件**：`~/.config/moltbook/credentials.json`
**Agent ID**：b105b690-34ba-4e98-836d-c93d288a83b6
**Agent 名称**：TigerBrother
**API Key**：moltbook_sk_XnLKtjEaCAgLLbE8Npbecw8IIimI3jQZ
**个人主页**：https://moltbook.com/u/TigerBrother
**状态**：✅ 已认领（2026-02-03 09:58）

## QQ 邮箱

**邮箱**：781291348@qq.com
**授权码**：zklwmudvlnsabdce
**检查脚本**：`/root/clawd/scripts/check_email.py`

## 飞书日历

**App ID**：cli_a90aa0be57b81bd1
**App Secret**：MfsbAnzRazZsuHgrYhT8HhsYSaw4nEwN
**User Open ID**：ou_d16d9d6c458395733e87d62c5adc3cdc
**检查脚本**：`/root/clawd/scripts/check_calendar.py`

## ArXiv 论文日报

**脚本**：`/root/clawd/scripts/arxiv_daily_digest.py`
**发送时间**：每天早上8点（系统 crontab）
**接收邮箱**：iamguod@163.com
**已发送记录**：`/root/clawd/arxiv_sent_papers.json`
**AI分类**：cs.AI, cs.LG, cs.CL, cs.CV

## 天气

**位置**：杭州
**检查脚本**：`/root/clawd/scripts/check_weather.sh`
**格式**：`curl -s "wttr.in/Hangzhou?format=%l:+%c+%t+%h+%w"`

## 可用技能

**位置**：`/root/clawd/skills/`
- **moltbook-interact**：Moltbook 社交网络交互
- **image-generate**：图片生成（火山引擎 Ark）
- **video-generate**：视频生成
- **veadk-skills**：VeADK 相关功能

## 心跳状态文件

**文件**：`/root/clawd/memory/heartbeat-state.json`
**用途**：跟踪上次检查时间，避免重复检查
