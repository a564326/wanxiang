@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo   万象词条录 - APK 出包脚本 (Windows)
echo ============================================
echo.

REM ========== 0. 环境探测 ==========
echo [0/4] 探测 Android 环境...

if "%ANDROID_HOME%"=="" (
    REM 自动探测常见路径
    if exist "G:\Android\cmdline-tools" set "ANDROID_HOME=G:\Android"
    if exist "C:\Android\cmdline-tools" set "ANDROID_HOME=C:\Android"
    if exist "%LOCALAPPDATA%\Android\Sdk" set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
)
if "%ANDROID_HOME%"=="" (
    echo   [ERROR] 未找到 ANDROID_HOME，请先在系统环境变量中设置
    echo   例如: setx ANDROID_HOME "G:\Android"
    pause
    exit /b 1
)
echo   ANDROID_HOME = %ANDROID_HOME%

REM 探测 NDK 版本（取 buildozer.spec 里写的是 26b）
if exist "%ANDROID_HOME%\ndk" (
    for /d %%D in ("%ANDROID_HOME%\ndk\*") do set "ANDROID_NDK_HOME=%%D"
)
if "%ANDROID_NDK_HOME%"=="" (
    echo   [WARN] 未检测到 NDK 目录，请确认已安装
) else (
    echo   ANDROID_NDK_HOME = %ANDROID_NDK_HOME%
)

set "PATH=%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\build-tools\34.0.0"

REM ========== 1. 校验 ==========
echo.
echo [0.5/4] 生成/补齐美术资源（若已有 AI 原图则跳过覆盖）...
if not exist "assets\icon.png" (
    python _make_assets.py
) else (
    echo   美术资源已存在，跳过
)

echo.
echo [1/4] 运行代码校验...
python -m py_compile game_data.py main.py gacha_anim.py module_bg.py 2>&1
if errorlevel 1 (
    echo   [ERROR] 语法校验失败，请检查上方报错
    pause
    exit /b 1
)
echo   语法校验通过 ✓

if exist "_runtime_check.py" (
    python _runtime_check.py
    if errorlevel 1 (
        echo   [WARN] 运行时校验有警告，继续构建...
    ) else (
        echo   运行时校验通过 ✓
    )
)

REM ========== 2. 依赖 ==========
echo.
echo [2/4] 检查 Python 依赖...
python -c "import kivy" 2>nul
if errorlevel 1 (
    echo   安装 kivy...
    pip install kivy[base] -q
)
python -c "import buildozer" 2>nul
if errorlevel 1 (
    echo   安装 buildozer...
    pip install buildozer -q
)
echo   依赖就绪 ✓

REM ========== 3. 版本对齐检查 ==========
echo.
echo [3/4] 检查 buildozer.spec 版本对齐...
echo   目标: build-tools 34.0.0 / platform 34 / NDK 26b
echo   （如与实际不符，请修改 buildozer.spec 对应行）
type buildozer.spec | findstr /C:"android.build_tools" /C:"android.api" /C:"android.ndk"

REM ========== 4. 构建 ==========
echo.
echo [4/4] 开始构建 APK（首次约 15-25 分钟，请耐心）...
echo.
buildozer android debug

if exist "bin\*.apk" (
    echo.
    echo ============================================
    echo   [SUCCESS] APK 已生成！
    echo   位置: %cd%\bin\
    echo ============================================
    dir /b "bin\*.apk"
) else (
    echo.
    echo [ERROR] 构建未产出 APK，请检查上方日志
    echo   常见原因: 中文路径 / NDK版本不匹配 / 网络下载超时
)
pause
