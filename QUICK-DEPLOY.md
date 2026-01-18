# ⚡ 快速部署命令

最常用的部署命令速查。

---

## 🚀 首次部署到GitHub

```bash
# 1. 初始化仓库
git init
git add .
git commit -m "Initial commit"
git branch -M main

# 2. 关联远程仓库
git remote add origin https://github.com/yalding8/pricelist.git
git push -u origin main

# 3. 生成SSH密钥
ssh-keygen -t ed25519 -C "deploy" -f ~/.ssh/pricelist_deploy

# 4. 查看公钥（添加到服务器）
cat ~/.ssh/pricelist_deploy.pub

# 5. 查看私钥（添加到GitHub Secrets）
cat ~/.ssh/pricelist_deploy
```

---

## 🖥️ 服务器快速初始化

```bash
# 一键初始化（推荐）
wget https://raw.githubusercontent.com/yalding8/pricelist/main/deploy/setup-server.sh
chmod +x setup-server.sh
sudo ./setup-server.sh
```

或手动执行：

```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git nginx

# 创建目录
sudo mkdir -p /var/www/pricelist/{current,releases}
sudo mkdir -p /var/log/pricelist

# 克隆代码
cd /var/www/pricelist/current
sudo git clone https://github.com/yalding8/pricelist.git .

# 安装Python依赖
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
sudo venv/bin/python -m playwright install chromium

# 配置环境变量
sudo cp .env.example .env
sudo nano .env

# 设置权限
sudo chown -R www-data:www-data /var/www/pricelist
sudo chown -R www-data:www-data /var/log/pricelist

# 安装服务
sudo cp deploy/pricelist.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pricelist
sudo systemctl start pricelist

# 配置Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/pricelist
sudo ln -s /etc/nginx/sites-available/pricelist /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🌐 配置SSL证书

```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d price.pylosy.com

# 测试自动续期
sudo certbot renew --dry-run
```

---

## 📊 服务管理

```bash
# 查看状态
sudo systemctl status pricelist

# 启动
sudo systemctl start pricelist

# 停止
sudo systemctl stop pricelist

# 重启
sudo systemctl restart pricelist

# 重新加载（优雅重启）
sudo systemctl reload pricelist

# 查看日志
sudo journalctl -u pricelist -f
```

---

## 📝 日志查看

```bash
# 应用日志
sudo tail -f /var/log/pricelist/error.log
sudo tail -f /var/log/pricelist/access.log

# Nginx日志
sudo tail -f /var/log/nginx/pricelist_error.log
sudo tail -f /var/log/nginx/pricelist_access.log

# 系统日志
sudo journalctl -u pricelist -n 100
```

---

## 🔄 手动更新代码

```bash
cd /var/www/pricelist/current
sudo -u www-data git pull origin main
sudo -u www-data source venv/bin/activate
sudo -u www-data pip install -r requirements.txt
sudo systemctl restart pricelist
```

---

## ↩️ 回滚版本

```bash
# 查看备份
ls -lh /var/www/pricelist/releases/

# 回滚
sudo rm -rf /var/www/pricelist/current
sudo cp -r /var/www/pricelist/releases/20260117_123456 /var/www/pricelist/current
sudo systemctl restart pricelist
```

---

## 🧪 测试访问

```bash
# 测试本地服务
curl http://localhost:8001

# 测试Nginx
curl http://localhost

# 测试域名
curl https://price.pylosy.com

# 测试健康检查
curl https://price.pylosy.com/health
```

---

## 🔍 故障排查

```bash
# 检查端口占用
sudo lsof -i :8001
sudo lsof -i :80
sudo lsof -i :443

# 检查进程
ps aux | grep gunicorn
ps aux | grep nginx

# 测试Nginx配置
sudo nginx -t

# 检查防火墙
sudo ufw status

# 检查磁盘空间
df -h

# 检查内存
free -h
```

---

## 📤 推送更新

```bash
# 日常更新
git add .
git commit -m "feat: 添加新功能"
git push origin main
# 自动触发GitHub Actions部署
```

---

## 🎯 GitHub Actions

### 手动触发部署

1. GitHub → Actions → Deploy to Production
2. Run workflow → main分支
3. 点击绿色按钮

### 查看部署日志

GitHub → Actions → 点击工作流 → 展开步骤

---

## 🔐 安全加固

```bash
# 配置防火墙
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 安装fail2ban
sudo apt-get install fail2ban
sudo systemctl enable fail2ban

# 禁用密码登录
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

---

## 📋 常用文件路径

```
项目目录: /var/www/pricelist/current
备份目录: /var/www/pricelist/releases
日志目录: /var/log/pricelist/
虚拟环境: /var/www/pricelist/current/venv
配置文件: /var/www/pricelist/current/.env
Nginx配置: /etc/nginx/sites-available/pricelist
服务配置: /etc/systemd/system/pricelist.service
```

---

## ⚡ 一行命令

```bash
# 完整部署（新服务器）
curl -sSL https://raw.githubusercontent.com/yalding8/pricelist/main/deploy/setup-server.sh | sudo bash

# 快速重启
sudo systemctl restart pricelist && sudo systemctl restart nginx

# 查看状态
sudo systemctl status pricelist nginx --no-pager

# 清理日志
sudo truncate -s 0 /var/log/pricelist/*.log

# 备份当前版本
sudo cp -r /var/www/pricelist/current /var/www/pricelist/releases/$(date +%Y%m%d_%H%M%S)
```

---

**保存这个文件，部署时随时查阅！** 📌
