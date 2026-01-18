# 🏠 Pricelist - 异乡好居报价单生成系统

为异乡好居（Uhomes）销售顾问打造的专业报价单生成系统。

[![Deploy Status](https://img.shields.io/badge/deploy-automatic-success)](https://github.com/yalding8/pricelist)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ 功能特性

- 🎨 **可视化表单界面** - 友好的Web界面，无需编程
- 💰 **价格透明化** - 清晰展示房东优惠和异乡补贴
- 🎁 **礼品库系统** - 15个精选礼品，点击勾选
- 📱 **微信优化** - 专为微信分享优化的PNG长图
- 🖥️ **多终端适配** - 手机、平板、桌面全覆盖
- 🚀 **一键生成** - 同时生成HTML和PNG两种格式
- ⚡ **自动部署** - GitHub Actions自动部署到服务器

---

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆仓库
git clone https://github.com/yalding8/pricelist.git
cd pricelist

# 2. 安装依赖
pip install -r requirements.txt
python -m playwright install chromium

# 3. 启动服务
python3 pricelist-web-app.py

# 4. 访问应用
# 打开浏览器: http://localhost:5001
```

详细说明：[QUICK-START.md](QUICK-START.md)

### 生产部署

完整的服务器部署指南：[DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📱 在线访问

**生产环境**: https://price.pylosy.com

---

## 📸 界面预览

### 表单界面
![表单界面](docs/images/form-preview.png)

### 报价单示例
![报价单示例](docs/images/quote-preview.png)

---

## 📁 项目结构

```
pricelist/
├── pricelist_web_app.py         # Flask应用主文件
├── wsgi.py                      # WSGI入口
├── requirements.txt             # Python依赖
├── templates/
│   └── form.html                # 表单界面
├── pricelist-quote-wechat.html  # 微信版模板
├── pricelist-gift_library.yaml  # 礼品库配置
├── deploy/                      # 部署配置
│   ├── nginx.conf               # Nginx配置
│   ├── pricelist.service        # Systemd服务
│   └── setup-server.sh          # 服务器初始化
└── .github/workflows/
    └── deploy.yml               # GitHub Actions
```

---

## 🛠️ 技术栈

- **后端**: Python 3.9+ / Flask 3.1
- **模板**: Jinja2
- **截图**: Playwright
- **部署**: Gunicorn + Nginx
- **CI/CD**: GitHub Actions

---

## 📚 文档

- [快速开始](QUICK-START.md) - 1分钟上手指南
- [Web应用使用手册](README-WEB-APP.md) - 详细功能说明
- [部署指南](DEPLOYMENT.md) - 完整部署流程
- [项目总览](PROJECT-SUMMARY.md) - 项目全貌

---

## 🎯 使用场景

### 场景1: 微信一对一咨询

1. 打开Web表单
2. 填写房源信息和优惠
3. 选择礼品
4. 生成PNG长图
5. 在微信中发送给客户

**时间**: 3-5分钟

### 场景2: 办公室面对面

1. 使用1024×768版本
2. 投影到显示器
3. 与客户讲解细节

**优势**: 专业、清晰

---

## 🔧 开发指南

### 环境配置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r requirements.txt
```

### 运行测试

```bash
# 生成示例报价单
python3 pricelist-demo.py

# 测试Web应用
./test-web-app.sh
```

### 修改模板

编辑对应的HTML文件：
- `pricelist-quote-wechat.html` - 微信版
- `pricelist-quote-1024x768.html` - 桌面版
- `pricelist-quote-compact.html` - 紧凑版
- `pricelist-quote-premium.html` - 高端版

### 添加礼品

编辑 `pricelist-gift_library.yaml`：

```yaml
gift_library:
  - id: new_gift
    name: 新礼品名称
    value: 100
    category: cash
    icon: 💰
    description: 说明
```

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📝 变更日志

### v1.0.0 (2026-01-17)

- ✅ 初始版本发布
- ✅ Web表单界面
- ✅ 4个报价单模板
- ✅ PNG长图生成
- ✅ GitHub Actions自动部署

---

## 📄 许可证

[MIT License](LICENSE)

---

## 📞 联系方式

- **GitHub**: [@yalding8](https://github.com/yalding8)
- **Email**: your-email@example.com
- **网站**: https://price.pylosy.com

---

## ⭐ Star History

如果这个项目对你有帮助，请给个Star ⭐️

[![Star History Chart](https://api.star-history.com/svg?repos=yalding8/pricelist&type=Date)](https://star-history.com/#yalding8/pricelist&Date)

---

**Happy coding! 🎉**
