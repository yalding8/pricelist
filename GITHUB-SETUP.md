# 📤 GitHub设置指南

完整的GitHub仓库创建和配置流程。

---

## 步骤1: 创建GitHub仓库

### 在GitHub网站上

1. 访问 https://github.com/new
2. 填写信息:
   - **Repository name**: `pricelist`
   - **Description**: `异乡好居报价单生成系统`
   - **Visibility**: Private（推荐）或Public
   - **不要勾选**: Initialize with README, .gitignore, license
3. 点击 "Create repository"

---

## 步骤2: 初始化本地仓库

在项目目录执行:

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 首次提交
git commit -m "Initial commit: Pricelist报价单系统v1.0"

# 设置主分支名称
git branch -M main

# 关联远程仓库
git remote add origin https://github.com/yalding8/pricelist.git

# 推送到GitHub
git push -u origin main
```

---

## 步骤3: 生成SSH密钥

### 在本地电脑生成密钥对

```bash
# 生成新的SSH密钥
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/pricelist_deploy

# 查看公钥（添加到服务器）
cat ~/.ssh/pricelist_deploy.pub

# 查看私钥（添加到GitHub Secrets）
cat ~/.ssh/pricelist_deploy
```

### 密钥说明

- **公钥** (`pricelist_deploy.pub`): 添加到服务器的 `~/.ssh/authorized_keys`
- **私钥** (`pricelist_deploy`): 添加到GitHub Secrets

---

## 步骤4: 配置服务器SSH访问

### 方法1: 手动配置（推荐）

```bash
# SSH登录到服务器
ssh root@your-server-ip

# 切换到www-data用户
sudo su - www-data

# 创建.ssh目录
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 添加公钥
nano ~/.ssh/authorized_keys
# 粘贴 pricelist_deploy.pub 的内容
chmod 600 ~/.ssh/authorized_keys

# 退出www-data用户
exit
exit
```

### 方法2: 使用ssh-copy-id

```bash
# 在本地执行
ssh-copy-id -i ~/.ssh/pricelist_deploy.pub www-data@your-server-ip
```

### 测试SSH连接

```bash
# 在本地测试
ssh -i ~/.ssh/pricelist_deploy www-data@your-server-ip

# 成功登录后退出
exit
```

---

## 步骤5: 配置GitHub Secrets

### 访问GitHub仓库设置

1. 打开你的GitHub仓库
2. 点击 **Settings** (设置)
3. 左侧菜单选择 **Secrets and variables → Actions**
4. 点击 **New repository secret**

### 添加以下Secrets

#### SECRET 1: SERVER_HOST

- **Name**: `SERVER_HOST`
- **Value**: 你的服务器IP或域名
- 例如: `123.45.67.89` 或 `server.example.com`

#### SECRET 2: SERVER_USER

- **Name**: `SERVER_USER`
- **Value**: `www-data`

#### SECRET 3: SSH_PRIVATE_KEY

- **Name**: `SSH_PRIVATE_KEY`
- **Value**: 私钥完整内容
- 获取方法:
  ```bash
  cat ~/.ssh/pricelist_deploy
  ```
- 复制从 `-----BEGIN OPENSSH PRIVATE KEY-----` 到 `-----END OPENSSH PRIVATE KEY-----` 的所有内容（包括这两行）

#### SECRET 4: SERVER_PORT (可选)

- **Name**: `SERVER_PORT`
- **Value**: `22` (如果SSH端口是22，可以不配置)

### 验证Secrets配置

在 Secrets 页面应该看到:

- ✅ SERVER_HOST
- ✅ SERVER_USER
- ✅ SSH_PRIVATE_KEY
- ✅ SERVER_PORT (可选)

---

## 步骤6: 测试GitHub Actions

### 方法1: 推送触发

```bash
# 做一个小改动
echo "# Test deploy" >> README.md

# 提交并推送
git add README.md
git commit -m "Test: trigger GitHub Actions"
git push origin main
```

### 方法2: 手动触发

1. 访问 GitHub仓库
2. 点击 **Actions** 标签
3. 左侧选择 "Deploy to Production"
4. 点击 **Run workflow**
5. 选择 `main` 分支
6. 点击绿色的 **Run workflow** 按钮

### 查看部署日志

1. 在 Actions 页面
2. 点击正在运行的工作流
3. 展开 "Deploy to server" 步骤
4. 查看详细日志

---

## 步骤7: 验证部署成功

### 检查服务器

```bash
# SSH登录服务器
ssh root@your-server-ip

# 检查服务状态
sudo systemctl status pricelist

# 查看最近日志
sudo journalctl -u pricelist -n 50

# 检查Nginx
sudo systemctl status nginx
```

### 测试访问

```bash
# 本地测试
curl https://price.pylosy.com

# 或在浏览器打开
open https://price.pylosy.com
```

---

## 常见问题

### Q1: git push时要求输入用户名密码？

**A: 使用Personal Access Token**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. 勾选 `repo` 权限
4. 生成token并保存
5. 推送时使用token作为密码:
   ```bash
   Username: your-github-username
   Password: ghp_xxxxxxxxxxxx (你的token)
   ```

或者配置SSH方式:

```bash
# 修改远程仓库URL为SSH
git remote set-url origin git@github.com:yalding8/pricelist.git

# 推送
git push origin main
```

### Q2: GitHub Actions部署失败 - Permission denied

**A: 检查SSH配置**

1. 确认公钥已添加到服务器
2. 确认私钥完整复制到GitHub Secrets
3. 确认www-data用户有git和systemctl权限:
   ```bash
   sudo visudo
   # 添加:
   www-data ALL=(ALL) NOPASSWD: /bin/systemctl restart pricelist, /bin/systemctl status pricelist
   ```

### Q3: GitHub Actions部署失败 - Host key verification failed

**A: 添加known_hosts**

修改 `.github/workflows/deploy.yml`，在ssh-action步骤前添加:

```yaml
- name: Add server to known hosts
  run: |
    mkdir -p ~/.ssh
    ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts
```

或在ssh-action中添加:

```yaml
- name: Deploy to server
  uses: appleboy/ssh-action@v1.2.0
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    port: ${{ secrets.SERVER_PORT || 22 }}
    script_stop: true
    # 添加这行
    host_key_verification: false
    script: |
      # ... 部署脚本
```

### Q4: 如何回滚部署？

**A: 使用备份版本**

```bash
# SSH登录服务器
ssh root@your-server-ip

# 查看备份
ls -lh /var/www/pricelist/releases/

# 回滚
sudo rm -rf /var/www/pricelist/current
sudo cp -r /var/www/pricelist/releases/20260117_123456 /var/www/pricelist/current
sudo systemctl restart pricelist
```

---

## 日常工作流

### 开发新功能

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发和测试
# ... 编辑代码 ...

# 3. 提交更改
git add .
git commit -m "feat: 添加新功能"

# 4. 推送到GitHub
git push origin feature/new-feature

# 5. 创建Pull Request
# 在GitHub网站上创建PR

# 6. 合并到main后自动部署
```

### 修复bug

```bash
# 1. 创建修复分支
git checkout -b hotfix/fix-bug

# 2. 修复bug
# ... 编辑代码 ...

# 3. 提交
git add .
git commit -m "fix: 修复xxx bug"

# 4. 推送并合并
git push origin hotfix/fix-bug
# 创建PR并合并
```

### 直接推送到main（小改动）

```bash
git add .
git commit -m "docs: 更新文档"
git push origin main
# 自动触发部署
```

---

## 最佳实践

1. **提交信息规范**
   - `feat:` 新功能
   - `fix:` bug修复
   - `docs:` 文档更新
   - `style:` 代码格式
   - `refactor:` 重构
   - `test:` 测试
   - `chore:` 构建/工具

2. **分支策略**
   - `main` - 生产分支
   - `develop` - 开发分支
   - `feature/*` - 功能分支
   - `hotfix/*` - 修复分支

3. **定期备份**
   - GitHub自动备份代码
   - 服务器releases目录保留最近5个版本

4. **监控部署**
   - 每次部署后检查GitHub Actions日志
   - 验证服务器服务状态
   - 测试在线访问

---

## 清理和维护

### 清理本地分支

```bash
# 删除已合并的分支
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# 同步远程分支
git fetch --prune
```

### 清理服务器旧备份

```bash
# 自动清理（保留最近5个）
cd /var/www/pricelist/releases
ls -t | tail -n +6 | xargs rm -rf
```

---

## 参考资源

- [GitHub Actions文档](https://docs.github.com/actions)
- [SSH密钥生成](https://docs.github.com/authentication/connecting-to-github-with-ssh)
- [Git基础教程](https://git-scm.com/book/zh/v2)

---

**配置完成后，你的项目就可以自动部署了！** 🎉
