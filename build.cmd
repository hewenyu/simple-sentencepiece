@echo off
setlocal enabledelayedexpansion

:: 检查 Python 是否安装
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    exit /b 1
)

:: 设置代理（如果需要的话）
set http_proxy=http://192.168.199.118:7890
set https_proxy=http://192.168.199.118:7890

:: 设置环境变量
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
chcp 65001

:: 激活虚拟环境
call .venv\Scripts\activate.bat

:: 获取 Python 路径
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.prefix)"') do set PYTHON_ROOT=%%i

:: 创建构建目录
if exist build (
    echo Cleaning build directory...
    rmdir /s /q build
)
mkdir build

:: 配置 CMake
echo Configuring CMake...
cmake -B build -G Ninja ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DPYTHON_EXECUTABLE="%PYTHON_PATH%" ^
    -DPython_EXECUTABLE="%PYTHON_PATH%" ^
    -DPython_ROOT_DIR="%PYTHON_ROOT%" ^
    -DCMAKE_CXX_STANDARD=14 ^
    -DCMAKE_CXX_STANDARD_REQUIRED=ON

if %ERRORLEVEL% neq 0 (
    echo CMake configuration failed
    exit /b 1
)

:: 构建项目
echo Building project...
cmake --build build --config Release

if %ERRORLEVEL% neq 0 (
    echo Build failed
    exit /b 1
)

echo Build completed successfully!
endlocal 