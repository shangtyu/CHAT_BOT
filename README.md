# 二手商品价格预测聊天机器人

一个集成 DeepSeek AI 的智能价格预测系统，具有共享链接功能。

## 功能特性

- 🤖 智能价格预测
- 📊 市场分析报告 (由 DeepSeek AI 提供)
- 🔗 共享链接功能
- 📱 响应式设计
- 🔄 会话重置功能

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，确保 DeepSeek API 密钥正确：

```
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 启动应用

```bash
python app.py
```

或者使用启动脚本：

```bash
./start.sh
```

### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

## API 接口

### 价格预测
- **POST** `/predict_price`
- 请求体：`{"product": "商品描述"}`
- 返回：`{"price": 预测价格}`

### 市场分析
- **POST** `/deepseek`
- 请求体：`{"product": "商品描述"}`
- 返回：`{"market_analysis": "分析报告"}`

### 健康检查
- **GET** `/api/health`
- 返回：`{"status": "healthy", "service": "price-prediction-bot"}`

## 共享功能

应用包含以下共享功能：

1. **复制链接**：一键复制当前页面链接
2. **生成二维码**：生成页面二维码供移动设备扫描
3. **多端访问**：支持桌面和移动设备访问

## 目录结构

```
CHAT_BOT/
├── app.py              # Flask 主应用
├── requirements.txt    # Python 依赖
├── .env               # 环境变量
├── start.sh           # 启动脚本
├── templates/         # HTML 模板
│   └── frontend.html
├── static/           # 静态文件
│   └── logo.png
└── README.md         # 项目说明
```

## 安全建议

1. 不要将 `.env` 文件提交到版本控制系统
2. 在生产环境中使用更安全的密钥管理方案
3. 考虑添加用户认证和访问控制

## 技术栈

- **后端**：Flask + Python
- **前端**：HTML5 + JavaScript + CSS3
- **AI**：DeepSeek API
- **其他**：Flask-CORS, python-dotenv

## 部署建议

### 本地开发
```bash
export FLASK_ENV=development
python app.py
```

### 生产部署
考虑使用 Gunicorn 或其他 WSGI 服务器：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 故障排除

1. **导入错误**：确保已安装所有依赖
2. **API 调用失败**：检查 DeepSeek API 密钥是否正确
3. **模板未找到**：确保 templates 目录存在且包含 frontend.html

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！
