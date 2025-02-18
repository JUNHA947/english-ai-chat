import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# OpenAI API 설정
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No input received"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI English conversation partner."},
                      {"role": "user", "content": user_input}]
        )
        ai_message = response.choices[0].message.content
        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔥 Render에서 실행될 때 올바른 포트 사용
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 제공하는 포트 사용
    app.run(host="0.0.0.0", port=port, debug=False)  # debug=False로 설정
