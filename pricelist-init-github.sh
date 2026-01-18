#!/bin/bash

# pricelist GitHub仓库初始化脚本
# 使用方法: bash pricelist-init-github.sh

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  pricelist GitHub仓库初始化脚本"
echo "========================================"
echo ""

# 1. 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ 错误: 未安装Git，请先安装Git${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git已安装${NC}"

# 2. 设置变量
VAULT_PATH="/Users/ningding/Documents/Obsidian Vault"
PROJECT_NAME="pricelist"
GITHUB_REPO="https://github.com/yalding8/pricelist.git"

# 询问用户项目路径
echo ""
echo "📁 请输入项目创建路径（默认: ~/Projects）:"
read -r PROJECT_ROOT
if [ -z "$PROJECT_ROOT" ]; then
    PROJECT_ROOT="$HOME/Projects"
fi

PROJECT_PATH="$PROJECT_ROOT/$PROJECT_NAME"

echo -e "${YELLOW}项目将创建在: $PROJECT_PATH${NC}"
echo ""

# 3. 创建项目目录结构
echo "📦 创建项目目录结构..."

mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

# 创建目录
mkdir -p config
mkdir -p core
mkdir -p generator/templates/assets
mkdir -p scrapers
mkdir -p api
mkdir -p web/{static,templates}
mkdir -p data/cache
mkdir -p tests
mkdir -p docs
mkdir -p examples
mkdir -p output

echo -e "${GREEN}✅ 目录结构创建完成${NC}"

# 4. 复制文件
echo ""
echo "📝 从Obsidian Vault复制文件..."

# 检查Vault路径是否存在
if [ ! -d "$VAULT_PATH" ]; then
    echo -e "${RED}❌ 错误: Vault路径不存在: $VAULT_PATH${NC}"
    exit 1
fi

# 复制文件
cp "$VAULT_PATH/pricelist-README.md" "README.md"
cp "$VAULT_PATH/pricelist-requirements.txt" "requirements.txt"
cp "$VAULT_PATH/pricelist-models.py" "core/models.py"
cp "$VAULT_PATH/pricelist-brand_config.py" "config/brand.py"
cp "$VAULT_PATH/pricelist-gift_library.yaml" "config/gift_library.yaml"
cp "$VAULT_PATH/pricelist-quote_template.html" "generator/templates/quote_card.html"
cp "$VAULT_PATH/pricelist-使用示例.py" "examples/basic_usage.py"

echo -e "${GREEN}✅ 文件复制完成${NC}"

# 5. 创建.gitignore
echo ""
echo "📄 创建.gitignore..."

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# 数据库
*.db
*.sqlite3

# 环境变量
.env
.env.local

# 缓存
data/cache/
*.log
logs/

# 生成的文件
output/
data/quotes/
*.png
*.html

# 测试
.pytest_cache/
.coverage
htmlcov/

# 文档
docs/_build/
EOF

echo -e "${GREEN}✅ .gitignore创建完成${NC}"

# 6. 创建.env.example
echo ""
echo "📄 创建.env.example..."

cat > .env.example << 'EOF'
# 应用配置
APP_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=8000

# 品牌配置
BRAND_COLOR=#FF5A5F
LOGO_URL=

# 数据库
DATABASE_URL=sqlite:///data/quotes.db

# 爬虫配置
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
SCRAPER_TIMEOUT=30

# 报价单配置
QUOTE_DEFAULT_VALID_DAYS=7
QUOTE_IMAGE_WIDTH=750
QUOTE_IMAGE_QUALITY=90
EOF

echo -e "${GREEN}✅ .env.example创建完成${NC}"

# 7. 创建空的__init__.py
echo ""
echo "📄 创建__init__.py..."

touch core/__init__.py
touch config/__init__.py
touch generator/__init__.py
touch scrapers/__init__.py
touch api/__init__.py
touch tests/__init__.py

echo -e "${GREEN}✅ __init__.py创建完成${NC}"

# 8. Git初始化
echo ""
echo "🔧 初始化Git仓库..."

git init
git branch -M main

echo -e "${GREEN}✅ Git仓库初始化完成${NC}"

# 9. 添加远程仓库
echo ""
echo "🔗 添加远程仓库..."

# 检查GitHub仓库是否存在（需要手动确认）
echo -e "${YELLOW}⚠️  请确保已在GitHub创建仓库: $GITHUB_REPO${NC}"
echo "按Enter继续，或Ctrl+C取消..."
read -r

git remote add origin "$GITHUB_REPO"

echo -e "${GREEN}✅ 远程仓库添加完成${NC}"

# 10. 首次提交
echo ""
echo "💾 创建首次提交..."

git add .
git commit -m "Initial commit: pricelist project setup

- 核心数据模型（房源、优惠、礼品库）
- 品牌配置（异乡好居品牌规范）
- 礼品库配置（15种礼品）
- HTML报价单模板
- 使用示例代码
- 项目文档

Created with Claude Code (Claudian plugin)"

echo -e "${GREEN}✅ 首次提交完成${NC}"

# 11. 询问是否推送
echo ""
echo "🚀 是否要推送到GitHub? (y/n)"
read -r PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then
    echo "推送到GitHub..."
    git push -u origin main
    echo -e "${GREEN}✅ 推送完成${NC}"
else
    echo -e "${YELLOW}⚠️  跳过推送，您可以稍后手动执行: git push -u origin main${NC}"
fi

# 12. 完成
echo ""
echo "========================================"
echo -e "${GREEN}✅ 项目初始化完成！${NC}"
echo "========================================"
echo ""
echo "📁 项目路径: $PROJECT_PATH"
echo ""
echo "🚀 下一步操作:"
echo "  1. cd $PROJECT_PATH"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. python examples/basic_usage.py"
echo ""
echo "📖 查看文档: cat README.md"
echo ""
echo "🎉 祝您使用愉快！"
