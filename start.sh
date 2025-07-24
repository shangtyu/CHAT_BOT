#!/bin/bash

# 激活虚拟环境
echo "Activating virtual environment..."
source venv/bin/activate

# 安装依赖 (如果需要)
echo "Installing dependencies..."
pip install -r requirements.txt

# 启动Flask应用
echo "Starting Flask application..."
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
