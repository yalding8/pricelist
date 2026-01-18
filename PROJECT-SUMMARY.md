# 📊 Pricelist 项目总览

## 🎯 项目目标

为异乡好居（Uhomes）销售顾问打造一个**报价单生成系统**，帮助销售顾问快速向客户展示：
- 房源价格明细
- 优惠和补贴详情
- 赠送礼包价值
- 总节省金额和优惠幅度

---

## ✅ 已完成功能

### 1. 核心系统

| 功能 | 状态 | 文件 |
|------|------|------|
| 数据模型 | ✅ | pricelist-models.py |
| 礼品库配置 | ✅ | pricelist-gift_library.yaml |
| 品牌配置 | ✅ | pricelist-brand_config.py |
| 演示程序 | ✅ | pricelist-demo.py |

### 2. 报价单模板（4个版本）

| 模板 | 适用场景 | 尺寸 | 状态 |
|------|----------|------|------|
| **微信版** | 微信聊天、朋友圈 | 375px宽 | ✅ |
| **1024×768版** | 桌面演示、投影 | 1024×768 | ✅ |
| **Compact版** | 平板/大屏手机 | 750px宽 | ✅ |
| **Premium版** | 高端展示 | 750px宽 | ✅ |

**推荐使用**：微信版（pricelist-quote-wechat.html）

### 3. Web应用（顾问表单系统）

| 组件 | 功能 | 状态 |
|------|------|------|
| Flask后端 | API服务、报价单生成 | ✅ |
| 表单界面 | 可视化输入、礼品选择 | ✅ |
| PNG生成 | Playwright截图 | ✅ |
| 文件下载 | HTML/PNG下载 | ✅ |

**访问地址**：http://localhost:5001

### 4. 工具脚本

| 脚本 | 功能 | 状态 |
|------|------|------|
| pricelist-demo.py | 命令行生成示例 | ✅ |
| pricelist-generate-image.py | PNG长图生成 | ✅ |
| pricelist-screenshot-mobile.py | 多尺寸截图 | ✅ |
| pricelist-screenshot-1024x768.py | 桌面版截图 | ✅ |
| start-web-app.sh | Web应用启动 | ✅ |

---

## 📁 项目文件结构

```
pricelist/
├── 核心模块
│   ├── pricelist-models.py              # 数据模型定义
│   ├── pricelist-brand_config.py        # 品牌配置
│   └── pricelist-gift_library.yaml      # 礼品库（15个礼品）
│
├── 报价单模板
│   ├── pricelist-quote-wechat.html      # 微信版 ⭐推荐
│   ├── pricelist-quote-1024x768.html    # 桌面版
│   ├── pricelist-quote-compact.html     # 紧凑版
│   └── pricelist-quote-premium.html     # 高端版
│
├── Web应用
│   ├── pricelist-web-app.py             # Flask后端
│   ├── templates/
│   │   └── form.html                    # 顾问表单界面
│   └── start-web-app.sh                 # 启动脚本
│
├── 工具脚本
│   ├── pricelist-demo.py                # 演示程序
│   ├── pricelist-generate-image.py      # PNG生成器
│   ├── pricelist-screenshot-mobile.py   # 手机截图
│   └── pricelist-screenshot-1024x768.py # 桌面截图
│
└── 文档
    ├── PROJECT-SUMMARY.md               # 本文档
    ├── README-WEB-APP.md                # Web应用详细文档
    ├── QUICK-START.md                   # 快速开始指南
    └── 使用示例/                         # 生成的示例文件
```

---

## 🎨 界面展示

### 微信版报价单（推荐）

**特点**：
- 宽度375px（iPhone标准）
- 2列礼品网格，触摸友好
- 字号15px，手机阅读清晰
- 卡片式设计，层次分明

**适用场景**：
- 微信聊天直接发送
- 客户可点击放大查看
- 长按保存到相册

### 顾问表单界面

**特点**：
- 渐变头部（品牌色）
- 清晰分区（房源、优惠、礼品、顾问）
- 可视化礼品选择（点击勾选）
- 实时表单验证

**功能**：
- 动态添加优惠项
- 礼品库自动加载
- 一键生成HTML+PNG
- 即时下载

---

## 📊 数据流程

```
用户输入 → Flask后端 → 数据验证 → Jinja2渲染 → HTML报价单
                                            ↓
                                      Playwright
                                            ↓
                                       PNG长图
```

---

## 💡 核心功能亮点

### 1. 价格透明化

✅ **分层展示**：
- 房东原价
- 房东优惠（蓝标）
- 异乡补贴（红标）
- 最终到手价

✅ **结算方标识**：
- 房东结算 vs 异乡结算
- 清晰区分责任方

### 2. 礼品库系统

✅ **15个精选礼品**：
- 💵 现金返现（£100-£500）
- ✈️ 服务类（接机、搬家）
- 🎫 优惠券（超市、餐厅）
- 🎁 实物礼品（生活礼包、欢迎包）

✅ **灵活配置**：
- YAML配置文件
- 支持自定义添加
- 图标+名称+价值

### 3. 微信分享优化

✅ **PNG长图**：
- 375px宽，适配所有手机
- 文件大小约170KB
- 客户可放大查看细节

✅ **传播友好**：
- 直接显示在聊天流
- 长按保存到相册
- 可转发给家人讨论

---

## 🔧 技术栈

### 后端
- **Python 3.9+**
- **Flask 3.1**: Web框架
- **Jinja2**: 模板引擎
- **Playwright**: 浏览器自动化（截图）
- **PyYAML**: 配置文件解析

### 前端
- **HTML5 + CSS3**: 语义化、响应式
- **Vanilla JavaScript**: 无依赖
- **CSS Grid**: 布局系统
- **CSS Custom Properties**: 设计系统

### 数据
- **dataclass**: 类型安全
- **Decimal**: 精确金额计算
- **Enum**: 枚举类型

---

## 📈 使用统计

### 模板对比

| 指标 | 微信版 | 1024×768版 | Compact版 | Premium版 |
|------|--------|------------|-----------|-----------|
| 宽度 | 375px | 1024px | 750px | 750px |
| 高度 | ~1200px | 768px | ~840px | ~1310px |
| 礼品布局 | 2列 | 4列 | 3列 | 2列 |
| 基础字号 | 15px | 13px | 14px | 16px |
| 适用场景 | 手机 | 桌面 | 平板 | 展示 |

### 生成文件大小

| 文件类型 | 大小 | 加载速度 |
|---------|------|----------|
| HTML | ~50KB | 瞬间 |
| PNG | ~170KB | <1秒 |

---

## 🚀 实际使用场景

### 场景1：微信一对一咨询

1. 顾问打开Web表单
2. 填写房源和优惠信息
3. 选择礼品
4. 生成PNG长图
5. 在微信中发送图片给客户
6. 客户点击放大查看

**优势**：即时呈现，视觉冲击强

### 场景2：办公室面对面

1. 顾问在电脑上打开1024×768版
2. 投影到显示器或投影仪
3. 与客户面对面讲解
4. 客户可以看到所有细节

**优势**：专业，沟通充分

### 场景3：批量发送（朋友圈）

1. 生成多个房源的报价单
2. 批量导出PNG图片
3. 在朋友圈发布
4. 感兴趣的客户主动咨询

**优势**：触达面广

---

## 📋 待开发功能

### 优先级1️⃣：历史记录
- 保存生成的报价单
- 快速查找和修改
- 避免重复输入

### 优先级2️⃣：模板管理
- 保存常用房源模板
- 一键套用
- 提高效率

### 优先级3️⃣：爬虫集成
- 自动获取Special Offers
- 实时价格更新
- 减少手动输入

### 优先级4️⃣：批量生成
- Excel导入房源列表
- 批量生成报价单
- 批量导出PNG

---

## 🎓 学习资源

### 如何修改模板样式？

编辑对应的HTML文件，修改CSS变量：

```css
:root {
    --brand-primary: #FF5A5F;  /* 主色调 */
    --spacing-md: 12px;         /* 间距 */
    --font-display: "SF Pro Display", ...;  /* 字体 */
}
```

### 如何添加新礼品？

编辑 `pricelist-gift_library.yaml`：

```yaml
gift_library:
  - id: my_new_gift
    name: 新礼品
    value: 100
    category: cash
    icon: 💰
    description: 说明文字
```

### 如何自定义品牌色？

编辑 `pricelist-brand_config.py`：

```python
BRAND_PRIMARY_COLOR = "#FF5A5F"
```

---

## 📞 技术支持

### 环境要求
- Python 3.9+
- pip3
- 现代浏览器（Chrome/Safari/Firefox）

### 依赖包
```bash
pip3 install flask jinja2 playwright pyyaml
python3 -m playwright install chromium
```

### 常见问题
详见：[README-WEB-APP.md](README-WEB-APP.md)

---

## 🎉 总结

这个项目提供了：

✅ **4个报价单模板**（微信、桌面、平板、高端）
✅ **Web表单系统**（可视化输入、一键生成）
✅ **PNG长图生成**（适合微信分享）
✅ **完整文档**（快速开始、详细指南）
✅ **礼品库系统**（15个礼品，可扩展）

**核心价值**：
- 🚀 **提高效率**：5分钟生成专业报价单
- 💰 **展示优势**：清晰的价格对比和优惠明细
- 📱 **适配微信**：最符合中国市场的分享方式
- 🎨 **品牌形象**：专业设计，提升信任度

---

**开始使用**：[QUICK-START.md](QUICK-START.md)

**Happy quoting! 🎊**
