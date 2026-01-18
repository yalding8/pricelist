# ✅ 部署检查清单

使用这个清单确保部署过程顺利完成。

---

## 📋 部署前检查

### 本地准备

- [ ] 代码已提交到Git
- [ ] 所有测试通过
- [ ] 依赖文件已更新（requirements.txt）
- [ ] .gitignore配置正确
- [ ] 环境变量示例文件已创建（.env.example）

### GitHub配置

- [ ] 创建GitHub仓库
- [ ] 推送代码到main分支
- [ ] 配置GitHub Secrets:
  - [ ] `SERVER_HOST`
  - [ ] `SERVER_USER`
  - [ ] `SSH_PRIVATE_KEY`
  - [ ] `SERVER_PORT` (可选)

### 服务器准备

- [ ] 服务器可访问（SSH）
- [ ] 服务器满足最低要求（2核2G）
- [ ] root或sudo权限
- [ ] 防火墙配置（开放22, 80, 443端口）

---

## 🖥️ 服务器初始化

- [ ] 更新系统包
  ```bash
  sudo apt-get update && sudo apt-get upgrade -y
  ```

- [ ] 安装基础软件
  ```bash
  sudo apt-get install -y python3 python3-pip python3-venv git nginx
  ```

- [ ] 创建项目目录
  ```bash
  sudo mkdir -p /var/www/pricelist/{current,releases}
  sudo mkdir -p /var/log/pricelist
  ```

- [ ] 克隆代码
  ```bash
  cd /var/www/pricelist/current
  sudo git clone https://github.com/yalding8/pricelist.git .
  ```

- [ ] 创建虚拟环境
  ```bash
  sudo python3 -m venv venv
  sudo venv/bin/pip install -r requirements.txt
  ```

- [ ] 安装Playwright浏览器
  ```bash
  sudo venv/bin/python -m playwright install chromium
  sudo venv/bin/python -m playwright install-deps
  ```

- [ ] 配置环境变量
  ```bash
  sudo cp .env.example .env
  sudo nano .env  # 编辑配置
  ```

- [ ] 设置文件权限
  ```bash
  sudo chown -R www-data:www-data /var/www/pricelist
  sudo chown -R www-data:www-data /var/log/pricelist
  ```

- [ ] 安装systemd服务
  ```bash
  sudo cp deploy/pricelist.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable pricelist
  sudo systemctl start pricelist
  ```

- [ ] 检查服务状态
  ```bash
  sudo systemctl status pricelist
  ```

- [ ] 配置Nginx
  ```bash
  sudo cp deploy/nginx.conf /etc/nginx/sites-available/pricelist
  sudo ln -s /etc/nginx/sites-available/pricelist /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

---

## 🌐 DNS和SSL配置

### DNS配置

- [ ] 登录DNS服务商（阿里云/Cloudflare等）
- [ ] 添加A记录
  - 类型: A
  - 主机记录: price
  - 记录值: 服务器IP
  - TTL: 600
- [ ] 等待DNS生效（5-30分钟）
- [ ] 测试DNS解析
  ```bash
  ping price.pylosy.com
  nslookup price.pylosy.com
  ```

### SSL证书（Let's Encrypt）

- [ ] 安装certbot
  ```bash
  sudo apt-get install certbot python3-certbot-nginx
  ```

- [ ] 获取证书
  ```bash
  sudo certbot --nginx -d price.pylosy.com
  ```

- [ ] 确认选择（重定向HTTP到HTTPS）

- [ ] 测试自动续期
  ```bash
  sudo certbot renew --dry-run
  ```

- [ ] 检查证书
  ```bash
  sudo certbot certificates
  ```

---

## 🚀 首次部署

### GitHub Actions

- [ ] 触发手动部署
  - GitHub → Actions → Deploy to Production → Run workflow

- [ ] 查看部署日志
  - 确认所有步骤成功

- [ ] 部署完成后检查
  ```bash
  sudo systemctl status pricelist
  sudo journalctl -u pricelist -n 50
  ```

### 功能测试

- [ ] 访问主页
  ```bash
  curl https://price.pylosy.com
  ```

- [ ] 测试表单加载
  - 打开浏览器访问 https://price.pylosy.com
  - 检查礼品库加载

- [ ] 测试报价单生成
  - 填写完整表单
  - 点击生成
  - 下载HTML和PNG

- [ ] 测试不同设备
  - [ ] 桌面浏览器
  - [ ] 手机浏览器
  - [ ] 平板浏览器

---

## 🔍 验证部署

### 服务健康检查

- [ ] Gunicorn进程运行中
  ```bash
  ps aux | grep gunicorn
  ```

- [ ] Nginx进程运行中
  ```bash
  ps aux | grep nginx
  ```

- [ ] 端口监听正常
  ```bash
  sudo lsof -i :8001  # Gunicorn
  sudo lsof -i :80    # Nginx HTTP
  sudo lsof -i :443   # Nginx HTTPS
  ```

- [ ] 日志无错误
  ```bash
  sudo tail -50 /var/log/pricelist/error.log
  sudo tail -50 /var/log/nginx/pricelist_error.log
  ```

### HTTP响应检查

- [ ] HTTP自动重定向到HTTPS
  ```bash
  curl -I http://price.pylosy.com
  # 应返回 301 或 302
  ```

- [ ] HTTPS正常访问
  ```bash
  curl -I https://price.pylosy.com
  # 应返回 200
  ```

- [ ] SSL证书有效
  ```bash
  openssl s_client -connect price.pylosy.com:443 -servername price.pylosy.com
  ```

### 性能测试

- [ ] 响应时间正常（< 3秒）
  ```bash
  time curl -s https://price.pylosy.com > /dev/null
  ```

- [ ] 并发测试
  ```bash
  ab -n 100 -c 10 https://price.pylosy.com/
  ```

---

## 📊 监控设置

### 日志监控

- [ ] 配置logrotate
  ```bash
  sudo nano /etc/logrotate.d/pricelist
  ```

- [ ] 测试logrotate
  ```bash
  sudo logrotate -d /etc/logrotate.d/pricelist
  ```

### 服务监控

- [ ] 设置Uptime监控（UptimeRobot/StatusCake）
  - URL: https://price.pylosy.com/health
  - 间隔: 5分钟
  - 通知: Email/Slack

- [ ] 配置邮件告警
  ```bash
  sudo apt-get install mailutils
  ```

### 系统监控

- [ ] 磁盘空间监控
  ```bash
  df -h
  ```

- [ ] 内存使用监控
  ```bash
  free -h
  ```

---

## 🔐 安全加固

- [ ] 配置防火墙
  ```bash
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```

- [ ] 禁用密码登录
  ```bash
  sudo nano /etc/ssh/sshd_config
  # PasswordAuthentication no
  sudo systemctl restart sshd
  ```

- [ ] 安装fail2ban
  ```bash
  sudo apt-get install fail2ban
  sudo systemctl enable fail2ban
  ```

- [ ] 定期更新系统
  ```bash
  sudo apt-get update && sudo apt-get upgrade
  ```

---

## 📝 文档更新

- [ ] 更新README.md（添加在线地址）
- [ ] 记录部署时间和版本
- [ ] 更新运维联系人信息
- [ ] 创建故障恢复文档

---

## ✅ 部署完成

恭喜！部署成功！🎉

### 最后确认

- [ ] 在线地址可访问: https://price.pylosy.com
- [ ] 所有功能正常工作
- [ ] SSL证书有效
- [ ] 监控已设置
- [ ] 团队成员已通知

### 交付清单

- [ ] 在线地址: https://price.pylosy.com
- [ ] 服务器IP: _____________
- [ ] SSH用户: www-data
- [ ] 日志位置: /var/log/pricelist/
- [ ] 项目目录: /var/www/pricelist/
- [ ] 重启命令: `sudo systemctl restart pricelist`

---

## 📞 支持联系

如遇到问题，请联系：
- GitHub Issues: https://github.com/yalding8/pricelist/issues
- Email: your-email@example.com

---

**部署日期**: _____________

**部署人**: _____________

**版本**: v1.0.0
