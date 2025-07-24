from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from openai import OpenAI
import os
import random
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 从环境变量获取API密钥
API_KEY = os.getenv('DEEPSEEK_API_KEY')

if not API_KEY:
    print("Warning: DEEPSEEK_API_KEY not found in environment variables")
    API_KEY = 'sk-1953083fe68946ca939bce624319660b'  # 后备方案

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
)

@app.route("/")
def index():
    return render_template("frontend.html")

@app.route("/predict_price", methods=["POST"])
def predict_price():
    """简单的价格预测功能"""
    data = request.get_json()
    product = data.get("product", "")
    
    # 这里可以添加实际的价格预测逻辑
    # 现在使用随机价格作为演示
    base_price = random.uniform(10, 200)
    predicted_price = round(base_price, 2)
    
    return jsonify({"price": predicted_price})

@app.route("/deepseek", methods=["POST"])
def deepseek_analysis():
    data = request.get_json()
    product = data.get("product", "")
    
    # 改进的提示词，要求英文输出
    prompt = f"""Please provide a comprehensive market analysis report for the following product:

Product: {product}

Please include:
1. Current market price trends
2. Comparison with similar products
3. Purchase recommendations
4. Market demand analysis

Please respond in English with clear formatting."""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        result = response.choices[0].message.content
        return jsonify({"market_analysis": result})
    except Exception as e:
        return jsonify({"market_analysis": f"Analysis failed: {str(e)}"}), 500

@app.route("/share")
def share():
    """共享链接页面"""
    return render_template("frontend.html")

@app.route("/api/health")
def health_check():
    """健康检查接口"""
    return jsonify({"status": "healthy", "service": "price-prediction-bot"})

if __name__ == "__main__":
    app.run(debug=True)
