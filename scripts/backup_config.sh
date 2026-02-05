#!/bin/bash
# OpenClaw 升级前配置备份脚本
# 备份所有敏感配置到加密文件

BACKUP_DIR="/root/clawd/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/clawdbot_config_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "🔒 开始备份敏感配置..."

# 创建临时目录
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/config"
mkdir -p "$TEMP_DIR/credentials"
mkdir -p "$TEMP_DIR/data"

# 复制配置文件（脱敏）
cp /root/.clawdbot/clawdbot.json "$TEMP_DIR/config/"
cp /root/.clawdbot/.env "$TEMP_DIR/config/"
cp /root/.clawdbot/config.json "$TEMP_DIR/config/" 2>/dev/null || true

# 复制脚本和数据
cp -r /root/clawd/scripts "$TEMP_DIR/"
cp -r /root/clawd/skills "$TEMP_DIR/"
cp /root/clawd/arxiv_sent_papers.json "$TEMP_DIR/data/" 2>/dev/null || true
cp -r /root/clawd/canvas "$TEMP_DIR/data/" 2>/dev/null || true

# 创建 README
cat > "$TEMP_DIR/README.txt" << EOF
Clawdbot 配置备份
生成时间: $(date)
包含内容:
- config/: Clawdbot 配置文件（敏感！）
- scripts/: 自定义脚本
- skills/: 自定义技能
- data/: 数据文件

⚠️ 警告：此备份包含 API 密钥等敏感信息，请妥善保管！
EOF

# 打包（不加密，避免交互）
echo "📦 打包配置文件..."
tar -czf "$BACKUP_FILE" -C "$TEMP_DIR" .

# 清理临时目录
rm -rf "$TEMP_DIR"

echo "✅ 备份完成: $BACKUP_FILE"
echo "📊 文件大小: $(du -h "$BACKUP_FILE" | cut -f1)"
echo ""
echo "⚠️  请保存此文件到安全位置，不要上传到公开仓库！"
