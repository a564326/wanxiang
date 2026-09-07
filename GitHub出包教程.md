# 万象词条录 · GitHub 云端出 APK 教程（零基础版）

> 为什么不用本地打包？因为 Kivy 打包 APK 需要 Linux 环境，Windows 原生不支持。用 GitHub 云端构建最省心，不用装 WSL、不用重启电脑。

---

## 第一步：注册 GitHub 账号（已有就跳过）

1. 打开 https://github.com
2. 点右上角 **Sign up**
3. 用邮箱注册，免费账号就行

---

## 第二步：创建新仓库

1. 登录后，点右上角 **+** 号 → **New repository**
2. Repository name 填：`wanxiang`
3. 选 **Public**（公开，免费）
4. 不要勾选任何选项（不要加 README、.gitignore、license）
5. 点 **Create repository**

---

## 第三步：上传代码

创建仓库后，你会看到一个页面，按下面操作：

### 方法A：网页上传（最简单）

1. 在仓库页面，点 **uploading an existing file** 链接
2. 打开文件夹 `G:\dev\wanxiang`
3. 把里面**所有文件和文件夹**全选（Ctrl+A），拖到网页的上传区域
4. 等上传完成，点页面底部的 **Commit changes**

### 方法B：用 GitHub Desktop（文件多的话推荐）

1. 下载安装 https://desktop.github.com
2. 登录你的 GitHub 账号
3. File → Clone repository → 选你刚建的 wanxiang 仓库
4. 把 `G:\dev\wanxiang` 里的所有文件复制到克隆下来的文件夹
5. GitHub Desktop 会自动检测变化，左下角填个备注（比如 "first commit"）
6. 点 **Commit to main**，然后点 **Push origin**

---

## 第四步：等待自动构建

1. 上传完成后，回到你的仓库页面
2. 点顶部的 **Actions** 标签
3. 你会看到一个叫 **Build APK** 的任务正在运行（黄色圆点）
4. 点进去可以看实时日志
5. **首次构建约 15-25 分钟**，耐心等

> 如果 Actions 页面是空的，说明上传没触发。点 Actions → 找到 "Build APK" → 右边点 **Run workflow** → 绿色按钮 Run workflow 手动触发。

---

## 第五步：下载 APK

1. 构建成功后（绿色对勾），点进那个构建任务
2. 页面最下方 **Artifacts** 区域，有个 `wanxiang-apk`
3. 点它下载，得到一个 zip 文件
4. 解压 zip，里面就是 `万象词条录-0.2-debug.apk`

---

## 第六步：安装到手机

1. 把 APK 传到手机（微信文件传输、QQ、U盘都行）
2. 手机上点击 APK 安装
3. 如果提示"未知来源应用"，去设置里允许安装

---

## 常见问题

| 问题 | 解决 |
|------|------|
| Actions 显示红色叉号（失败） | 点进任务看日志，把错误截图发给我 |
| 构建超过 30 分钟还没好 | 正常，首次下载依赖慢，再等等 |
| 上传后 Actions 没反应 | 确认 .github/workflows/build.yml 文件传上去了 |
| APK 安装失败 | 手机 CPU 架构不支持？这个包支持 arm64-v8a 和 armeabi-v7a（绝大多数安卓手机） |

---

## 修改代码后重新出包

每次你修改代码并上传（push），GitHub 会自动重新构建。也可以在 Actions 页面手动点 **Run workflow** 触发。
