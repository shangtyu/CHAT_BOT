from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=" sk-1953083fe68946ca939bce624319660b",
    base_url="https://api.deepseek.com"
)

@app.route("/")
def index():
    return render_template("frontend.html")  # 注意：模板文件应放在 templates/

@app.route("/deepseek", methods=["POST"])
def deepseek_analysis():
    data = request.get_json()
    product = data.get("product", "")
    prompt = f"请提供关于以下商品的市场分析报告:\\n商品名称: {product}\\n要求: 包括市场价格趋势、同类产品比较和购买建议。以英文纯文字形式输出。"

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        result = response.choices[0].message.content
        return jsonify({"market_analysis": result})
    except Exception as e:
        return jsonify({"market_analysis": f"调用失败: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
