#!/bin/bash
# 服务器初始化脚本
# 在服务器上运行此脚本进行首次部署设置

set -e

echo "========================================================================"
echo "  Pricelist 服务器初始化"
echo "========================================================================"
echo ""

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用root用户或sudo运行此脚本"
    exit 1
fi

# 更新系统
echo "📦 更新系统包..."
apt-get update
apt-get upgrade -y

# 安装必要的软件
echo "📦 安装必要软件..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    supervisor \
    wget \
    curl

# 安装Playwright依赖
echo "📦 安装Playwright浏览器依赖..."
apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# 创建项目目录
echo "📁 创建项目目录..."
mkdir -p /var/www/pricelist/{current,releases}
mkdir -p /var/log/pricelist

# 创建www-data用户（如果不存在）
if ! id "www-data" &>/dev/null; then
    useradd -r -s /bin/bash www-data
fi

# 克隆代码
echo "📥 克隆代码仓库..."
cd /var/www/pricelist/current
if [ ! -d ".git" ]; then
    git clone https://github.com/yalding8/pricelist.git .
else
    git pull origin main
fi

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install python-dotenv gunicorn

# 安装Playwright浏览器
echo "🎭 安装Playwright浏览器..."
python -m playwright install chromium

# 创建环境变量文件
echo "⚙️  创建环境变量文件..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    # 生成随机SECRET_KEY
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    sed -i "s/your-secret-key-here-change-this-in-production/$SECRET_KEY/" .env
    echo "✅ .env 文件已创建，请手动编辑配置"
fi

# 设置权限
echo "🔒 设置文件权限..."
chown -R www-data:www-data /var/www/pricelist
chown -R www-data:www-data /var/log/pricelist
chmod -R 755 /var/www/pricelist

# 安装systemd服务
echo "⚙️  安装systemd服务..."
cp deploy/pricelist.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable pricelist

# 配置nginx
echo "🌐 配置Nginx..."
cp deploy/nginx.conf /etc/nginx/sites-available/pricelist
ln -sf /etc/nginx/sites-available/pricelist /etc/nginx/sites-enabled/
nginx -t

# 启动服务
echo "🚀 启动服务..."
systemctl start pricelist
systemctl restart nginx

# 显示状态
echo ""
echo "========================================================================"
echo "✅ 服务器初始化完成！"
echo "========================================================================"
echo ""
echo "📊 服务状态:"
systemctl status pricelist --no-pager
echo ""
echo "🌐 Nginx状态:"
systemctl status nginx --no-pager
echo ""
echo "========================================================================"
echo "📝 后续步骤:"
echo ""
echo "1. 配置DNS:"
echo "   将 price.pylosy.com 指向服务器IP"
echo ""
echo "2. 安装SSL证书:"
echo "   sudo certbot --nginx -d price.pylosy.com"
echo ""
echo "3. 配置GitHub Secrets:"
echo "   SERVER_HOST: 服务器IP或域名"
echo "   SERVER_USER: www-data"
echo "   SSH_PRIVATE_KEY: SSH私钥"
echo "   SERVER_PORT: 22"
echo ""
echo "4. 测试访问:"
echo "   http://price.pylosy.com"
echo ""
echo "5. 查看日志:"
echo "   sudo journalctl -u pricelist -f"
echo "   sudo tail -f /var/log/pricelist/error.log"
echo ""
echo "========================================================================"
