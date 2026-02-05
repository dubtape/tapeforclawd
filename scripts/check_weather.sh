#!/bin/bash
# 检查天气 - 杭州
CITY="杭州"
echo "🌤️ $CITY 天气:"
curl -s "wttr.in/${CITY}?format=%l:+%c+%t+%h+%w" && echo
curl -s "wttr.in/${CITY}?format=今天:%C+最高%t+最低%t+降水%p" && echo
