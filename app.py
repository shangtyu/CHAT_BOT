from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from openai import OpenAI
import os
import random
import re
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
    """使用DeepSeek AI进行价格预测"""
    data = request.get_json()
    product = data.get("product", "")
    
    if not product:
        return jsonify({"error": "Product description is required"}), 400
    
    # 使用DeepSeek API进行价格预测
    prompt = f"""作为一个专业的二手商品价格评估专家，请根据以下商品描述预测其二手市场价格（人民币）。

商品描述: {product}

请考虑以下因素：
1. 商品的品牌和型号
2. 使用年限和磨损程度
3. 当前市场供需情况
4. 同类产品的价格范围
5. 商品的稀有程度和保值性

请只返回一个具体的价格数字（单位：元），不要包含其他文字说明。
例如：150.00"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        
        # 尝试从回复中提取价格数字
        price_match = re.search(r'(\d+\.?\d*)', result)
        if price_match:
            predicted_price = float(price_match.group(1))
        else:
            # 如果无法解析，使用随机价格作为后备
            predicted_price = round(random.uniform(10, 200), 2)
        
        return jsonify({
            "price": predicted_price,
            "ai_response": result,
            "source": "deepseek-ai"
        })
        
    except Exception as e:
        print(f"DeepSeek API error: {str(e)}")
        # 如果API调用失败，使用随机价格作为后备
        fallback_price = round(random.uniform(10, 200), 2)
        return jsonify({
            "price": fallback_price,
            "error": f"AI prediction failed: {str(e)}",
            "source": "fallback"
        })

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
    app.run(debug=True, port=5001)
