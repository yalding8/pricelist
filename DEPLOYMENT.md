# 🚀 Pricelist 部署指南

完整的生产环境部署流程，包括GitHub Actions自动部署到服务器。

---

## 📋 目录

1. [准备工作](#准备工作)
2. [服务器配置](#服务器配置)
3. [GitHub配置](#github配置)
4. [首次部署](#首次部署)
5. [自动部署](#自动部署)
6. [域名和SSL](#域名和ssl)
7. [运维管理](#运维管理)
8. [故障排查](#故障排查)

---

## 准备工作

### 服务器要求

- **操作系统**: Ubuntu 20.04+ / Debian 11+
- **CPU**: 2核+
- **内存**: 2GB+
- **磁盘**: 20GB+
- **权限**: root或sudo访问

### 本地要求

- Git
- GitHub账号
- SSH密钥对

---

## 服务器配置

### 1. 首次登录服务器

```bash
ssh root@your-server-ip
```

### 2. 运行初始化脚本

```bash
# 下载初始化脚本
wget https://raw.githubusercontent.com/yalding8/pricelist/main/deploy/setup-server.sh

# 赋予执行权限
chmod +x setup-server.sh

# 运行脚本
sudo ./setup-server.sh
```

脚本会自动完成以下任务：
- ✅ 更新系统包
- ✅ 安装Python、Nginx、Git等
- ✅ 创建项目目录
- ✅ 克隆代码仓库
- ✅ 创建Python虚拟环境
- ✅ 安装依赖
- ✅ 配置systemd服务
- ✅ 配置Nginx
- ✅ 启动服务

### 3. 手动配置（如果自动脚本失败）

#### 安装依赖

```bash
apt-get update
apt-get install -y python3 python3-pip python3-venv git nginx
```

#### 创建项目目录

```bash
mkdir -p /var/www/pricelist/{current,releases}
mkdir -p /var/log/pricelist
```

#### 克隆代码

```bash
cd /var/www/pricelist/current
git clone https://github.com/yalding8/pricelist.git .
```

#### 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv gunicorn
python -m playwright install chromium
```

#### 配置环境变量

```bash
cp .env.example .env
nano .env  # 编辑配置
```

#### 设置权限

```bash
chown -R www-data:www-data /var/www/pricelist
chown -R www-data:www-data /var/log/pricelist
```

#### 安装systemd服务

```bash
cp deploy/pricelist.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable pricelist
systemctl start pricelist
```

#### 配置Nginx

```bash
cp deploy/nginx.conf /etc/nginx/sites-available/pricelist
ln -s /etc/nginx/sites-available/pricelist /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

---

## GitHub配置

### 1. 创建GitHub仓库

```bash
# 在本地项目目录
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yalding8/pricelist.git
git push -u origin main
```

### 2. 生成SSH密钥对

在**本地电脑**生成：

```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/pricelist_deploy
```

会生成两个文件：
- `pricelist_deploy`（私钥）
- `pricelist_deploy.pub`（公钥）

### 3. 配置服务器SSH访问

将**公钥**添加到服务器：

```bash
# 在服务器上
sudo su - www-data
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys  # 粘贴公钥内容
chmod 600 ~/.ssh/authorized_keys
```

测试SSH连接：

```bash
# 在本地
ssh -i ~/.ssh/pricelist_deploy www-data@your-server-ip
```

### 4. 配置GitHub Secrets

在GitHub仓库页面：**Settings → Secrets and variables → Actions → New repository secret**

添加以下Secrets：

| Name | Value | 说明 |
|------|-------|------|
| `SERVER_HOST` | `your-server-ip` | 服务器IP或域名 |
| `SERVER_USER` | `www-data` | SSH用户 |
| `SSH_PRIVATE_KEY` | `私钥内容` | 从pricelist_deploy文件复制 |
| `SERVER_PORT` | `22` | SSH端口（可选，默认22） |

复制私钥内容：

```bash
cat ~/.ssh/pricelist_deploy
```

---

## 首次部署

### 1. 手动触发部署

在GitHub仓库页面：**Actions → Deploy to Production → Run workflow**

### 2. 查看部署日志

GitHub Actions会显示详细的部署过程。

### 3. 验证部署

```bash
# 在服务器上
sudo systemctl status pricelist
sudo journalctl -u pricelist -n 50

# 测试访问
curl http://localhost:8001
curl http://price.pylosy.com
```

---

## 自动部署

配置完成后，每次推送到`main`分支都会自动部署：

```bash
git add .
git commit -m "Update feature"
git push origin main
```

GitHub Actions会自动：
1. ✅ 备份当前版本
2. ✅ 拉取最新代码
3. ✅ 安装依赖
4. ✅ 重启服务
5. ✅ 清理旧备份

---

## 域名和SSL

### 1. 配置DNS

在你的DNS提供商（如阿里云、Cloudflare）添加A记录：

```
类型: A
主机记录: price
记录值: your-server-ip
TTL: 600
```

等待DNS生效（5-30分钟）：

```bash
ping price.pylosy.com
```

### 2. 安装SSL证书

使用Let's Encrypt免费证书：

```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书并自动配置Nginx
sudo certbot --nginx -d price.pylosy.com

# 测试自动续期
sudo certbot renew --dry-run
```

Certbot会自动：
- 获取SSL证书
- 配置Nginx HTTPS
- 设置自动续期

### 3. 强制HTTPS

Certbot会自动添加HTTP到HTTPS的重定向。

如果需要手动添加，编辑nginx配置：

```nginx
server {
    listen 80;
    server_name price.pylosy.com;
    return 301 https://$host$request_uri;
}
```

---

## 运维管理

### 服务管理

```bash
# 查看状态
sudo systemctl status pricelist

# 启动服务
sudo systemctl start pricelist

# 停止服务
sudo systemctl stop pricelist

# 重启服务
sudo systemctl restart pricelist

# 重新加载配置（优雅重启）
sudo systemctl reload pricelist

# 查看日志
sudo journalctl -u pricelist -f
```

### 查看应用日志

```bash
# 应用日志
sudo tail -f /var/log/pricelist/error.log
sudo tail -f /var/log/pricelist/access.log

# Nginx日志
sudo tail -f /var/log/nginx/pricelist_error.log
sudo tail -f /var/log/nginx/pricelist_access.log
```

### 更新代码（手动）

```bash
cd /var/www/pricelist/current
sudo -u www-data git pull origin main
sudo -u www-data source venv/bin/activate
sudo -u www-data pip install -r requirements.txt
sudo systemctl restart pricelist
```

### 回滚版本

```bash
# 查看备份
ls -lh /var/www/pricelist/releases/

# 回滚到备份版本
sudo rm -rf /var/www/pricelist/current
sudo cp -r /var/www/pricelist/releases/20260117_123456 /var/www/pricelist/current
sudo systemctl restart pricelist
```

### 数据库备份（如果有数据库）

```bash
# 创建备份脚本
sudo nano /usr/local/bin/backup-pricelist.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/pricelist"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
# 备份生成的报价单
tar -czf $BACKUP_DIR/quotes_$DATE.tar.gz /var/www/pricelist/current/quote_*.html
# 保留最近30天
find $BACKUP_DIR -type f -mtime +30 -delete
```

### 监控和告警

推荐使用：
- **Uptime监控**: UptimeRobot, StatusCake
- **日志监控**: Logwatch, Sentry
- **性能监控**: New Relic, DataDog

---

## 故障排查

### 问题1: 服务无法启动

```bash
# 查看详细错误
sudo journalctl -u pricelist -n 100 --no-pager

# 检查端口占用
sudo lsof -i :8001

# 手动启动测试
cd /var/www/pricelist/current
source venv/bin/activate
gunicorn --config gunicorn_config.py wsgi:application
```

### 问题2: Nginx 502 Bad Gateway

```bash
# 检查Gunicorn是否运行
sudo systemctl status pricelist

# 检查nginx配置
sudo nginx -t

# 查看nginx错误日志
sudo tail -f /var/log/nginx/pricelist_error.log

# 检查socket文件权限
ls -l /tmp/pricelist.pid
```

### 问题3: GitHub Actions部署失败

检查以下项：
- ✅ GitHub Secrets配置正确
- ✅ SSH私钥格式正确（包含BEGIN和END行）
- ✅ 服务器SSH端口开放
- ✅ www-data用户有权限执行git和systemctl

### 问题4: 模块导入错误

```bash
# 激活虚拟环境
cd /var/www/pricelist/current
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
pip install python-dotenv gunicorn

# 重启服务
sudo systemctl restart pricelist
```

### 问题5: Playwright浏览器错误

```bash
# 重新安装浏览器
cd /var/www/pricelist/current
source venv/bin/activate
python -m playwright install chromium

# 安装系统依赖
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0
```

---

## 性能优化

### Nginx缓存

```nginx
# 添加到nginx配置
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=pricelist_cache:10m max_size=100m;

location / {
    proxy_cache pricelist_cache;
    proxy_cache_valid 200 10m;
    # ... 其他配置
}
```

### Gunicorn Workers

调整`gunicorn_config.py`：

```python
# CPU密集型应用
workers = multiprocessing.cpu_count() + 1

# IO密集型应用
workers = multiprocessing.cpu_count() * 2 + 1
```

### 日志轮转

```bash
sudo nano /etc/logrotate.d/pricelist
```

```
/var/log/pricelist/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload pricelist > /dev/null 2>&1 || true
    endscript
}
```

---

## 安全建议

1. **定期更新系统**
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

2. **配置防火墙**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **禁用密码登录**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   sudo systemctl restart sshd
   ```

4. **设置fail2ban**
   ```bash
   sudo apt-get install fail2ban
   sudo systemctl enable fail2ban
   ```

---

## 联系和支持

如有问题，请查看：
- GitHub Issues: https://github.com/yalding8/pricelist/issues
- 项目文档: PROJECT-SUMMARY.md

---

**部署愉快！🚀**
