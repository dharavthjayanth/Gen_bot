from flask import Flask, render_template, request, jsonify, session
from google import genai
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")


app.config["SESSION_PERMANENT"] = False


API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment variables")


client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Answer user questions clearly, simply, and politely."
)

@app.route("/")
def home():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        history = session.get("chat_history", [])

        
        conversation = SYSTEM_PROMPT + "\n\nConversation:\n"

        for item in history[-6:]:
            conversation += f"{item['role']}: {item['text']}\n"

        conversation += f"user: {user_message}\nassistant:"

        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation
        )

        bot_reply = response.text if response.text else "Sorry, no response."

        
        history.append({"role": "user", "text": user_message})
        history.append({"role": "assistant", "text": bot_reply})
        session["chat_history"] = history

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear():
    session["chat_history"] = []
    return jsonify({"message": "Chat cleared"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)