@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   万象词条录 - 一键回归校验 (Windows)
echo ============================================
echo.

echo [1/3] 代码校验...
python -m py_compile game_data.py main.py gacha_anim.py module_bg.py _prebuild_check.py
if errorlevel 1 ( echo 语法错误 & pause & exit /b 1 )
echo   通过 ✓

echo.
echo [2/3] 词条库 + 出包配置检查...
python _prebuild_check.py
if errorlevel 1 ( echo 检查未通过 & pause & exit /b 1 )

echo.
echo [3/3] 抽卡动画动态适配验证（mock 时钟驱动时序）...
python _runtime_check.py
if errorlevel 1 (
    echo   动画验证未通过
    pause
    exit /b 1
)

echo.
echo ============================================
echo   全部通过 ✓  可运行 package.bat 出 APK
echo ============================================
pause
