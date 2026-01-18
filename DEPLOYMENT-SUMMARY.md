# 📦 部署配置总结

完整的部署相关文件和配置清单。

---

## ✅ 已创建的文件

### 📋 核心配置文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `.gitignore` | Git忽略文件 | 项目根目录 |
| `requirements.txt` | Python依赖 | 项目根目录 |
| `.env.example` | 环境变量示例 | 项目根目录 |
| `wsgi.py` | WSGI入口 | 项目根目录 |
| `gunicorn_config.py` | Gunicorn配置 | 项目根目录 |
| `pricelist_web_app.py` | Flask主应用 | 项目根目录 |

### 🚀 部署文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `.github/workflows/deploy.yml` | GitHub Actions | `.github/workflows/` |
| `deploy/pricelist.service` | Systemd服务 | `deploy/` |
| `deploy/nginx.conf` | Nginx配置 | `deploy/` |
| `deploy/setup-server.sh` | 服务器初始化 | `deploy/` |
| `deploy/DEPLOYMENT-CHECKLIST.md` | 部署检查清单 | `deploy/` |

### 📚 文档文件

| 文件 | 用途 | 位置 |
|------|------|------|
| `README.md` | 项目主文档 | 项目根目录 |
| `DEPLOYMENT.md` | 完整部署指南 | 项目根目录 |
| `GITHUB-SETUP.md` | GitHub配置指南 | 项目根目录 |
| `QUICK-DEPLOY.md` | 快速命令参考 | 项目根目录 |
| `QUICK-START.md` | 快速开始指南 | 项目根目录 |
| `README-WEB-APP.md` | Web应用使用手册 | 项目根目录 |
| `PROJECT-SUMMARY.md` | 项目总览 | 项目根目录 |

---

## 🎯 下一步操作

### 1. 推送到GitHub

```bash
git init
git add .
git commit -m "feat: 完整部署配置"
git branch -M main
git remote add origin https://github.com/yalding8/pricelist.git
git push -u origin main
```

### 2. 配置GitHub Secrets

在GitHub仓库设置中添加：
- `SERVER_HOST`: 服务器IP
- `SERVER_USER`: www-data
- `SSH_PRIVATE_KEY`: SSH私钥
- `SERVER_PORT`: 22 (可选)

### 3. 服务器初始化

```bash
# SSH登录服务器
ssh root@your-server-ip

# 下载并运行初始化脚本
wget https://raw.githubusercontent.com/yalding8/pricelist/main/deploy/setup-server.sh
chmod +x setup-server.sh
sudo ./setup-server.sh
```

### 4. 配置DNS

在DNS服务商添加A记录：
```
类型: A
主机记录: price
记录值: 服务器IP
```

### 5. 安装SSL证书

```bash
sudo certbot --nginx -d price.pylosy.com
```

### 6. 触发首次部署

GitHub → Actions → Deploy to Production → Run workflow

### 7. 验证部署

访问: https://price.pylosy.com

---

## 📁 完整目录结构

```
pricelist/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions工作流
│
├── deploy/                         # 部署配置目录
│   ├── nginx.conf                  # Nginx配置
│   ├── pricelist.service           # Systemd服务
│   ├── setup-server.sh             # 服务器初始化脚本
│   └── DEPLOYMENT-CHECKLIST.md     # 部署检查清单
│
├── templates/                      # Flask模板
│   └── form.html                   # 表单界面
│
├── pricelist_web_app.py            # Flask主应用
├── wsgi.py                         # WSGI入口
├── gunicorn_config.py              # Gunicorn配置
│
├── pricelist-demo.py               # 演示脚本
├── pricelist-models.py             # 数据模型
├── pricelist-brand_config.py       # 品牌配置
├── pricelist-gift_library.yaml     # 礼品库
│
├── pricelist-quote-wechat.html     # 微信版模板
├── pricelist-quote-1024x768.html   # 桌面版模板
├── pricelist-quote-compact.html    # 紧凑版模板
├── pricelist-quote-premium.html    # 高端版模板
│
├── requirements.txt                # Python依赖
├── .env.example                    # 环境变量示例
├── .gitignore                      # Git忽略文件
│
├── README.md                       # 项目主文档
├── DEPLOYMENT.md                   # 完整部署指南
├── GITHUB-SETUP.md                 # GitHub配置指南
├── QUICK-DEPLOY.md                 # 快速命令参考
├── QUICK-START.md                  # 快速开始
├── README-WEB-APP.md               # Web应用手册
├── PROJECT-SUMMARY.md              # 项目总览
└── DEPLOYMENT-SUMMARY.md           # 本文档
```

---

## 🔑 关键配置说明

### Gunicorn配置

**文件**: `gunicorn_config.py`

- **绑定地址**: `0.0.0.0:8001`
- **Worker数量**: `CPU核心数 * 2 + 1`
- **超时**: 120秒
- **日志**: `/var/log/pricelist/`

### Nginx配置

**文件**: `deploy/nginx.conf`

- **监听端口**: 80 (HTTP) / 443 (HTTPS)
- **域名**: price.pylosy.com
- **反向代理**: → 127.0.0.1:8001
- **上传限制**: 10MB
- **超时**: 60秒

### Systemd服务

**文件**: `deploy/pricelist.service`

- **服务名**: pricelist
- **用户**: www-data
- **工作目录**: `/var/www/pricelist/current`
- **启动命令**: `gunicorn --config gunicorn_config.py wsgi:application`
- **自动重启**: 失败后10秒重启

### GitHub Actions

**文件**: `.github/workflows/deploy.yml`

- **触发条件**: push到main分支 / 手动触发
- **部署步骤**:
  1. 备份当前版本
  2. 拉取最新代码
  3. 安装依赖
  4. 重启服务
  5. 清理旧备份

---

## 🔄 部署流程图

```
本地开发
   ↓
git push origin main
   ↓
GitHub Actions触发
   ↓
SSH连接服务器
   ↓
备份当前版本 → /var/www/pricelist/releases/
   ↓
git pull最新代码
   ↓
安装依赖
   ↓
systemctl restart pricelist
   ↓
验证服务状态
   ↓
清理旧备份（保留最近5个）
   ↓
部署完成 ✅
```

---

## 📊 环境对比

| 环境 | 域名 | 端口 | 服务器 | 部署方式 |
|------|------|------|--------|----------|
| **开发** | localhost | 5001 | 本地 | 手动启动 |
| **生产** | price.pylosy.com | 8001→80/443 | 远程 | 自动部署 |

---

## 🛡️ 安全措施

- ✅ **HTTPS强制**: Certbot自动配置
- ✅ **防火墙**: ufw限制端口
- ✅ **SSH密钥**: 禁用密码登录
- ✅ **Fail2ban**: 防暴力破解
- ✅ **最小权限**: www-data用户运行
- ✅ **日志监控**: 集中日志管理
- ✅ **定期备份**: 自动备份最近5个版本

---

## 📈 性能优化

- ✅ **Gunicorn多Worker**: CPU核心数 * 2 + 1
- ✅ **Nginx缓存**: 静态文件缓存30天
- ✅ **Gzip压缩**: Nginx自动压缩
- ✅ **HTTP/2**: SSL启用HTTP/2
- ✅ **连接池**: Gunicorn keepalive
- ✅ **优雅重启**: 零停机部署

---

## 📞 支持和帮助

### 文档索引

- **快速开始**: [QUICK-START.md](QUICK-START.md)
- **详细部署**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **GitHub配置**: [GITHUB-SETUP.md](GITHUB-SETUP.md)
- **命令参考**: [QUICK-DEPLOY.md](QUICK-DEPLOY.md)
- **检查清单**: [deploy/DEPLOYMENT-CHECKLIST.md](deploy/DEPLOYMENT-CHECKLIST.md)

### 常见问题

查看各个文档的"故障排查"章节。

### 联系方式

- GitHub Issues: https://github.com/yalding8/pricelist/issues
- Email: your-email@example.com

---

## ✅ 部署完成确认

完成部署后，确认以下项目：

- [ ] ✅ 代码已推送到GitHub
- [ ] ✅ GitHub Secrets已配置
- [ ] ✅ 服务器已初始化
- [ ] ✅ DNS解析正常
- [ ] ✅ SSL证书已安装
- [ ] ✅ 服务运行正常
- [ ] ✅ 可以通过域名访问
- [ ] ✅ GitHub Actions部署成功
- [ ] ✅ 所有功能测试通过

---

**恭喜！你的应用已成功部署到生产环境！** 🎉

**在线地址**: https://price.pylosy.com

---

**最后更新**: 2026-01-18
