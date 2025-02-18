from flask import Flask, render_template, request, jsonify, session
import openai
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키 설정 (아무 값이나 설정 가능)

# OpenAI API 클라이언트 설정
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    # 새로운 방문자라면 세션 초기화
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No input received"}), 400

    try:
        # 세션에서 기존 대화 기록 가져오기
        chat_history = session.get("chat_history", [])

        # 새로운 메시지 추가
        chat_history.append({"role": "user", "content": user_input})

        # OpenAI API 호출 (이전 대화 포함)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI English conversation partner."}] + chat_history
        )

        ai_message = response.choices[0].message.content

        # AI 응답 저장
        chat_history.append({"role": "assistant", "content": ai_message})

        # 세션에 대화 기록 저장
        session["chat_history"] = chat_history

        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


