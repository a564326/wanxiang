@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   万象词条录 - 一键推送到 GitHub
echo ============================================
echo.

REM 检查 git
where git >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 git，请先安装 git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM 检查是否是 git 仓库
if not exist ".git" (
    echo [信息] 初始化 git 仓库...
    git init
    git config user.name "a564326"
    git config user.email "a564326@users.noreply.github.com"
)

REM 添加远程仓库
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [信息] 添加远程仓库...
    git remote add origin https://github.com/a564326/wanxiang.git
)

echo.
echo [1/3] 添加所有文件...
git add -A
echo   完成

echo.
echo [2/3] 提交...
git commit -m "update: 万象词条录"
if errorlevel 1 (
    echo   [提示] 没有新的更改需要提交
)

echo.
echo [3/3] 推送到 GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [提示] 推送失败，可能是首次推送需要认证
    echo.
    echo 如果提示输入用户名密码：
    echo   用户名: a564326
    echo   密码: 不是登录密码，是 Personal Access Token
    echo.
    echo 获取 Token 步骤：
    echo   1. 打开 https://github.com/settings/tokens
    echo   2. 点 Generate new token -^> Generate new token (classic)
    echo   3. Note 随便填，比如 wanxiang
    echo   4. 勾选 repo（全部勾选）
    echo   5. 点 Generate token
    echo   6. 复制生成的 token（ghp_开头），粘贴到密码处
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   推送成功！
echo ============================================
echo.
echo 查看构建进度：
echo   https://github.com/a564326/wanxiang/actions
echo.
echo 约 15-25 分钟后，在 Actions 页面点绿色对勾的任务
echo 最下方 Artifacts 下载 wanxiang-apk
echo.
pause
